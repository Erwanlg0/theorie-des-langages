import ply.yacc as yacc
from lexer import tokens

# La mémoire 
variables = {}

# Ordre de priorité des opérations
precedence = (
    ('left', 'INFERIEUR', 'SUPERIEUR', 'EGAL_EGAL'),
    ('left', 'PLUS', 'MOINS'),
    ('left', 'FOIS', 'DIVISE'),
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


def p_instruction_for(p):
    'instruction : FOR LPAREN instruction expression POINT_VIRGULE instruction RPAREN LBRACE bloc RBRACE'
    # p[3] = initialisation
    # p[4] = condition
    # p[6] = incrémentation
    # p[9] = le bloc à répéter
    p[0] = ('for', p[3], p[4], p[6], p[9])

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
    data = "x=4;while(x<30){x=x+3;print(x);};for(i=0;i<4;i=i+1;){print(i*i);};"
    parser.parse(data)