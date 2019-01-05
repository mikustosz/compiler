import os
from antlr4 import *
from gen.LatteLexer import LatteLexer
from gen.LatteParser import LatteParser
from src.LLVMVisitor import LLVMVisitor


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
    tree = parser.program()

    if compiler == "llvm":
        visitor = LLVMVisitor()
        visitor.visit(tree)
        llvm_code = visitor.get_llvm()
        with open(base_path + ".ll", "w") as file:
            print(llvm_code, file=file)
        print("Generated: " + base_path + ".ll")
        os.system(f"llvm-as {base_path}.ll")
        print("Generated: " + base_path + ".bc")

    else:
        raise ValueError("No such compiler")


