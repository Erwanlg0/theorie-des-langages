import ply.yacc as yacc
from lexer import tokens

# La mémoire 
variables = {}

# Ordre de priorité des opérations
precedence = (
    ('left', 'INFERIEUR', 'SUPERIEUR', 'EGAL_EGAL'),
    ('left', 'PLUS', 'MOINS'),
    ('left', 'FOIS', 'DIVISE'),
    ('right', 'UMINUS'),
)


# --- LA GRAMMAIRE ---

def p_start(p):
    'start : bloc'
    p[0] = p[1]
    print("--- AST ---")
    print(p[0])
    print("--- EXECUTION ---")
    evalInst(p[0])


def p_bloc_instruction(p):
    '''bloc : instruction
            | instruction bloc'''
    if len(p) == 2:
        p[0] = ('bloc', p[1], 'empty')
    else:
        p[0] = ('bloc', p[1], p[2])


def p_instruction_affectation(p):
    'instruction : IDENTIFIANT EGAL expression POINT_VIRGULE'
    p[0] = ('assign', p[1], p[3])


def p_instruction_print(p):
    'instruction : PRINT LPAREN expression RPAREN POINT_VIRGULE'
    p[0] = ('print', p[3])


def p_instruction_if(p):
    'instruction : IF LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('if', p[3], p[6], 'empty')


def p_instruction_if_else(p):
    'instruction : IF LPAREN expression RPAREN LBRACE bloc RBRACE ELSE LBRACE bloc RBRACE'
    p[0] = ('if', p[3], p[6], p[10])


def p_instruction_while(p):
    'instruction : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE'
    p[0] = ('while', p[3], p[6])


def p_expression_nombre(p):
    'expression : NOMBRE'
    p[0] = ('nombre', p[1])


def p_expression_identifiant(p):
    'expression : IDENTIFIANT'
    p[0] = ('var', p[1])


def p_expression_math(p):
    '''expression : expression PLUS expression
                  | expression MOINS expression
                  | expression FOIS expression
                  | expression DIVISE expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_comparaison(p):
    '''expression : expression INFERIEUR expression
                  | expression SUPERIEUR expression
                  | expression EGAL_EGAL expression'''
    p[0] = (p[2], p[1], p[3])


def p_affectation_simple(p):
    'affectation_simple : IDENTIFIANT EGAL expression'
    p[0] = ('assign', p[1], p[3])


def p_instruction_for(p):
    'instruction : FOR LPAREN affectation_simple POINT_VIRGULE expression POINT_VIRGULE affectation_simple RPAREN LBRACE bloc RBRACE'
    # p[3]  = initialisation  (i=0)
    # p[5]  = condition        (i<4)
    # p[7]  = incrementation   (i=i+1)
    # p[10] = le bloc a repeter
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_expression_uminus(p):
    'expression : MOINS expression %prec UMINUS'
    p[0] = ('uminus', p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_instruction_vide(p):
    'instruction : POINT_VIRGULE'
    p[0] = 'empty'


def p_error(p):
    if p:
        print(f"Erreur de syntaxe vers '{p.value}'")
    else:
        print("Erreur de syntaxe à la fin du fichier")

parser = yacc.yacc()


def evalExpr(t):
    if t[0] == 'nombre':
        return t[1]

    if t[0] == 'var':
        nom_var = t[1]
        if nom_var in variables:
            return variables[nom_var]
        else:
            print(f"Erreur : Variable '{nom_var}' non initialisée")
            return 0

    # Mathématiques
    if t[0] == '+':
        return evalExpr(t[1]) + evalExpr(t[2])
    elif t[0] == '-':
        return evalExpr(t[1]) - evalExpr(t[2])
    elif t[0] == '*':
        return evalExpr(t[1]) * evalExpr(t[2])
    elif t[0] == '/':
        droite = evalExpr(t[2])
        if droite == 0:
            print("Erreur : Division par zéro")
            return 0
        return evalExpr(t[1]) / droite
    elif t[0] == 'uminus':
        return -evalExpr(t[1])
    elif t[0] == '<':
        return evalExpr(t[1]) < evalExpr(t[2])
    elif t[0] == '>':
        return evalExpr(t[1]) > evalExpr(t[2])
    elif t[0] == '==':
        return evalExpr(t[1]) == evalExpr(t[2])


def evalInst(t):
    if t == 'empty':
        return

    if t[0] == 'bloc':
        evalInst(t[1])
        evalInst(t[2])

    elif t[0] == 'assign':
        variables[t[1]] = evalExpr(t[2])

    elif t[0] == 'print':
        print(f"calc > {evalExpr(t[1])}")

    elif t[0] == 'if':
        condition = evalExpr(t[1])
        if condition:
            evalInst(t[2])
        else:
            evalInst(t[3])

    elif t[0] == 'while':
        while evalExpr(t[1]):
            evalInst(t[2])

    elif t[0] == 'for':
        initialisation = t[1]
        condition = t[2]
        incrementation = t[3]
        bloc_interieur = t[4]

        evalInst(initialisation)

        while evalExpr(condition):
            evalInst(bloc_interieur)
            evalInst(incrementation)


#  TEST
if __name__ == '__main__':
    # affectation, print
    s1 = 'x=4;x=x+3;print(x);'
    # operations arithmetiques
    s2 = 'a=10;b=3;c=a*b;print(c);d=a/b;print(d);'
    # if
    s3 = 'x=5;if(x>3){print(x);};'
    # if-else
    s4 = 'x=2;if(x>3){print(x);}else{y=99;print(y);};'
    # while
    s5 = 'x=4;while(x<30){x=x+3;print(x);};'
    # for
    s6 = 'for(i=0;i<4;i=i+1){print(i*i);};'
    # while + for combines
    s7 = 'x=4;while(x<30){x=x+3;print(x);};for(i=0;i<4;i=i+1){print(i*i);};'
    # moins unaire
    s8 = 'x=-3;print(x);y=-(2+3);print(y);'
    # parentheses dans les expressions
    s9 = 'a=2;b=3;print((a+b)*4);'
    # erreur : variable non initialisee
    s10 = 'print(z);'
    # erreur : division par zero
    s11 = 'x=5;y=0;print(x/y);'

    tests = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]
    for i, s in enumerate(tests, 1):
        variables.clear()
        print(f"\n{'-'*50}")
        print(f"  s{i} : {s}")
        print('-'*50)
        parser.parse(s)
