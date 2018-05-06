from __future__ import print_function
import ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(ast.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(ast.Number)
    def printTree(self, indent=0):
        print(createIndent(indent) + self.value)

    @addToClass(ast.Variable)
    def printTree(self, indent=0):
        print(createIndent(indent) + self.id)

    @addToClass(ast.BinOp)
    def printTree(self, indent=0):
        print(createIndent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(ast.IfElse)
    def printTree(self, indent=0):
        print(createIndent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(createIndent(indent) + 'THEN')
        self.instTrue.printTree(indent + 1)
        if self.instFalse:
            print(createIndent(indent + 1) + 'ELSE')
            self.instFalse.printTree(indent + 1)

    @addToClass(ast.ForLoop)
    def printTree(self, indent=0):
        print(createIndent(indent) + 'FOR')
        self.variable.printTree(indent + 1)
        self.varFrom.printTree(indent + 2)
        self.varTo.printTree(indent + 2)
        self.instructions.printTree(indent + 1)

    @addToClass(ast.WhileLoop)
    def printTree(self, indent=0):
        print(createIndent(indent) + 'WHILE')
        self.condition.printTree(indent + 1)
        self.instructions.printTree(indent + 1)

    @addToClass(ast.Ones)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Zeros)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Eye)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.PrintInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.ReturnInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.ContinueInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.BreakInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Array)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Range)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.SingleMatrixRef)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.DoubleMatrixRef)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.UnOp)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.PrintInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.AssignInstruction)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Matrix)
    def printTree(self, indent=0):
        pass

    @addToClass(ast.Row)
    def printTree(self, indent=0):
        pass


def createIndent(indent):
    return '|  ' * indent
