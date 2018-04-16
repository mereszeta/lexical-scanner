import ply.lex as lex

reserved = {
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'eye': 'EYE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'RETURN': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'print': 'PRINT'

}
literals = "();\'=<>[]{}:,+-*/\""

tokens = [
             'DOTADD',
             'DOTSUB',
             'DOTMUL',
             'DOTDIV',

             'ADDASSIGN',
             'SUBASSIGN',
             'MULASSIGN',
             'DIVASSIGN',

             'EQ',
             'LTE',
             'GTE',
             'NE',
             'FLOATNUM',
             'INTNUM',
             'ID'
         ] + list(reserved.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.\-'
t_DOTMUL = r'\.\*'
t_DOTDIV = '\./'


t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'\/='

t_EQ = r'=='
t_LTE = r'<='
t_GTE = r'>='
t_NE = r'!='


def t_COMMENT(t):
    r'\#.*'
    pass

def t_FLOATNUM(t):
    r"""\d+\.\d+"""
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


t_ignore = " \t"


def t_newline(t):
    r'\r?\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
