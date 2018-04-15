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
