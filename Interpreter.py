import ast
import SymbolTable
from Memory import *
from Exceptions import *
from visitor import *
import sys
import numpy

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(ast.BinOp)
    def visit(self, node):
        opmap = dict({('+', lambda left, right: left + right),
                      ('-', lambda left, right: left - right),
                      ('*', lambda left, right: left * right),
                      ('/', lambda left, right: left / right),
                      ('>', lambda left, right: left > right),
                      ('<', lambda left, right: left < right),
                      ('DOTADD', lambda left, right: left + right),
                      ('DOTSUB', lambda left, right: left - right),
                      ('DOTMUL', lambda left, right: numpy.multiply(left, right)),
                      ('DOTDIV', lambda left, right: numpy.divide(left, right)),
                      ('EQ', lambda left, right: left == right),
                      ('LTE', lambda left, right: left <= right),
                      ('GTE', lambda left, right: left >= right),
                      ('NE', lambda left, right: left != right)})
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return opmap[node.op](r1, r2)

    @when(ast.UnOp)
    def visit(self, node):
        opmap = dict({('-', lambda val: -val),
                      ('!', lambda val: not val),
                      ("'", lambda val: numpy.transpose(val))
                      })
        r = node.right.accept(self)
        return opmap[node.op](r)

    @when(ast.AssignInstruction)
    def visit(self, node):
        opmap = dict({
            ('-=', lambda left, right: left - right),
            ('*=', lambda left, right: left * right),
            ('/=', lambda left, right: left / right),
            ('=', lambda left, right: right),
            ('+=', lambda left, right: left + right)
        })
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        res = opmap[node.operand](r1, r2)
        if not self.stack.set(node.left.id, res):
            self.stack.insert(node.left.id, res)
        pass

    # simplistic while loop interpretation
    @when(ast.WhileLoop)
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            try:
                r = node.instructions.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
        return r

    @when(ast.Range)
    def visit(self, node):
        return range(node.start.accept(self), node.end.accept(self))

    @when(ast.ForLoop)
    def visit(self, node):
        self.stack.insert(node.variable.id, node.varFrom.accept(self))
        rng = range(node.varFrom.accept(self), node.varTo.accept(self))
        for i in rng:
            self.stack.set(node.variable.id, i)
            try:
                r = node.instructions.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
        return r

    @when(ast.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            r = node.instTrue.accept(self)
        elif not node.condition.accept(self) and node.instFalse:
            r = node.instFalse.accept(self)
        return r

    @when(ast.PrintInstruction)
    def visit(self, node):
        print node.value.accept(self)

    @when(ast.PrintExpression)
    def visit(self, node):
        return str(node.expression.accept(self))

    @when(ast.PrintExpressions)
    def visit(self, node):
        return str(node.expression.accept(self)) + str(node.expressions.accept(self))

    @when(ast.BreakInstruction)
    def visit(self, node):
        raise BreakException

    @when(ast.ContinueInstruction)
    def visit(self, node):
        raise ContinueException

    @when(ast.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(node.value.accept(self))

    @when(ast.Instr)
    def visit(self, node):
        instruction = node.instruction.accept(self)
        instructions = node.instructions.accept(self)

    @when(ast.Number)
    def visit(self, node):
        return node.value

    @when(ast.Variable)
    def visit(self, node):
        return self.stack.get(node.id)

    @when(ast.Array)
    def visit(self, node):
        return node.range.accept(self)

    @when(ast.Row)
    def visit(self, node):
        return node.nums

    @when(ast.Matrix)
    def visit(self, node):
        rs = []
        for row in node.rows:
            rs.append(row.accept(self))
        return numpy.array(rs)

    @when(ast.SingleMatrixRef)
    def visit(self, node):
        idx = node.idx.accept(self)
        matrix = self.stack.get(node.id)
        return matrix[idx]

    @when(ast.DoubleMatrixRef)
    def visit(self, node):
        idx1 = node.idx.accept(self)
        idx2 = node.idx2.accept(self)
        matrix = self.stack.get(node.id)
        return matrix[idx1][idx2]
