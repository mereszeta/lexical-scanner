#!/usr/bin/python

import scanner
import ply.yacc as yacc
from ast import *

tokens = scanner.tokens

precedence = (
    # to fill ...
    ("left", '+', '-'),
    ("left", '*', '/')
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


def p_expression_binop(p):
    '''expression : expression + expression
                  | expression - expression
                  | expression * expression
                  | expression / expression
                  | expression < expression
                  | expression > expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
                  | expression EQ expression
                  | expression LTE expression
                  | expression GTE expression
                  | expression NE expression '''

    p[0] = BinOp(p[1], p[2], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])


parser = yacc.yacc()
