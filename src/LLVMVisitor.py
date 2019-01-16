from gen.LatteParser import LatteParser
from gen.LatteVisitor import LatteVisitor
from src.constants import *
import sys

# TODO this is deprecated, remove this file and go to BackendVisitors

t_d = {  # type dictionary
    'void': 'void',
    'int': 'i32',
    'boolean': 'i32',
    'string': 'i8*',
}
default_val_d = {
    'int': 0,
    'boolean': 0,
    'string': '',
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
        self.stack = []  # TODO czy potrzebne?
        self.env = []  # env is List[Dict[ID str, value]], each list element is one block
        self.strings = []  # global constant string table
        self.string_id = 1

    def get_id(self):
        self.id += 1
        return self.id - 1

    def get_label(self):
        self.label += 1
        return self.label - 1

    def save_string(self, s):
        self.strings.append(s)
        self.string_id += 1
        return self.string_id - 1

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
        for idx, arg in enumerate(func.args):
            i = self.get_id()
            self.env[0][arg.ID] = i
            self.ins.append(f'%{i} = alloca {t_d[arg.type]}')
            self.ins.append(f'store i32 %{idx}, i32* %{i}')

        self.visitChildren(ctx)

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
            if var_type == 'string':
                raise_runtime_error(ctx, 'Jeszcze nie zaimplementowałem tego lol')

            i = self.get_id()
            self.ins.append(f'%{i} = alloca {t_d[var_type]}')
            self.env[-1][var_name] = i  # TODO string

            if item.expr() is None:
                self.ins.append(f'store i32 0, i32* %{i}')
            else:
                r_expr = self.visit(item.expr())
                self.ins.append(f'store i32 %{r_expr}, i32* %{i}')

    def visitAss(self, ctx: LatteParser.AssContext):
        var_ID = ctx.ID().getText()
        r_expr = self.visit(ctx.expr())
        r_var = self.get_variable(ctx, var_ID)
        self.ins.append(f'store i32 %{r_expr}, i32* %{r_var}')

    def visitIncr(self, ctx: LatteParser.IncrContext, op='add nsw'):
        var_ID = ctx.ID().getText()
        r_var = self.get_variable(ctx, var_ID)
        i = self.get_id()
        self.ins.append(f'%{i} = load i32, i32* %{r_var}')
        i = self.get_id()
        self.ins.append(f'%{i} = {op} i32 %{i - 1}, 1')
        self.ins.append(f'store i32  %{i}, i32* %{r_var}')
        return i

    def visitDecr(self, ctx: LatteParser.DecrContext):
        self.visitIncr(ctx, op='sub nsw')

    def visitRet(self, ctx: LatteParser.RetContext):
        r = self.visit(ctx.expr())
        self.ins.append(f'ret i32 %{r}')

    def visitVRet(self, ctx: LatteParser.VRetContext):
        self.ins.append('ret void')

    def visitCond(self, ctx: LatteParser.CondContext):
        self.visitChildren(ctx)

    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        self.visitChildren(ctx)

    def visitWhile(self, ctx: LatteParser.WhileContext):
        self.visitChildren(ctx)

    # === Expressions ===
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
        r1 = self.visit(ctx.expr(0))
        r2 = self.visit(ctx.expr(1))
        i = self.get_id()
        self.ins.append(f'%{i} = {op_d[op]} i32 %{r1}, %{r2}')
        return i

    # def visitSExp(self, ctx):
    #     r = self.visit(ctx.expr())
    #     i = self.get_id()
    #     self.ins.append(f"%{i} = call i32 (i8*, ...)@printf(i8* getelementptr inbounds"
    #                     f"([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %{r})")


    # === Expressions ===
    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        r = self.visit(ctx.expr())
        i = self.get_id()
        op_d = {'-': f'sub nsw i32 0, %{r}',
                '!': f'sub nsw i32 1, %{r}'}
        op = ctx.getChild(0).getText()
        self.ins.append(f'%{i} = {op_d[op]}')
        return i

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

    def visitEId(self, ctx: LatteParser.EIdContext):
        i = self.get_id()
        r_var = self.get_variable(ctx, ctx.ID().getText())
        self.ins.append(f'%{i} = load i32, i32* %{r_var}')
        return i

    def visitEInt(self, ctx: LatteParser.EIntContext):
        val = ctx.INT().getText()
        i = self.get_id()
        self.ins.append(f'%{i} = add i32 {val}, 0')
        return i

    def visitETrue(self, ctx: LatteParser.ETrueContext):
        i = self.get_id()
        self.ins.append(f'%{i} = add i32 1, 0')
        return i

    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        i = self.get_id()
        self.ins.append(f'%{i} = add i32 0, 0')
        return i

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        func_ID = ctx.ID().getText()
        func = self.functions[func_ID]

        rs = [self.visit(expr) for expr in ctx.expr()]  # get list of expression registers
        arg_str = ', '.join([f'{t_d[var.type]} %{r}' for r, var in zip(rs, func.args)])
        i = self.id - 1
        instr = ''
        if func.type != 'void':
            i = self.get_id()
            instr = f'%{i} = '
        instr += f'call {t_d[func.type]} @{func_ID}({arg_str})'
        self.ins.append(instr)
        return i

    def visitEStr(self, ctx: LatteParser.EStrContext):
        return self.save_string(ctx.STR().getText())  # TODO it's returning other int than usual

    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visit(ctx.expr())

    # TODO deprec
    def visitExpVar(self, ctx):
        name = ctx.ID().getText()
        self.id += 1
        self.stack.append(self.id)
        self.ins.append(f"%{self.id} = load i32, i32* %{name}")

    def get_llvm(self):
        return HEADER + '\n'.join(self.ins) + FOOTER
        # decs = [f"%{v} = alloca i32" for v in self.memory]
        # return self._get_header() + "\n".join(decs + self.ins) + self._get_footer()
