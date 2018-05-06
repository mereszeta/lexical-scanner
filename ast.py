class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class Expr: pass

class Instr(Node):
    def __init__(self,instructions,instruction):
        self.instructions = instructions
        self.instruction = instruction


class BinOp(Expr):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op


class Number(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value


class IfElse(Node):
    def __init__(self, condition, instTrue, instFalse):
        self.condition = condition
        self.instTrue = instTrue
        self.instFalse = instFalse


class ForLoop(Node):
    def __init__(self, variable, varFrom, varTo, instructions):
        self.variable = variable
        self.varFrom = varFrom
        self.varTo = varTo
        self.instructions = instructions


class WhileLoop(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions


class Ones(Node):
    def __init__(self, num):
        self.num = num


class Zeros(Node):
    def __init__(self, num):
        self.num = num


class Eye(Node):
    def __init__(self, num):
        self.num = num


class PrintInstruction(Node):
    def __init__(self, value):
        self.value = value


class ReturnInstruction(Node):
    def __init__(self):
        pass


class ContinueInstruction(Node):
    def __init__(self):
        pass


class BreakInstruction(Node):
    def __init__(self):
        pass


class Array(Node):
    def __init__(self, range):
        self.range = range


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Variable(Expr):
    def __init__(self, id):
        self.id = id


class SingleMatrixRef(Expr):
    def __init__(self, id, idx):
        self.id = id
        self.idx = idx


class DoubleMatrixRef(Expr):
    def __init__(self, id, idx, idx2):
        self.id = id
        self.idx = idx
        self.idx2 = idx2


class UnOp(Expr):
    def __init__(self, op, right):
        self.type = "unop"
        self.op = op
        self.right = right


class AssignInstruction(Node):
    def __init__(self, operand, left, right):
        self.operand = operand
        self.left = left
        self.right = right


class Matrix(Node):
    def __init__(self):
        self.rows = []

    def append(self, row):
        self.rows.append(row)


class Row(Node):
    def __init__(self):
        self.nums = []

    def append(self, num):
        self.nums.append(num)
