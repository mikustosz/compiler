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
        self.ins = []  # instructions
        self.stack = []
        self.env = []  # env is List[Dict[ID str, value]], each list element is one block



    def get_variable(self, ctx, var_ID: str):
        for block in reversed(self.env):
            if var_ID in block:
                return block[var_ID]
        raise_runtime_error(ctx, f'Variable {var_ID} not defined in this scope')


    def _visit_both(self, ctx, op):
        self.visit(ctx.exp(0))
        self.visit(ctx.exp(1))
        self.id += 1
        last_id1 = self.stack.pop()
        last_id2 = self.stack.pop()
        self.stack.append(self.id)
        self.ins.append(f"%{self.id} = " + op + f" i32 %{last_id2}, %{last_id1}")

    # === Functions ===

    def visitTopDef(self, ctx: LatteParser.TopDefContext):
        func_ID = ctx.ID().getText()
        func_type = self.functions[func_ID].type
        arg_types = ', '.join([t_d[var.type] for var in self.functions[func_ID].args])
        self.ins.append(f'define {t_d[func_type]} @{func_ID}({arg_types}) {{')
        self.ins.append('call void @printInt(i32 123123)')

        self.visitChildren(ctx)

        self.ins.append('ret i32 0\n}')

        # Cleanup for the next function
        self.env = []
        self.id = 1
        self.stack = []

    # === Statements ===
    def visitBlock(self, ctx: LatteParser.BlockContext):
        self.env.append({})
        self.visitChildren(ctx)

    def visitDecl(self, ctx: LatteParser.DeclContext):
        var_type = ctx.type_().getText()
        for item in ctx.item():
            var_name = item.ID().getText()
            if var_name in self.env[-1]:
                raise_runtime_error(ctx, f'Variable {var_name} is declared twice in this scope')
            self.env[-1][var_name] = default_val_d[var_type]  # empty decl gives default value
            if item.expr() is not None:  # this happens only when item is of type "ID '=' expr"
                # Calculate the expression here
                self.visit(item.expr())

    def visitAss(self, ctx: LatteParser.AssContext):
        self.visitChildren(ctx)

    def visitIncr(self, ctx: LatteParser.IncrContext):
        self.visitChildren(ctx)

    def visitDecr(self, ctx: LatteParser.DecrContext):
        self.visitChildren(ctx)

    def visitRet(self, ctx: LatteParser.RetContext):
        self.visitChildren(ctx)

    def visitVRet(self, ctx: LatteParser.VRetContext):
        self.visitChildren(ctx)

    def visitCond(self, ctx: LatteParser.CondContext):
        self.visitChildren(ctx)

    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        self.visitChildren(ctx)

    def visitWhile(self, ctx: LatteParser.WhileContext):
        self.visitChildren(ctx)


    # === Expressions ===

    def visitSExp(self, ctx):
        self.visit(ctx.exp())
        self.id += 1
        last_id = self.stack.pop()
        self.ins.append(f"%{self.id} = call i32 (i8*, ...)@printf(i8* getelementptr inbounds"
                        f"([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %{last_id})")

    def visitSAss(self, ctx):
        name = ctx.ID().getText()
        self.memory.add(name)
        self.visit(ctx.exp())
        last_id = self.stack.pop()
        self.ins.append(f"store i32 %{last_id}, i32* %{name}")

    # === Expressions ===
    def visitExpVar(self, ctx):
        name = ctx.ID().getText()
        self.id += 1
        self.stack.append(self.id)
        self.ins.append(f"%{self.id} = load i32, i32* %{name}")

    def visitExpLit(self, ctx):
        val = ctx.INTEGER().getText()
        self.id += 1
        self.stack.append(self.id)
        self.ins.append(f"%{self.id} = add i32 {val}, 0")

    def visitExpPar(self, ctx): self.visit(ctx.exp())

    def visitExpDiv(self, ctx): self._visit_both(ctx, "sdiv")

    def visitExpAdd(self, ctx): self._visit_both(ctx, "add nsw")

    def visitExpMul(self, ctx): self._visit_both(ctx, "mul nsw")

    def visitExpSub(self, ctx): self._visit_both(ctx, "sub nsw")

    def get_llvm(self):
        return HEADER + '\n'.join(self.ins) + FOOTER
        # decs = [f"%{v} = alloca i32" for v in self.memory]
        # return self._get_header() + "\n".join(decs + self.ins) + self._get_footer()
