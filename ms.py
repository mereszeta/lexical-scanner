# import sys
# import scanner
# import parser
# from treeprinter import TreePrinter
#
# if __name__ == '__main__':
#
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example3.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     parser = parser.parser
#     text = file.read()
#     ast = parser.parse(text, lexer=scanner.lexer)
#     ast.printTree()

import sys
import ply.yacc as yacc
import parser
import scanner
from Interpreter import Interpreter
from treeprinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = parser.parser
    parser = yacc.yacc(module=parser)
    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
    ast.accept(Interpreter())
