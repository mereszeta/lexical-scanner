#!/usr/bin/python

import scanner
import ply.yacc as yacc
from ast import *

names_dictionary = {}
tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFY'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', '<', '>', 'EQ', 'LTE', 'GTE', 'NE',),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", "DOTADD", "DOTSUB"),
    ("left", "DOTMUL", "DOTDIV"),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, "1",
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions
               |
    """
    p[0] = p[1]


def p_instructions_1(p):
    """instructions : instruction instructions
                    | instruction"""
    if len(p) == 3:
        p[0] = Instr(p[2], p[1])
    else:
        p[0] = p[1]


def p_instruction(p):
    """ instruction : assign_instruction ";"
                    | print_instruction ";"
                    | return_instruction ";"
                    | break_instruction ";"
                    | continue_instruction ";"
                    | for_instruction
                    | while_instruction
                    | choice_instruction """
    p[0] = p[1]


def p_expression_group(p):
    'expression : "(" expression ")"'
    p[0] = p[2]


def p_assign_instruction(p):
    '''assign_instruction : var assign_operand expression
                         | var assign_operand assign_instruction
                         | var "=" matrix_init_instruction
    '''
    p[0] = AssignInstruction(p[1], p[2], p[3], p.lexer.lineno)


def p_var(p):
    '''
            var : ID
           | ID '[' INTNUM ']'
           | ID '[' INTNUM ',' INTNUM ']'
    '''
    if len(p) == 2:
        p[0] = Variable(p[1], p.lexer.lineno)
    elif len(p) == 5:
        p[0] = SingleMatrixRef(p[1], p[3], p.lexer.lineno)
    elif len(p) == 7:
        p[0] = DoubleMatrixRef(p[1], p[3], p[5], p.lexer.lineno)


def p_assign_operand(p):
    '''assign_operand : "="
                      | ADDASSIGN
                      | SUBASSIGN
                      | MULASSIGN
                      | DIVASSIGN
    '''
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression "+" expression
                  | expression "-" expression
                  | expression "*" expression
                  | expression "/" expression
                  | expression "<" expression
                  | expression ">" expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
                  | expression EQ expression
                  | expression LTE expression
                  | expression GTE expression
                  | expression NE expression '''
    p[0] = BinOp(p[1], p[2], p[3], p.lexer.lineno)


def p_expression_number(p):
    '''expression : INTNUM'''
    p[0] = Number(int(p[1]))


def p_expression_float(p):
    '''expression : FLOATNUM'''
    p[0] = Number(float(p[1]))


def p_expression_var(p):
    '''expression : var'''
    p[0] = p[1]


# def p_exp_name(p):
#   '''expression : ID'''
#  try:
#     p[0] = names_dictionary[p[1]]
# except LookupError:
#    print("Name not defined")
#   p[0] = 0


def p_expression_unop(p):
    '''expression : "-" expression
                  | "!" expression
                  | expression "'"
    '''
    if p[2] != "'":
        p[0] = UnOp(p[1], p[2])
    else:
        p[0] = UnOp(p[2], p[1])


def p_expression_block(p):
    '''block : "{" instructions "}"
             | instruction '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_choice_instruction(p):
    """choice_instruction : if_else """
    p[0] = p[1]


def p_if_else(p):
    '''if_else : IF "(" expression ")" block %prec IFY
             | IF "(" expression ")" block ELSE block'''
    if len(p) == 7:
        p[0] = IfElse(p[3], p[5], p[7])
    else:
        p[0] = IfElse(p[3], p[5], None)


def p_for_instruction(p):
    """for_instruction : for_1
                       | for_2"""
    p[0] = p[1]


def p_for_1(p):
    'for_1 : FOR ID "=" expression ":" expression "{" instructions "}"'
    p[0] = ForLoop(Variable(p[2], p.lexer.lineno), p[4], p[6], p[8], p.lexer.lineno)


def p_for_2(p):
    'for_2 : FOR ID "=" expression ":" expression instruction '
    p[0] = ForLoop(Variable(p[2], p.lexer.lineno), p[4], p[6], p[7], p.lexer.lineno)


def p_while_instruction(p):
    """while_instruction : while_1
                         | while_2"""
    p[0] = p[1]


def p_while_1(p):
    'while_1 : WHILE "(" expression ")" instruction'
    p[0] = WhileLoop(p[3], p[5])


def p_while_2(p):
    'while_2 : WHILE "(" expression ")" "{" instructions "}"'
    p[0] = WhileLoop(p[3], p[6])


def p_ones(p):
    'ones : ONES "(" INTNUM ")"'
    p[0] = Matrix(p.lexer.lineno)
    for i in range(p[3]):
        row = Row()
        for j in range(p[3]):
            row.append(1)
        p[0].append(row)


def p_zeros(p):
    'zeros : ZEROS "(" INTNUM ")"'
    p[0] = Matrix(p.lexer.lineno)
    for i in range(p[3]):
        row = Row()
        for j in range(p[3]):
            row.append(0)
        p[0].append(row)


def p_eye(p):
    'eye : EYE "(" INTNUM ")"'
    p[0] = Matrix(p.lexer.lineno)
    for i in range(p[3]):
        row = Row()
        for j in range(p[3]):
            if i == j:
                row.append(1)
            else:
                row.append(0)
        p[0].append(row)


def p_break_instruction(p):
    'break_instruction : BREAK'

    p[0] = BreakInstruction(p.lexer.lineno)


def p_return_instruction(p):
    'return_instruction : RETURN'
    p[0] = ReturnInstruction()


def p_continue_instruction(p):
    'continue_instruction : CONTINUE'
    p[0] = ContinueInstruction()


def p_print_instruction(p):
    '''print_instruction : PRINT vars_to_print
                       | PRINT '"' vars_to_print '"' '''
    if (p[2] != '"'):
        p[0] = PrintInstruction(p[2])
    else:
        p[0] = PrintInstruction(p[3])


def p_print_list(p):
    """vars_to_print : vars_to_print ',' expression
                     | expression"""
    if len(p) == 2:
        p[0] = PrintExpression(p[1])
    else:
        p[0] = PrintExpressions(p[1], p[3])


def p_matrix_init_instruction(p):
    '''matrix_init_instruction : matrix_init_fun
                               | '[' matrix_row ']'
                               | '[' matrix_rows ']'
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_matrix_init_fun(p):
    '''matrix_init_fun : zeros
                       | ones
                       | eye
    '''
    p[0] = p[1]


def p_matrix_row(p):
    """matrix_row : matrix_row ',' INTNUM
                      | INTNUM """
    p[0] = Row()
    if len(p) == 4:
        p[0].concat(p[1], p[3])
    else:
        p[0].append(p[1])


def p_matrix_rows(p):
    """matrix_rows : matrix_row ';' matrix_rows
                   | matrix_row"""
    p[0] = Matrix(p.lexer.lineno)
    if len(p) == 4:
        p[0].concat(p[3], p[1])
    else:
        p[0].append(p[1])


parser = yacc.yacc()
