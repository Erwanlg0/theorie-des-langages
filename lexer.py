import ast

import ply.lex as lex


tokens = (
    'IDENTIFIANT', 'NOMBRE', 'CHAINE',
    'EGAL', 'POINT_VIRGULE', 'VIRGULE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PLUS', 'MOINS', 'FOIS', 'DIVISE',
    'PLUS_PLUS', 'PLUS_EGAL', 'MOINS_EGAL', 'FOIS_EGAL', 'DIVISE_EGAL',
    'INFERIEUR', 'SUPERIEUR', 'EGAL_EGAL',
    'PRINT', 'IF', 'ELSE', 'WHILE', 'FOR', 'FUNCTION', 'RETURN', 'VAR',
)


reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'var': 'VAR',
}


t_PLUS_PLUS = r'\+\+'
t_PLUS_EGAL = r'\+='
t_MOINS_EGAL = r'-='
t_FOIS_EGAL = r'\*='
t_DIVISE_EGAL = r'/='
t_EGAL_EGAL = r'=='
t_EGAL = r'='
t_POINT_VIRGULE = r';'
t_VIRGULE = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'
t_MOINS = r'-'
t_FOIS = r'\*'
t_DIVISE = r'/'
t_INFERIEUR = r'<'
t_SUPERIEUR = r'>'

t_ignore = ' \t'


def t_COMMENTAIRE_BLOC(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_COMMENTAIRE_LIGNE(t):
    r'(//[^\n]*|\#[^\n]*)'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_CHAINE(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = ast.literal_eval(t.value)
    return t


def t_NOMBRE(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIANT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIANT')
    return t


def t_error(t):
    print(f"Erreur lexicale ligne {t.lexer.lineno} : caractere illegal '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
