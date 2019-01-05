# Generated from Latte.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LatteParser import LatteParser
else:
    from LatteParser import LatteParser

# This class defines a complete listener for a parse tree produced by LatteParser.
class LatteListener(ParseTreeListener):

    # Enter a parse tree produced by LatteParser#program.
    def enterProgram(self, ctx:LatteParser.ProgramContext):
        pass

    # Exit a parse tree produced by LatteParser#program.
    def exitProgram(self, ctx:LatteParser.ProgramContext):
        pass


    # Enter a parse tree produced by LatteParser#topDef.
    def enterTopDef(self, ctx:LatteParser.TopDefContext):
        pass

    # Exit a parse tree produced by LatteParser#topDef.
    def exitTopDef(self, ctx:LatteParser.TopDefContext):
        pass


    # Enter a parse tree produced by LatteParser#arg.
    def enterArg(self, ctx:LatteParser.ArgContext):
        pass

    # Exit a parse tree produced by LatteParser#arg.
    def exitArg(self, ctx:LatteParser.ArgContext):
        pass


    # Enter a parse tree produced by LatteParser#block.
    def enterBlock(self, ctx:LatteParser.BlockContext):
        pass

    # Exit a parse tree produced by LatteParser#block.
    def exitBlock(self, ctx:LatteParser.BlockContext):
        pass


    # Enter a parse tree produced by LatteParser#Empty.
    def enterEmpty(self, ctx:LatteParser.EmptyContext):
        pass

    # Exit a parse tree produced by LatteParser#Empty.
    def exitEmpty(self, ctx:LatteParser.EmptyContext):
        pass


    # Enter a parse tree produced by LatteParser#BlockStmt.
    def enterBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by LatteParser#BlockStmt.
    def exitBlockStmt(self, ctx:LatteParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by LatteParser#Decl.
    def enterDecl(self, ctx:LatteParser.DeclContext):
        pass

    # Exit a parse tree produced by LatteParser#Decl.
    def exitDecl(self, ctx:LatteParser.DeclContext):
        pass


    # Enter a parse tree produced by LatteParser#Ass.
    def enterAss(self, ctx:LatteParser.AssContext):
        pass

    # Exit a parse tree produced by LatteParser#Ass.
    def exitAss(self, ctx:LatteParser.AssContext):
        pass


    # Enter a parse tree produced by LatteParser#Incr.
    def enterIncr(self, ctx:LatteParser.IncrContext):
        pass

    # Exit a parse tree produced by LatteParser#Incr.
    def exitIncr(self, ctx:LatteParser.IncrContext):
        pass


    # Enter a parse tree produced by LatteParser#Decr.
    def enterDecr(self, ctx:LatteParser.DecrContext):
        pass

    # Exit a parse tree produced by LatteParser#Decr.
    def exitDecr(self, ctx:LatteParser.DecrContext):
        pass


    # Enter a parse tree produced by LatteParser#Ret.
    def enterRet(self, ctx:LatteParser.RetContext):
        pass

    # Exit a parse tree produced by LatteParser#Ret.
    def exitRet(self, ctx:LatteParser.RetContext):
        pass


    # Enter a parse tree produced by LatteParser#VRet.
    def enterVRet(self, ctx:LatteParser.VRetContext):
        pass

    # Exit a parse tree produced by LatteParser#VRet.
    def exitVRet(self, ctx:LatteParser.VRetContext):
        pass


    # Enter a parse tree produced by LatteParser#Cond.
    def enterCond(self, ctx:LatteParser.CondContext):
        pass

    # Exit a parse tree produced by LatteParser#Cond.
    def exitCond(self, ctx:LatteParser.CondContext):
        pass


    # Enter a parse tree produced by LatteParser#CondElse.
    def enterCondElse(self, ctx:LatteParser.CondElseContext):
        pass

    # Exit a parse tree produced by LatteParser#CondElse.
    def exitCondElse(self, ctx:LatteParser.CondElseContext):
        pass


    # Enter a parse tree produced by LatteParser#While.
    def enterWhile(self, ctx:LatteParser.WhileContext):
        pass

    # Exit a parse tree produced by LatteParser#While.
    def exitWhile(self, ctx:LatteParser.WhileContext):
        pass


    # Enter a parse tree produced by LatteParser#SExp.
    def enterSExp(self, ctx:LatteParser.SExpContext):
        pass

    # Exit a parse tree produced by LatteParser#SExp.
    def exitSExp(self, ctx:LatteParser.SExpContext):
        pass


    # Enter a parse tree produced by LatteParser#Int.
    def enterInt(self, ctx:LatteParser.IntContext):
        pass

    # Exit a parse tree produced by LatteParser#Int.
    def exitInt(self, ctx:LatteParser.IntContext):
        pass


    # Enter a parse tree produced by LatteParser#Str.
    def enterStr(self, ctx:LatteParser.StrContext):
        pass

    # Exit a parse tree produced by LatteParser#Str.
    def exitStr(self, ctx:LatteParser.StrContext):
        pass


    # Enter a parse tree produced by LatteParser#Bool.
    def enterBool(self, ctx:LatteParser.BoolContext):
        pass

    # Exit a parse tree produced by LatteParser#Bool.
    def exitBool(self, ctx:LatteParser.BoolContext):
        pass


    # Enter a parse tree produced by LatteParser#Void.
    def enterVoid(self, ctx:LatteParser.VoidContext):
        pass

    # Exit a parse tree produced by LatteParser#Void.
    def exitVoid(self, ctx:LatteParser.VoidContext):
        pass


    # Enter a parse tree produced by LatteParser#item.
    def enterItem(self, ctx:LatteParser.ItemContext):
        pass

    # Exit a parse tree produced by LatteParser#item.
    def exitItem(self, ctx:LatteParser.ItemContext):
        pass


    # Enter a parse tree produced by LatteParser#EId.
    def enterEId(self, ctx:LatteParser.EIdContext):
        pass

    # Exit a parse tree produced by LatteParser#EId.
    def exitEId(self, ctx:LatteParser.EIdContext):
        pass


    # Enter a parse tree produced by LatteParser#EFunCall.
    def enterEFunCall(self, ctx:LatteParser.EFunCallContext):
        pass

    # Exit a parse tree produced by LatteParser#EFunCall.
    def exitEFunCall(self, ctx:LatteParser.EFunCallContext):
        pass


    # Enter a parse tree produced by LatteParser#ERelOp.
    def enterERelOp(self, ctx:LatteParser.ERelOpContext):
        pass

    # Exit a parse tree produced by LatteParser#ERelOp.
    def exitERelOp(self, ctx:LatteParser.ERelOpContext):
        pass


    # Enter a parse tree produced by LatteParser#ETrue.
    def enterETrue(self, ctx:LatteParser.ETrueContext):
        pass

    # Exit a parse tree produced by LatteParser#ETrue.
    def exitETrue(self, ctx:LatteParser.ETrueContext):
        pass


    # Enter a parse tree produced by LatteParser#EOr.
    def enterEOr(self, ctx:LatteParser.EOrContext):
        pass

    # Exit a parse tree produced by LatteParser#EOr.
    def exitEOr(self, ctx:LatteParser.EOrContext):
        pass


    # Enter a parse tree produced by LatteParser#EInt.
    def enterEInt(self, ctx:LatteParser.EIntContext):
        pass

    # Exit a parse tree produced by LatteParser#EInt.
    def exitEInt(self, ctx:LatteParser.EIntContext):
        pass


    # Enter a parse tree produced by LatteParser#EUnOp.
    def enterEUnOp(self, ctx:LatteParser.EUnOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EUnOp.
    def exitEUnOp(self, ctx:LatteParser.EUnOpContext):
        pass


    # Enter a parse tree produced by LatteParser#EStr.
    def enterEStr(self, ctx:LatteParser.EStrContext):
        pass

    # Exit a parse tree produced by LatteParser#EStr.
    def exitEStr(self, ctx:LatteParser.EStrContext):
        pass


    # Enter a parse tree produced by LatteParser#EMulOp.
    def enterEMulOp(self, ctx:LatteParser.EMulOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EMulOp.
    def exitEMulOp(self, ctx:LatteParser.EMulOpContext):
        pass


    # Enter a parse tree produced by LatteParser#EAnd.
    def enterEAnd(self, ctx:LatteParser.EAndContext):
        pass

    # Exit a parse tree produced by LatteParser#EAnd.
    def exitEAnd(self, ctx:LatteParser.EAndContext):
        pass


    # Enter a parse tree produced by LatteParser#EParen.
    def enterEParen(self, ctx:LatteParser.EParenContext):
        pass

    # Exit a parse tree produced by LatteParser#EParen.
    def exitEParen(self, ctx:LatteParser.EParenContext):
        pass


    # Enter a parse tree produced by LatteParser#EFalse.
    def enterEFalse(self, ctx:LatteParser.EFalseContext):
        pass

    # Exit a parse tree produced by LatteParser#EFalse.
    def exitEFalse(self, ctx:LatteParser.EFalseContext):
        pass


    # Enter a parse tree produced by LatteParser#EAddOp.
    def enterEAddOp(self, ctx:LatteParser.EAddOpContext):
        pass

    # Exit a parse tree produced by LatteParser#EAddOp.
    def exitEAddOp(self, ctx:LatteParser.EAddOpContext):
        pass


    # Enter a parse tree produced by LatteParser#addOp.
    def enterAddOp(self, ctx:LatteParser.AddOpContext):
        pass

    # Exit a parse tree produced by LatteParser#addOp.
    def exitAddOp(self, ctx:LatteParser.AddOpContext):
        pass


    # Enter a parse tree produced by LatteParser#mulOp.
    def enterMulOp(self, ctx:LatteParser.MulOpContext):
        pass

    # Exit a parse tree produced by LatteParser#mulOp.
    def exitMulOp(self, ctx:LatteParser.MulOpContext):
        pass


    # Enter a parse tree produced by LatteParser#relOp.
    def enterRelOp(self, ctx:LatteParser.RelOpContext):
        pass

    # Exit a parse tree produced by LatteParser#relOp.
    def exitRelOp(self, ctx:LatteParser.RelOpContext):
        pass


