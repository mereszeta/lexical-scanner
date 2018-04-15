class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class Expr: pass


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