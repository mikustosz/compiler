import os, sys
from antlr4 import *
from gen.LatteLexer import LatteLexer
from gen.LatteParser import LatteParser
from src.Visitors import FunctionReaderVisitor, FrontendValidationVisitor, ReturnReachabilityVisitor, check_reachability
from src.CustomErrorListener import CustomErrorListener



def main(argv, compiler):
    if len(argv) <= 1:
        print("Please specify .lat file as an argument")
        return
    file_path = argv[1]
    base_path, extension = os.path.splitext(file_path)

    if extension != ".lat":
        print("Input file must have '.lat' extension")
        return
    input_stream = FileStream(file_path)
    lexer = LatteLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LatteParser(token_stream)
    # TODO uncomment the line for correct errors? But then shows too much errors
    # lexer._listeners = [CustomErrorListener()]  # Hack to change default behavior of lexer/parser errors
    # parser._listeners = [CustomErrorListener()]
    tree = parser.program()
    # print(tree.toStringTree(recog=parser))  # TODO Debug

    if compiler == "llvm":
        functionReader = FunctionReaderVisitor()
        functionReader.visit(tree)
        functions = functionReader.get_functions()

        frontendValidation = FrontendValidationVisitor(functions)
        frontendValidation.visit(tree)

        check_reachability(tree, functions)


        # llvm_code = visitor.get_llvm()

        # with open(base_path + ".ll", "w") as file:
        #     print(llvm_code, file=file)
        # print("Generated: " + base_path + ".ll")
        # os.system(f"llvm-as {base_path}.ll")
        # print("Generated: " + base_path + ".bc")

        print('OK', file=sys.stderr)
    else:
        raise ValueError("No such compiler")


