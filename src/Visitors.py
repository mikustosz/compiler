from typing import List, Dict

from gen.LatteParser import LatteParser
from gen.LatteVisitor import LatteVisitor
from dataclasses import dataclass, field
import sys


@dataclass(frozen=True)
class Var:
    type: str
    ID: str


@dataclass
class Func:
    type: str
    ID: str
    args: List[Var]
    vars: Dict[str, Var]


def find_function_name(ctx):
    top_def_ctx = ctx
    while not isinstance(top_def_ctx, LatteParser.TopDefContext):
        top_def_ctx = top_def_ctx.parentCtx
    return top_def_ctx.func_ID_hack


class FunctionReaderVisitor(LatteVisitor):
    def __init__(self):
        self.functions = {}

    # Read function declarations
    def visitTopDef(self, ctx: LatteParser.TopDefContext):
        args = []
        i = 0
        # iterate over the list of the function arguments
        while ctx.arg() and i < len(ctx.arg().children):
            args.append(Var(type=ctx.arg().getChild(i).getText(), ID=ctx.arg().getChild(i + 1).getText()))
            i += 3  # +3 because the third child is a comma (',')

        func_ID = ctx.ID().getText()
        if func_ID in self.functions:
            raise_frontend_error(ctx, 'Function ' + func_ID + ' is declared twice')
        self.functions[func_ID] = Func(type=ctx.type_().getText(), ID=func_ID, args=args, vars={})

        # Noting the function name in the context
        ctx.func_ID_hack = func_ID
        return self.visitChildren(ctx)

    # Read variable declarations inside function
    def visitDecl(self, ctx: LatteParser.DeclContext):
        func_ID = find_function_name(ctx)
        var_type = ctx.type_().getText()

        # Now iterate over other variables
        for item in ctx.item():
            if item.expr() is not None:  # this happens only when item is of type "ID '=' expr"
                exprValidator = ExprValidateVisitor(self.functions)
                expr_type = exprValidator.visit(item)
                if expr_type != var_type:
                    raise_frontend_expr_type_error(ctx)
            var_ID = item.ID().getText()
            if var_ID in self.functions[func_ID].vars:
                raise_frontend_error(ctx, f'Variable {var_ID} is declared second time')
            self.functions[func_ID].vars[var_ID] = Var(var_type, var_ID)

    def get_functions(self):
        return self.functions


### FRONTEND VISITOR ###

def raise_frontend_error(ctx, msg):
    print(f'ERROR\nFrontend error on line {ctx.start.line}: {msg}', file=sys.stderr)
    sys.exit(1)


def raise_frontend_expr_type_error(ctx):
    raise_frontend_error(ctx, 'Expression type is invalid')


class ExprValidateVisitor(LatteVisitor):
    def __init__(self, functions):
        self.functions = functions

    # This is for two children exprs, both must be the same given type
    def _both_should_have_type(self, type_, ctx):
        type1 = self.visit(ctx.expr(0))
        type2 = self.visit(ctx.expr(1))
        if type1 == type2 == type_:
            return type_
        raise_frontend_expr_type_error(ctx)

    def visitEUnOp(self, ctx: LatteParser.EUnOpContext):
        type_ = self.visit(ctx.expr())
        operator = ctx.children[0].getText()
        if operator == '!' and type_ == 'boolean':
            return 'boolean'
        if operator == '-' and type_ == 'int':
            return 'int'
        raise_frontend_expr_type_error(ctx)

    def visitEMulOp(self, ctx: LatteParser.EMulOpContext):
        return self._both_should_have_type('int', ctx)

    def visitEAddOp(self, ctx: LatteParser.EAddOpContext):
        return self._both_should_have_type('int', ctx)

    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        return self._both_should_have_type('boolean', ctx)

    def visitEAnd(self, ctx: LatteParser.EAndContext):
        return self._both_should_have_type('boolean', ctx)

    def visitEOr(self, ctx: LatteParser.EOrContext):
        return self._both_should_have_type('boolean', ctx)

    def visitEId(self, ctx: LatteParser.EIdContext):
        func_ID = find_function_name(ctx)
        return self.functions[func_ID].vars[ctx.ID().getText()].type

    def visitEInt(self, ctx: LatteParser.EIntContext):
        return 'int'

    def visitETrue(self, ctx: LatteParser.ETrueContext):
        return 'boolean'

    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        return 'boolean'

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        return self.functions[ctx.ID().getText()].type

    def visitEStr(self, ctx: LatteParser.EStrContext):
        return 'string'

    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visitChildren(ctx)


class FrontendValidationVisitor(LatteVisitor):
    def __init__(self, functions):
        self.functions = functions

    def visitProgram(self, ctx: LatteParser.ProgramContext):
        # Most general rules checked here
        if 'main' not in self.functions:
            raise_frontend_error(ctx, 'You should declare the "main" function')
        return self.visitChildren(ctx)

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        func_ID = ctx.ID().getText()

        # Validate if it's declared
        if func_ID not in self.functions:
            raise_frontend_error(ctx, 'Function ' + func_ID + ' was not declared')

        # Validate if number of arguments is right
        args = self.functions[func_ID].args
        exprs = ctx.expr()
        if len(args) != len(exprs):
            raise_frontend_error(ctx, 'Function ' + func_ID + ' has wrong number of arguments')

        # Validate if exps are the same type as declared args
        exprValidator = ExprValidateVisitor(self.functions)
        for i, expr in enumerate(exprs):
            type_ = exprValidator.visit(expr)
            if self.functions[func_ID].args[i].type != type_:
                raise_frontend_error(ctx, f'Function {func_ID} is called with wrong argument type: argument nr {i+1}')

        return self.visitChildren(ctx)
