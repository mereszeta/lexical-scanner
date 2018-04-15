#!/usr/bin/python

import scanner
import ply.yacc as yacc
from ast import *

names_dictionary = {}
tokens = scanner.tokens

precedence = (
    # to fill ...
    # ("left", '+', '-'),
    # ("left", '*', '/')
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, "1",
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

def p_instruction_assign(p):
    'instruction : ID "=" expression'
    names_dictionary[p[1]] = p[3]

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

    p[0] = BinOp(p[1], p[2], p[3])


def p_expression_group(p):
    'expression : "(" expression ")"'
    p[0] = p[2]


def p_expression_number(p):
    'expression : INTNUM'
    p[0] = Number(p[1])

def p_exp_name(p):
    'expression : ID'
    try:
        p[0] = names_dictionary[p[1]]
    except LookupError:
        print("Name not defined")
        p[0] = 0


def p_expression_block(p):
    '''block : "{" instructions "}"
             | instruction '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_if_else(p):
    'instruction : IF "(" expression ")" block ELSE block'
    p[0] = IfElse(p[3], p[5], p[7])

def p_if(p):
    'instruction : IF "(" expression ")" block'
    p[0] = IfElse(p[3], p[5], None)


def p_for_1(p):
    'instruction : FOR ID "=" INTNUM ":" INTNUM "{" instructions "}"'
    p[0] = ForLoop(p[2], p[4], p[6], p[8])


def p_for_2(p):
    'instruction : FOR ID "=" INTNUM ":" INTNUM instruction '
    p[0] = ForLoop(p[2], p[4], p[6], p[7])


def p_while_1(p):
    'instruction : WHILE "(" expression ")" instruction'
    p[0] = WhileLoop(p[3], p[5])


def p_while_2(p):
    'instruction : WHILE "(" expression ")" "{" instructions "}"'
    p[0] = WhileLoop(p[3], p[6])


def p_ones(p):
    'expression : ONES "(" INTNUM ")"'
    p[0] = Ones(p[3])


def p_zeros(p):
    'expression : ZEROS "(" INTNUM ")"'
    p[0] = Zeros(p[3])


def p_eye(p):
    'expression : EYE "(" INTNUM ")"'
    p[0] = Eye(p[3])


def p_break(p):
    'instruction : BREAK ";"'
    p[0] = BreakInstruction()


def p_return(p):
    'instruction : RETURN ";"'
    p[0] = ReturnInstruction()


def p_continue(p):
    'instruction : CONTINUE ";"'
    p[0] = ContinueInstruction()


def p_print(p):
    'instruction : PRINT expression ";"'
    p[0] = PrintInstruction(p[2])


def p_array_range(p):
    'expression : ID range'
    p[0] = Array(p[2])


def p_range(p):
    'range : "[" INTNUM "," INTNUM "]" '
    p[0]= Range(p[2], p[4])

parser = yacc.yacc()
