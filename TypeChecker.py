#!/usr/bin/python
import SymbolTable
import ast


class NodeVisitor(object):

    def __init__(self):
        self.table = SymbolTable.SymbolTable("root", None)
        self.errorlist = []

    def visit(self, node, stack):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, stack)

    def generic_visit(self, node, stack):        # Called if no explicit visitor function exists for a node.
        pass
        # if isinstance(node, list):
        #     for elem in node:
        #         self.visit(elem)
        # else:
        #     for child in node.children:
        #         if isinstance(child, list):
        #             for item in child:
        #                 if isinstance(item, ast.Node):
        #                     self.visit(item)
        #         elif isinstance(child, ast.Node):
        #             self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_Instr(self, node, stack):
        print("Instr visited, first:")
        self.visit(node.instruction, stack)
        print("second: ---")
        print("")
        self.visit(node.instructions, stack)

    def visit_PrintInstruction(self, node, stack):
        print("Print visited")
        self.visit(node.value, stack)

    def visit_Variable(self, node, stack):
        print("Variable visited")
        if self.table.symbols.get(node.id) is None:
            print node.line, "ERROR: variable undeclared"
        pass

    def visit_AssignInstruction(self, node, stack):
        print("Assignment visited")

        if not isinstance(node.left, ast.Variable) and not isinstance(node.left, ast.SingleMatrixRef):
            print node.line, "ERROR: assignment require variable as a left variable"
        self.table.put(node.left.id, node.right)

        self.visit(node.right, stack)

        if node.operand != '=' and (isinstance(node.right, ast.Number) or isinstance(node.left, ast.Variable)):
            print node.line, "ERROR: assignment require number as a right variable"


    def visit_BinOp(self, node, stack):
        self.visit(node.left, stack)
        self.visit(node.right, stack)

        if node.op in ['.+', '.-', '.*', './']:
            if (not isinstance(node.left, ast.Matrix) and not isinstance(node.left, ast.Variable)) or (not isinstance(node.right, ast.Matrix) and not isinstance(node.right, ast.Variable)):
                print node.line, "ERROR: incorrect arguments for the current binary operator"
            o1 = self.table.symbols.get(node.left.id)
            o2 = self.table.symbols.get(node.right.id)
            if isinstance(o1, ast.Matrix) and isinstance(o2, ast.Matrix):
                if len(o1.rows) != len(o2.rows) or len(o1.rows[0].nums) != len(o2.rows[0].nums):
                    print node.line, "ERROR: matrix of not equal dimensions"
        else:
            if (not isinstance(node.left, ast.Number) and not isinstance(node.left, ast.Variable)) or (not isinstance(node.right, ast.Number) and not isinstance(node.right, ast.Variable)):
                print node.line, "ERROR: lack of number argument for operator"

    def visit_Ones(self, node, stack):
        print("Ones visited")
        if not isinstance(node.num, ast.Variable) and not isinstance(node.num, int):
            print node.line, " ERROR: ones without a proper argument"

    def visit_Zeros(self, node, stack):
        print("Zeros visited")
        if not isinstance(node.num, ast.Variable) or not isinstance(node.num, int):
            print node.line, " ERROR: zeros without a proper argument"

    def visit_Eye(self, node, stack):
        print("Eye visited")
        if not isinstance(node.num, ast.Variable) or not isinstance(node.num, int):
            print node.line, " ERROR: eye without a proper argument"

    def visit_Matrix(self, node, stack):
        firstlen = len(node.rows[0].nums)
        for row in node.rows:
            if firstlen != len(row.nums):
                print node.line, "ERROR: matrix vectors have different length"
                break

    def visit_SingleMatrixRef(self, node, stack):
        if not isinstance(node.idx, int):
            print node.line, " ERROR: matrix reference requires integer arguments"
    
        if len(self.table.get(node.id).rows) < node.idx:
            print node.line, " ERROR: matrix reference out of matrix range"


    def visit_DoubleMatrixRef(self, node, stack):
        if not isinstance(node.idx, int) or not isinstance(node.idx2, int):
            print node.line, " ERROR: matrix reference requires integer arguments"
        if len(self.table.get(node.id).rows) < node.idx:
            print node.line, " ERROR: matrix reference out of matrix range"
        if len(self.table.get(node.id).rows[0].nums) < node.idx2:
            print node.line, " ERROR: matrix reference out of matrix range"


    def visit_ForLoop(self, node, stack):
        self.visit(node.variable, stack)
        self.visit(node.varFrom, stack)
        self.visit(node.varTo, stack)

        stack.append(node)
        self.visit(node.instructions, stack)
        stack = stack[:-1]

        if not isinstance(node.variable, str):
            print(" ERROR: incorrect variable")

        if not isinstance(node.varFrom, ast.Number):
            print(" ERROR: incorrect 'from' variable ")

        if not isinstance(node.varTo, ast.Number):
            print(" ERROR: incorrect 'to' variable ")

    def visit_WhileLoop(self, node, stack):
        self.visit(node.condition, stack)

        stack.append(node)
        self.visit(node.instructions, stack)
        stack = stack[:-1]

        if not isinstance(node.condition, str):
            print(" ERROR: incorrect variable")


    def visit_BreakInstruction(self, node, stack):
        if len(stack) == 0 or not isinstance(stack[-1], ast.ForLoop):
            print node.line, "ERROR: break without a loop"

    def visit_ContinueInstruction(self, node, stack):
        if len(stack) == 0 or not isinstance(stack[-1], ast.ForLoop):
            print(" ERROR: continue without a loop")

    def visit_ReturnInstruction(self, node, stack):
        if node.variable:
            self.visit(node.variable, stack)

            if not isinstance(node.variable, ast.Variable) or not isinstance(node.variable, ast.Number) or not isinstance(node.variable, ast.AssignInstruction) or not isinstance(node.variable, ast.Matrix):
                print(node.line + " ERROR: return with unknown type")


    # SymbolTable +
    # dict z typami (instead of most isinstance)
