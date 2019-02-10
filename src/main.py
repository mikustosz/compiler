import os, sys
from antlr4 import *
from gen.LatteLexer import LatteLexer
from gen.LatteParser import LatteParser
from src.FrontendVisitors import FunctionReaderVisitor, FrontendValidationVisitor, check_reachability
from src.LLVMVisitor import LLVMVisitor
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
    lexer._listeners = [CustomErrorListener()]  # Change default behavior of lexer/parser errors
    parser._listeners = [CustomErrorListener()]
    try: tree = parser.program()
    except: return
    # print(tree.toStringTree(recog=parser))  # Debug

    if compiler == "llvm":
        functionReader = FunctionReaderVisitor()
        try: functionReader.visit(tree)
        except: return
        functions = functionReader.get_functions()

        frontendValidation = FrontendValidationVisitor(functions)
        try: frontendValidation.visit(tree)
        except: return

        try: check_reachability(tree, functions)
        except: return
        # Generating backend code
        llvmVisitor = LLVMVisitor(functions)
        try: llvmVisitor.visit(tree)
        except: return

        llvm_code = llvmVisitor.get_llvm()

        with open(base_path + ".ll", "w") as file:
            print(llvm_code, file=file)
        print("Generated: " + base_path + ".ll")
        os.system(f"llvm-as {base_path}.ll")
        print("Generated: " + base_path + ".bc")

        print('OK', file=sys.stderr)
    else:
        raise ValueError("No such compiler")


