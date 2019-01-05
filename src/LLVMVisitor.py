from gen.LatteVisitor import LatteVisitor


class LLVMVisitor(LatteVisitor):
    def __init__(self):
        self.memory = set()
        self.id = 1
        self.ins = []
        self.stack = []

    @staticmethod
    def _get_header():
        return """@.str = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"\ndefine i32 @main() {\n%1 = alloca i32\n"""

    @staticmethod
    def _get_footer(): return "\nret i32 0\n}\ndeclare i32 @printf(i8*, ...)\n"

    def _visit_both(self, ctx, op):
        self.visit(ctx.exp(0))
        self.visit(ctx.exp(1))
        self.id += 1
        last_id1 = self.stack.pop()
        last_id2 = self.stack.pop()
        self.stack.append(self.id)
        self.ins.append(f"%{self.id} = " + op + f" i32 %{last_id2}, %{last_id1}")

    # === Statements ===
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
        decs = [f"%{v} = alloca i32" for v in self.memory]
        return self._get_header() + "\n".join(decs + self.ins) + self._get_footer()
