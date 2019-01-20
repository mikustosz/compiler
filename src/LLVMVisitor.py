from gen.LatteParser import LatteParser
from gen.LatteVisitor import LatteVisitor
from src.FrontendVisitors import FrontendValidationVisitor
from src.constants import *
import sys

# TODO this is deprecated, remove this file and go to BackendVisitors

t_d = {  # type dictionary
    'void': 'void',
    'int': 'i32',
    'boolean': 'i1',
    'string': 'i8*',
}


def raise_runtime_error(ctx, msg):
    print(f'ERROR\nRuntime error on line {ctx.start.line}: {msg}', file=sys.stderr)
    sys.exit(1)


class LLVMVisitor(LatteVisitor):
    def __init__(self, functions):
        self.functions = functions
        # self.memory = set()
        self.id = 1
        self.label = 1
        self.ins = []  # instructions
        self.env = []  # env is List[Dict[ID str, (register, type)]], each list element is one block
        self.strings = ['']  # global constant string table

    def get_id(self):
        self.id += 1
        return self.id - 1

    def get_label(self):
        self.label += 1
        return self.label - 1

    def get_variable(self, ctx, var_ID: str):
        for block in reversed(self.env):
            if var_ID in block:
                return block[var_ID]
        raise_runtime_error(ctx, f'Variable {var_ID} not defined in this scope')

    # === Functions ===

    def visitTopDef(self, ctx: LatteParser.TopDefContext):
        func_ID = ctx.ID().getText()
        func = self.functions[func_ID]

        # Cleanup
        self.env = [{}]
        self.id = len(func.args) + 1

        arg_types = ', '.join([t_d[var.type] for var in func.args])
        self.ins.append(f'define {t_d[func.type]} @{func_ID}({arg_types}) {{')
        # self.ins.append(f'L{self.get_label()}:')
        for idx, arg in enumerate(func.args):
            i = self.get_id()
            self.env[0][arg.ID] = (i, arg.type)
            self.ins.append(f'%{i} = alloca {t_d[arg.type]}')
            self.ins.append(f'store {t_d[arg.type]} %{idx}, {t_d[arg.type]}* %{i}')

        self.visitChildren(ctx)

        if func.type == 'void':
            self.ins.append('ret void')
        elif func.type == 'string':
            i = self.get_id()
            self.ins.append(f'%{i} = bitcast [1 x i8]* @s0 to i8*')
            self.ins.append(f'ret i8* %{i}')
        else:
            self.ins.append(f'ret {t_d[func.type]} 0')
        self.ins.append('}')

    # === Statements ===
    def visitBlockStmt(self, ctx: LatteParser.BlockStmtContext):
        self.env.append({})
        self.visitChildren(ctx)
        self.env.pop()

    def visitDecl(self, ctx: LatteParser.DeclContext):
        var_type = ctx.type_().getText()
        for item in ctx.item():
            var_name = item.ID().getText()
            if var_name in self.env[-1]:
                raise_runtime_error(ctx, f'Variable {var_name} is declared twice in this scope')

            i = self.get_id()
            self.ins.append(f'%{i} = alloca {t_d[var_type]}')
            self.env[-1][var_name] = i, var_type


            if item.expr() is None:
                if var_type == 'string':
                    i = self.get_id()
                    self.ins.append(f'%{i} = bitcast [1 x i8]* @s0 to i8*')
                else:
                    self.ins.append(f'store {t_d[var_type]} 0, {t_d[var_type]}* %{i}')
            else:
                r_expr, _ = self.visit(item.expr())
                self.ins.append(f'store {t_d[var_type]} %{r_expr}, {t_d[var_type]}* %{i}')

    def visitAss(self, ctx: LatteParser.AssContext):
        var_ID = ctx.ID().getText()
        r_expr, t_expr = self.visit(ctx.expr())
        r_var, var_t = self.get_variable(ctx, var_ID)
        assert var_t == t_expr, f'Wrong value assigned to {var_ID}'
        self.ins.append(f'store {t_d[t_expr]} %{r_expr}, {t_d[t_expr]}* %{r_var}')

    def visitIncr(self, ctx: LatteParser.IncrContext, op='add nsw'):
        var_ID = ctx.ID().getText()
        r_var, var_t = self.get_variable(ctx, var_ID)
        i = self.get_id()
        assert var_t == 'int'
        self.ins.append(f'%{i} = load i32, i32* %{r_var}')
        i = self.get_id()
        self.ins.append(f'%{i} = {op} i32 %{i - 1}, 1')
        self.ins.append(f'store i32  %{i}, i32* %{r_var}')
        return i

    def visitDecr(self, ctx: LatteParser.DecrContext):
        self.visitIncr(ctx, op='sub nsw')

    def visitRet(self, ctx: LatteParser.RetContext):
        r, t = self.visit(ctx.expr())
        self.get_id()
        self.ins.append(f'ret {t_d[t]} %{r}')

    def visitVRet(self, ctx: LatteParser.VRetContext):
        self.ins.append('ret void')
        self.get_id()

    def visitCond(self, ctx: LatteParser.CondContext):
        self.visitCondElse(ctx)

    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        l_true = self.get_label()
        l_false = self.get_label()
        l_next = self.get_label()
        r, t = self.visit(ctx.expr())
        self.ins.append(f'br {t_d[t]} %{r}, label %L{l_true}, label %L{l_false}')
        self.ins.append(f'L{l_true}:')
        if isinstance(ctx, LatteParser.CondElseContext):
            self.visit(ctx.stmt(0))
        else:
            self.visit(ctx.stmt())

        self.ins.append(f'br label %L{l_next}')

        self.ins.append(f'L{l_false}:')
        if isinstance(ctx, LatteParser.CondElseContext):
            self.visit(ctx.stmt(1))

        self.ins.append(f'br label %L{l_next}')  # TODO are these two necessary?

        self.ins.append(f'L{l_next}:')

    def visitWhile(self, ctx: LatteParser.WhileContext):
        l_expr = self.get_label()
        l_true = self.get_label()
        l_false = self.get_label()

        self.ins.append(f'br label %L{l_expr}')
        self.ins.append(f'L{l_expr}:')
        r, t = self.visit(ctx.expr())
        self.ins.append(f'br {t_d[t]} %{r}, label %L{l_true}, label %L{l_false}')

        self.ins.append(f'L{l_true}:')
        self.visit(ctx.stmt())
        self.ins.append(f'br label %L{l_expr}')

        self.ins.append(f'L{l_false}:')

    # === Expressions ===
    def get_type(self, ctx):
        v = FrontendValidationVisitor(self.functions)
        v.env = self.env
        return v.visit(ctx)

    def _visit_both(self, ctx, op):
        op_d = {
            '+': 'add nsw',
            '-': 'sub nsw',
            '*': 'mul nsw',
            '/': 'sdiv',
            '%': 'srem',
            '<': 'icmp slt',
            '<=': 'icmp sle',
            '>': 'icmp sgt',
            '>=': 'icmp sge',
            '==': 'icmp eq',
            '!=': 'icmp ne',
            '&&': 'and',
            '||': 'or',
        }
        r1, t1 = self.visit(ctx.expr(0))
        r2, t2 = self.visit(ctx.expr(1))
        assert t1 == t2, f'Types mismatch: {t1} {op} {t2}'
        i = self.get_id()
        if op == '+' and t1 == 'string':
            self.ins.append(f'%{i} = call i8* @concat(i8* %{r1}, i8* %{r2})')
        else:
            self.ins.append(f'%{i} = {op_d[op]} {t_d[t1]} %{r1}, %{r2}')
        return i, self.get_type(ctx)

    def visitSExp(self, ctx: LatteParser.SExpContext):
        self.visit(ctx.expr())  # TODO tylko func call warto odwiedzać

    # === Expressions ===
    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        r, t = self.visit(ctx.expr())
        i = self.get_id()
        op_d = {'-': f'sub nsw {t_d[t]} 0, %{r}',
                '!': f'sub nsw {t_d[t]} 1, %{r}'}
        op = ctx.getChild(0).getText()
        self.ins.append(f'%{i} = {op_d[op]}')
        return i, self.get_type(ctx)

    def visitEMulOp(self, ctx: LatteParser.EMulOpContext):
        return self._visit_both(ctx, ctx.mulOp().getText())

    def visitEAddOp(self, ctx: LatteParser.EAddOpContext):
        return self._visit_both(ctx, ctx.addOp().getText())

    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        return self._visit_both(ctx, ctx.relOp().getText())

    def visitEAnd(self, ctx: LatteParser.EAndContext):
        return self._visit_both(ctx, '&&')

    def visitEOr(self, ctx: LatteParser.EOrContext):
        return self._visit_both(ctx, '||')

    def visitEId(self,
                 ctx: LatteParser.EIdContext):  # TODO This won't work in blocks, you need to remember type from frontend
        i = self.get_id()
        r_var, var_t = self.get_variable(ctx, ctx.ID().getText())
        self.ins.append(f'%{i} = load {t_d[var_t]}, {t_d[var_t]}* %{r_var}')
        return i, self.get_type(ctx)

    def visitEInt(self, ctx: LatteParser.EIntContext):
        val = ctx.INT().getText()
        i = self.get_id()
        self.ins.append(f'%{i} = add i32 {val}, 0')
        return i, self.get_type(ctx)

    def visitETrue(self, ctx: LatteParser.ETrueContext):
        i = self.get_id()
        self.ins.append(f'%{i} = add i1 1, 0')
        return i, self.get_type(ctx)

    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        i = self.get_id()
        self.ins.append(f'%{i} = add i1 0, 0')
        return i, self.get_type(ctx)

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        func_ID = ctx.ID().getText()
        func = self.functions[func_ID]

        rs = [self.visit(expr)[0] for expr in ctx.expr()]  # get list of expression registers
        arg_str = ', '.join([f'{t_d[var.type]} %{r}' for r, var in zip(rs, func.args)])
        i = self.id - 1
        instr = ''
        if func.type != 'void':
            i = self.get_id()
            instr = f'%{i} = '
        instr += f'call {t_d[func.type]} @{func_ID}({arg_str})'
        self.ins.append(instr)
        return i, self.get_type(ctx)

    def visitEStr(self, ctx: LatteParser.EStrContext):
        s = ctx.STR().getText()[1:-1]
        i = self.get_id()
        s_idx = len(self.strings)
        if s in self.strings:
            s_idx = self.strings.index(s)
        else:
            self.strings.append(s)
        self.ins.append(f'%{i} = bitcast [{len(s)+1} x i8]* @s{s_idx} to i8*')
        return i, self.get_type(ctx)

    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visit(ctx.expr())

    def get_llvm(self):
        string_decs = [f'@s{i} = internal constant [{len(s)+1} x i8] c"{s}\\00"' for i, s in enumerate(self.strings)]
        return HEADER + '\n'.join(string_decs) + '\n\n' + '\n'.join(self.ins)
