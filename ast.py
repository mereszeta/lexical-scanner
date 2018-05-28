class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def accept(self, visitor):
        return visitor.visit(self)


# done
class Instr(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction


# done
class BinOp(Node):
    def __init__(self, left, op, right, line):
        self.line = line
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op


# done
class Number(Node):
    def __init__(self, value):
        self.type = "number"
        self.value = value


# done
class IfElse(Node):
    def __init__(self, condition, instTrue, instFalse):
        self.condition = condition
        self.instTrue = instTrue
        self.instFalse = instFalse


# done
class ForLoop(Node):
    def __init__(self, variable, varFrom, varTo, instructions, line):
        self.line = line
        self.variable = variable
        self.varFrom = varFrom
        self.varTo = varTo
        self.instructions = instructions


# done
class WhileLoop(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions


# done
class PrintInstruction(Node):
    def __init__(self, value):
        self.value = value


# done
class PrintExpressions(Node):
    def __init__(self, expression, expressions):
        self.expression = expression
        self.expressions = expressions


# done
class PrintExpression(Node):
    def __init__(self, expression):
        self.expression = expression


# done
class ReturnInstruction(Node):
    def __init__(self):
        pass


# done
class ContinueInstruction(Node):
    def __init__(self):
        pass


# done
class BreakInstruction(Node):
    def __init__(self, line):
        self.line = line
        pass


# done
class Array(Node):
    def __init__(self, range):
        self.range = range


# done
class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


# done
class Variable(Node):
    def __init__(self, id, line):
        self.line = line
        self.id = id


# done
class SingleMatrixRef(Node):
    def __init__(self, id, idx, line):
        self.line = line
        self.id = id
        self.idx = idx


# done
class DoubleMatrixRef(Node):
    def __init__(self, id, idx, idx2, line):
        self.line = line
        self.id = id
        self.idx = idx
        self.idx2 = idx2


# done
class UnOp(Node):
    def __init__(self, op, right):
        self.type = "unop"
        self.op = op
        self.right = right


# done
class AssignInstruction(Node):
    def __init__(self, left, operand, right, line):
        self.line = line
        self.operand = operand
        self.left = left
        self.right = right


# done
class Matrix(Node):
    def __init__(self, line):
        self.line = line
        self.rows = []

    def append(self, row):
        self.rows.append(row)

    def concat(self, mtx, row):
        self.rows = list(mtx.rows)
        self.rows.append(row)


# done
class Row(Node):
    def __init__(self):
        self.nums = []

    def append(self, num):
        self.nums.append(num)

    def concat(self, row, num):
        self.nums = list(row.nums)
        self.append(num)
