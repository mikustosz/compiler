from typing import List, Dict

from gen.LatteParser import LatteParser
from gen.LatteVisitor import LatteVisitor
from dataclasses import dataclass
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


def find_function_name(ctx):
    top_def_ctx = ctx
    while not isinstance(top_def_ctx, LatteParser.TopDefContext):
        top_def_ctx = top_def_ctx.parentCtx
    return top_def_ctx.func_ID_hack


def get_func(type, ID, args):
    return Func(type=type, ID=ID, args=args)


class FunctionReaderVisitor(LatteVisitor):
    def __init__(self):
        self.functions = {
            'printInt': get_func('void', 'printInt', [Var('int', 'x')]),
            'printString': get_func('void', 'printString', [Var('string', 'x')]),
            'error': get_func('void', 'error', []),
            'readInt': get_func('int', 'readInt', []),
            'readString': get_func('string', 'readString', []),
        }
        self.block = 0

    # Read function declarations
    def visitTopDef(self, ctx: LatteParser.TopDefContext):
        self.block = 0
        func_ID = ctx.ID().getText()
        func_type = ctx.type_().getText()
        args = []
        i = 0
        # iterate over the list of the function arguments
        while ctx.arg() and i < len(ctx.arg().children):
            arg_type = ctx.arg().getChild(i).getText()
            if arg_type == 'void':
                raise_frontend_error(ctx, 'Void is not a possible type for a variable')
            arg_ID = ctx.arg().getChild(i + 1).getText()
            # Check if an argument of the same name alredy exists in this function:
            for j in range(len(args)):
                if arg_ID == args[j].ID:
                    raise_frontend_error(ctx, f'Function {func_ID} has two arguments with the same name: {arg_ID}')
            args.append(Var(type=arg_type, ID=arg_ID))
            i += 3  # +3 because the third child is a comma (',')

        if func_ID in self.functions:
            raise_frontend_error(ctx, 'Function ' + func_ID + ' is declared twice')
        self.functions[func_ID] = get_func(func_type, func_ID, args)

        # Noting the function name in the context
        ctx.func_ID_hack = func_ID
        return self.visitChildren(ctx)

    # Read variable declarations inside function (but don't check expr types)
    # def visitDecl(self, ctx: LatteParser.DeclContext):
    #     func_ID = find_function_name(ctx)
    #     var_type = ctx.type_().getText()
    #
    #     # Now iterate over other variables
    #     for item in ctx.item():
    #         var_ID = item.ID().getText()
    #         # TODO check double declaration in the same scope
    #         # if var_ID in self.functions[func_ID].vars:
    #         #     raise_frontend_error(ctx, f'Variable {var_ID} is declared second time')
    #         if var_type == 'void':
    #             raise_frontend_error(ctx, f'Void is not proper type for a variable')
    #         self.functions[func_ID].vars[var_ID] = Var(var_type, var_ID)

    def get_functions(self):
        return self.functions


### FRONTEND VISITOR ###

def raise_frontend_error(ctx, msg):
    print(f'ERROR\nFrontend error on line {ctx.start.line}: {msg}', file=sys.stderr)
    sys.exit(1)


def raise_frontend_expr_type_error(ctx):
    raise_frontend_error(ctx, 'Expression type is invalid')


class FrontendValidationVisitor(LatteVisitor):
    def __init__(self, functions):
        self.functions = functions
        self.env = [{}]  # List[Dict[var_ID: (register, type)]]

    def get_variable(self, var_ID: str):
        for block in reversed(self.env):
            if var_ID in block:
                return block[var_ID]

    # Most general rules checked here
    def visitProgram(self, ctx: LatteParser.ProgramContext):
        if 'main' not in self.functions:
            raise_frontend_error(ctx, 'You should declare the "main" function')
        self.visitChildren(ctx)

    def visitTopDef(self, ctx: LatteParser.TopDefContext):
        func_ID = ctx.ID().getText()
        self.env = [{arg.ID: (0, arg.type) for arg in self.functions[func_ID].args}]
        self.visitChildren(ctx)

    def visitBlockStmt(self, ctx: LatteParser.BlockStmtContext):
        self.env.append({})
        self.visitChildren(ctx)
        self.env.pop()

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        func_ID = ctx.ID().getText()

        # Validate if used function is declared
        if func_ID not in self.functions:
            raise_frontend_error(ctx, 'Function ' + func_ID + ' was not declared')

        # Validate if number of arguments is right
        args = self.functions[func_ID].args
        exprs = ctx.expr()
        if len(args) != len(exprs):
            raise_frontend_error(ctx, 'Function ' + func_ID + ' has wrong number of arguments')

        # Validate if exps are the same type as declared args
        for i, expr in enumerate(exprs):
            type_ = self.visit(expr)
            if self.functions[func_ID].args[i].type != type_:
                raise_frontend_error(ctx, f'Function {func_ID} is called with wrong argument type: argument nr {i + 1}')

        self.visitChildren(ctx)

    def visitAss(self, ctx: LatteParser.AssContext):
        # Check if the type of assigned expression is the same as variable type
        var_ID = ctx.ID().getText()
        x = self.get_variable(var_ID)
        if x is None:
            raise_frontend_error(ctx, f'Variable {var_ID} was not declared')
        expr_type = self.visit(ctx.expr())
        if expr_type != x[1]:
            raise_frontend_expr_type_error(ctx)
        return self.visitChildren(ctx)

    def visitRet(self, ctx: LatteParser.RetContext):
        # expression in return should always bear type of declared function type
        func_ID = find_function_name(ctx)
        func_type = self.functions[func_ID].type
        expr_type = self.visit(ctx.expr())

        if expr_type != func_type:
            raise_frontend_error(ctx, f'Function {func_ID} should return {func_type}, not {expr_type}')
        return self.visitChildren(ctx)

    def visitVRet(self, ctx: LatteParser.VRetContext):
        func_ID = find_function_name(ctx)
        func_type = self.functions[func_ID].type
        if func_type != 'void':
            raise_frontend_error(ctx, f'Function {func_ID} should return {func_type}, not void')

    # check if assigned expression is of correct type
    def visitDecl(self, ctx: LatteParser.DeclContext):
        var_type = ctx.type_().getText()
        for item in ctx.item():
            var_ID = item.ID().getText()
            if var_ID in self.env[-1]:
                raise_frontend_error(ctx, f'Variable {var_ID} is declared second time in this scope')
            self.env[-1][var_ID] = (0, var_type)
            if item.expr() is not None:  # this happens only when item is of type "ID '=' expr"
                expr_type = self.visit(item)
                if expr_type != var_type:
                    raise_frontend_expr_type_error(ctx)

    def visitCond(self, ctx: LatteParser.CondContext):
        expr_type = self.visit(ctx.expr())
        if expr_type != 'boolean':
            raise_frontend_expr_type_error(ctx)

    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        self.visitCond(ctx)

    ########### EXPRESSIONS ##############
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
        type1 = self.visit(ctx.expr(0))
        type2 = self.visit(ctx.expr(1))
        if type1 == type2 and type1 in ['int', 'string']:
            return type1
        raise_frontend_expr_type_error(ctx)

    def visitERelOp(self, ctx: LatteParser.ERelOpContext):
        type1 = self.visit(ctx.expr(0))
        type2 = self.visit(ctx.expr(1))
        op = ctx.relOp().getText()

        if op in ['<', '<=', '>', '>=']:
            if type1 == type2 and type1 == 'int':
                return 'boolean'
            raise_frontend_expr_type_error(ctx)
        if op in ['==', '!=']:
            if type1 == type2:
                return 'boolean'
        raise_frontend_expr_type_error(ctx)

    def visitEAnd(self, ctx: LatteParser.EAndContext):
        return self._both_should_have_type('boolean', ctx)

    def visitEOr(self, ctx: LatteParser.EOrContext):
        return self._both_should_have_type('boolean', ctx)

    def visitEId(self, ctx: LatteParser.EIdContext):
        var_ID = ctx.ID().getText()
        x = self.get_variable(var_ID)
        if x is None:
            raise_frontend_error(ctx, f'Variable {var_ID} was not declared (EId)')
        return x[1]

    def visitEInt(self, ctx: LatteParser.EIntContext):
        return 'int'

    def visitETrue(self, ctx: LatteParser.ETrueContext):
        return 'boolean'

    def visitEFalse(self, ctx: LatteParser.EFalseContext):
        return 'boolean'

    def visitEFunCall(self, ctx: LatteParser.EFunCallContext):
        func_ID = ctx.ID().getText()
        if func_ID not in self.functions:
            raise_frontend_error(ctx, f'Function {func_ID} was not declared')
        return self.functions[ctx.ID().getText()].type

    def visitEStr(self, ctx: LatteParser.EStrContext):
        return 'string'

    def visitEParen(self, ctx: LatteParser.EParenContext):
        return self.visit(ctx.children[1])


########## REACHABILITY ############

def check_reachability(tree, functions):
    reachability = ReturnReachabilityVisitor(functions)
    for topDef in tree.children:
        func_ID = topDef.ID().getText()
        if functions[func_ID].type == 'void':
            continue
        is_reachable = reachability.visit(topDef)
        if not is_reachable:
            raise_frontend_error(topDef, f'Return clause is not present or may be unreachable in function {func_ID}')


# This visitor tells if there is a reachable return clause in a function
class ReturnReachabilityVisitor(LatteVisitor):
    def __init__(self, functions):
        self.functions = functions

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is True or nextResult is True:
            return True

    # This code is just for simple true/false expressions
    def visitCond(self, ctx: LatteParser.CondContext):
        expr_text = ctx.expr().getText()
        if expr_text == 'true':
            return self.visitChildren(ctx)

    def visitCondElse(self, ctx: LatteParser.CondElseContext):
        expr_text = ctx.expr().getText()
        if_result = self.visit(ctx.stmt(0))
        else_result = self.visit(ctx.stmt(1))
        if expr_text == 'true':
            return if_result
        elif expr_text == 'false':
            return else_result
        if if_result and else_result:  # When in both clauses we have return it's 100% reachable
            return True

    def visitWhile(self, ctx: LatteParser.WhileContext):
        expr_text = ctx.expr().getText()
        if expr_text == 'true':
            return self.visitChildren(ctx)

    def visitRet(self, ctx: LatteParser.RetContext):
        return True

    # def visitVRet(self, ctx: LatteParser.VRetContext):
