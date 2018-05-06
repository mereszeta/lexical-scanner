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

    @addToClass(ast.Instr)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)
        self.instruction.printTree(indent)

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
        print(createIndent(indent) + "ones")
        print(createIndent(indent) + str(self.num))

    @addToClass(ast.Zeros)
    def printTree(self, indent=0):
        print(createIndent(indent) + "zeros")
        print(createIndent(indent) + str(self.num))

    @addToClass(ast.Eye)
    def printTree(self, indent=0):
        print(createIndent(indent) + "ones")
        print(createIndent(indent) + str(self.num))

    @addToClass(ast.PrintInstruction)
    def printTree(self, indent=0):
        print(createIndent(indent) + "print")
        self.value.printTree(indent + 1)

    @addToClass(ast.ReturnInstruction)
    def printTree(self, indent=0):
        print(createIndent(indent) + "return")

    @addToClass(ast.ContinueInstruction)
    def printTree(self, indent=0):
        print(createIndent(indent) + "continue")

    @addToClass(ast.BreakInstruction)
    def printTree(self, indent=0):
        print(createIndent(indent) + "break")

    @addToClass(ast.Array)
    def printTree(self, indent=0):
        print(createIndent(indent) + "arr")
        self.range.printTree(indent + 1)

    @addToClass(ast.Range)
    def printTree(self, indent=0):
        self.start.printTree(indent)
        self.end.printTree(indent)

    @addToClass(ast.SingleMatrixRef)
    def printTree(self, indent=0):
        print(createIndent(indent) + "ref")
        self.id.printTree(indent + 1)
        self.idx.printTree(indent + 1)

    @addToClass(ast.DoubleMatrixRef)
    def printTree(self, indent=0):
        print(createIndent(indent) + "ref")
        self.id.printTree(indent + 1)
        self.idx.printTree(indent + 1)
        self.idx2.printTree(indent + 1)

    @addToClass(ast.UnOp)
    def printTree(self, indent=0):
        if type(self.op) == str:
            print(createIndent(indent) + self.op)
        else:
            self.op.printTree(indent)
        if type(self.right) == str:
            print(createIndent(indent+1) + self.right)
        else:
            self.right.printTree(indent+1)

    @addToClass(ast.AssignInstruction)
    def printTree(self, indent=0):
        print(createIndent(indent) + self.operand)
        if type(self.left) is not int:
            self.left.printTree(indent + 1)
        else:
            print(createIndent(indent + 1), self.left)
        if type(self.right) is not int:
            self.right.printTree(indent + 1)
        else:
            print(createIndent(indent + 1), self.right)

    @addToClass(ast.Matrix)
    def printTree(self, indent=0):
        print(createIndent(indent) + "Matrix")
        for row in self.rows:
            row.printTree(indent + 1)

    @addToClass(ast.Row)
    def printTree(self, indent=0):
        print(createIndent(indent) + "Vector")
        for num in self.nums:
            print(createIndent(indent + 1), str(num))


def createIndent(indent):
    return '|  ' * indent
