import ply.lex as lex

tokens = (
    'IDENTIFIANT', 'NOMBRE', 'EGAL', 'POINT_VIRGULE', 'PRINT',
    'LPAREN', 'RPAREN', 'PLUS', 'MOINS', 'FOIS', 'DIVISE',
    'IF', 'ELSE', 'WHILE', 'INFERIEUR', 'SUPERIEUR', 'EGAL_EGAL',
    'LBRACE', 'RBRACE','FOR'
)

reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for':'FOR'
}

t_EGAL        = r'='
t_POINT_VIRGULE = r';'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_PLUS        = r'\+'
t_MOINS       = r'-'
t_FOIS        = r'\*'
t_DIVISE      = r'/'
t_INFERIEUR   = r'<'
t_SUPERIEUR   = r'>'
t_EGAL_EGAL   = r'=='

t_ignore = ' \t\n'

def t_NOMBRE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIANT(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIANT')
    return t

def t_error(t):
    print(f"Caractère illégal ignoré : '{t.value[0]}'")
    t.lexer.skip(1)

# Construction du Lexer
lexer = lex.lex()