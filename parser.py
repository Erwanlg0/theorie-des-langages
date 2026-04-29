import ply.yacc as yacc

from lexer import tokens


# Memoire globale et table des fonctions.
variables = {}
functions = {}
scopes = [variables]


precedence = (
    ('left', 'INFERIEUR', 'SUPERIEUR', 'EGAL_EGAL'),
    ('left', 'PLUS', 'MOINS'),
    ('left', 'FOIS', 'DIVISE'),
    ('right', 'UMINUS'),
)


class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value


# --- GRAMMAIRE ---

def p_start(p):
    'start : instruction_list'
    p[0] = ('program', p[1])
    print("--- AST ---")
    print(p[0])
    print("--- EXECUTION ---")
    try:
        evalInst(p[0])
    except ReturnValue:
        print("Erreur : return utilise hors d'une fonction")


def p_instruction_list_single(p):
    'instruction_list : instruction'
    p[0] = [p[1]]


def p_instruction_list_multiple(p):
    'instruction_list : instruction_list instruction'
    p[0] = p[1] + [p[2]]


def p_block_empty(p):
    'block : LBRACE RBRACE'
    p[0] = []


def p_block_instructions(p):
    'block : LBRACE instruction_list RBRACE'
    p[0] = p[2]


def p_instruction_simple(p):
    'instruction : simple_statement POINT_VIRGULE'
    p[0] = p[1]


def p_simple_statement_assign(p):
    'simple_statement : id_list EGAL expression_list'
    if len(p[1]) == 1:
        p[0] = ('assign', p[1][0], p[3][0]) if len(p[3]) == 1 else ('multi_assign', p[1], p[3])
    else:
        p[0] = ('multi_assign', p[1], p[3])


def p_simple_statement_aug_assign(p):
    '''simple_statement : IDENTIFIANT PLUS_EGAL expression
                        | IDENTIFIANT MOINS_EGAL expression
                        | IDENTIFIANT FOIS_EGAL expression
                        | IDENTIFIANT DIVISE_EGAL expression'''
    p[0] = ('aug_assign', p[1], p[2], p[3])


def p_simple_statement_increment(p):
    'simple_statement : IDENTIFIANT PLUS_PLUS'
    p[0] = ('inc', p[1])


def p_simple_statement_declaration(p):
    'simple_statement : VAR declaration_list'
    p[0] = ('declare', p[2])


def p_instruction_print(p):
    'instruction : PRINT LPAREN expression_list RPAREN POINT_VIRGULE'
    p[0] = ('print', p[3])


def p_instruction_expression(p):
    'instruction : expression POINT_VIRGULE'
    p[0] = ('expr_stmt', p[1])


def p_instruction_if(p):
    'instruction : IF LPAREN expression RPAREN block'
    p[0] = ('if', p[3], p[5], [])


def p_instruction_if_else(p):
    'instruction : IF LPAREN expression RPAREN block ELSE block'
    p[0] = ('if', p[3], p[5], p[7])


def p_instruction_while(p):
    'instruction : WHILE LPAREN expression RPAREN block'
    p[0] = ('while', p[3], p[5])


def p_instruction_for(p):
    'instruction : FOR LPAREN for_part POINT_VIRGULE expression POINT_VIRGULE for_part RPAREN block'
    p[0] = ('for', p[3], p[5], p[7], p[9])


def p_instruction_function(p):
    'instruction : FUNCTION IDENTIFIANT LPAREN param_list_opt RPAREN block'
    p[0] = ('function', p[2], p[4], p[6])


def p_instruction_return_value(p):
    'instruction : RETURN expression POINT_VIRGULE'
    p[0] = ('return', p[2])


def p_instruction_return_empty(p):
    'instruction : RETURN POINT_VIRGULE'
    p[0] = ('return', ('nombre', 0))


def p_instruction_empty_semicolon(p):
    'instruction : POINT_VIRGULE'
    p[0] = ('empty',)


def p_for_part_statement(p):
    'for_part : simple_statement'
    p[0] = p[1]


def p_for_part_empty(p):
    'for_part : empty'
    p[0] = ('empty',)


def p_declaration_list_single(p):
    'declaration_list : declaration'
    p[0] = [p[1]]


def p_declaration_list_multiple(p):
    'declaration_list : declaration_list VIRGULE declaration'
    p[0] = p[1] + [p[3]]


def p_declaration_name(p):
    'declaration : IDENTIFIANT'
    p[0] = (p[1], ('nombre', 0))


def p_declaration_value(p):
    'declaration : IDENTIFIANT EGAL expression'
    p[0] = (p[1], p[3])


def p_id_list_single(p):
    'id_list : IDENTIFIANT'
    p[0] = [p[1]]


def p_id_list_multiple(p):
    'id_list : id_list VIRGULE IDENTIFIANT'
    p[0] = p[1] + [p[3]]


def p_param_list_opt_empty(p):
    'param_list_opt : empty'
    p[0] = []


def p_param_list_opt_values(p):
    'param_list_opt : param_list'
    p[0] = p[1]


def p_param_list_single(p):
    'param_list : IDENTIFIANT'
    p[0] = [p[1]]


def p_param_list_multiple(p):
    'param_list : param_list VIRGULE IDENTIFIANT'
    p[0] = p[1] + [p[3]]


def p_argument_list_opt_empty(p):
    'argument_list_opt : empty'
    p[0] = []


def p_argument_list_opt_values(p):
    'argument_list_opt : expression_list'
    p[0] = p[1]


def p_expression_list_single(p):
    'expression_list : expression'
    p[0] = [p[1]]


def p_expression_list_multiple(p):
    'expression_list : expression_list VIRGULE expression'
    p[0] = p[1] + [p[3]]


def p_expression_nombre(p):
    'expression : NOMBRE'
    p[0] = ('nombre', p[1])


def p_expression_chaine(p):
    'expression : CHAINE'
    p[0] = ('chaine', p[1])


def p_expression_identifiant(p):
    'expression : IDENTIFIANT'
    p[0] = ('var', p[1])


def p_expression_call(p):
    'expression : IDENTIFIANT LPAREN argument_list_opt RPAREN'
    p[0] = ('call', p[1], p[3])


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


def p_expression_uminus(p):
    'expression : MOINS expression %prec UMINUS'
    p[0] = ('uminus', p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    if p:
        raise SyntaxError(f"Erreur de syntaxe ligne {p.lineno} vers '{p.value}'")
    raise SyntaxError("Erreur de syntaxe a la fin du fichier")


parser = yacc.yacc()


# --- INTERPRETEUR ---

def reset_environment():
    variables.clear()
    functions.clear()
    scopes[:] = [variables]


def find_scope(name):
    for scope in reversed(scopes):
        if name in scope:
            return scope
    return None


def get_var(name):
    scope = find_scope(name)
    if scope is None:
        print(f"Erreur : Variable '{name}' non initialisee")
        return 0
    return scope[name]


def set_var(name, value):
    scope = find_scope(name)
    if scope is None:
        scope = scopes[-1]
    scope[name] = value


def declare_var(name, value):
    if name in scopes[-1]:
        print(f"Erreur : Variable '{name}' deja declaree dans ce scope")
    scopes[-1][name] = value


def evalExpr(t):
    if t[0] == 'nombre':
        return t[1]

    if t[0] == 'chaine':
        return t[1]

    if t[0] == 'var':
        return get_var(t[1])

    if t[0] == 'call':
        args = [evalExpr(arg) for arg in t[2]]
        return call_function(t[1], args)

    if t[0] == 'uminus':
        return -evalExpr(t[1])

    if t[0] in ('+', '-', '*', '/', '<', '>', '=='):
        left = evalExpr(t[1])
        right = evalExpr(t[2])
        try:
            if t[0] == '+':
                return left + right
            if t[0] == '-':
                return left - right
            if t[0] == '*':
                return left * right
            if t[0] == '/':
                if right == 0:
                    print("Erreur : Division par zero")
                    return 0
                return left / right
            if t[0] == '<':
                return left < right
            if t[0] == '>':
                return left > right
            if t[0] == '==':
                return left == right
        except TypeError:
            print(f"Erreur : operation impossible entre {type(left).__name__} et {type(right).__name__}")
            return 0

    print(f"Erreur interne : expression inconnue {t}")
    return 0


def eval_block(instructions):
    for instruction in instructions:
        evalInst(instruction)


def eval_simple_statement(t):
    if t[0] == 'assign':
        set_var(t[1], evalExpr(t[2]))

    elif t[0] == 'multi_assign':
        names = t[1]
        values = [evalExpr(expr) for expr in t[2]]
        if len(names) != len(values):
            print("Erreur : nombre de variables different du nombre de valeurs")
            return
        for name, value in zip(names, values):
            set_var(name, value)

    elif t[0] == 'aug_assign':
        current = get_var(t[1])
        value = evalExpr(t[3])
        op = t[2]
        if op == '+=':
            set_var(t[1], current + value)
        elif op == '-=':
            set_var(t[1], current - value)
        elif op == '*=':
            set_var(t[1], current * value)
        elif op == '/=':
            if value == 0:
                print("Erreur : Division par zero")
            else:
                set_var(t[1], current / value)

    elif t[0] == 'inc':
        set_var(t[1], get_var(t[1]) + 1)

    elif t[0] == 'declare':
        for name, expr in t[1]:
            declare_var(name, evalExpr(expr))

    elif t[0] == 'empty':
        return

    else:
        print(f"Erreur interne : instruction simple inconnue {t}")


def evalInst(t):
    if t[0] == 'program':
        eval_block(t[1])

    elif t[0] in ('assign', 'multi_assign', 'aug_assign', 'inc', 'declare', 'empty'):
        eval_simple_statement(t)

    elif t[0] == 'print':
        values = [evalExpr(expr) for expr in t[1]]
        print("calc >", *values)

    elif t[0] == 'expr_stmt':
        evalExpr(t[1])

    elif t[0] == 'if':
        if evalExpr(t[1]):
            eval_block(t[2])
        else:
            eval_block(t[3])

    elif t[0] == 'while':
        while evalExpr(t[1]):
            eval_block(t[2])

    elif t[0] == 'for':
        eval_simple_statement(t[1])
        while evalExpr(t[2]):
            eval_block(t[4])
            eval_simple_statement(t[3])

    elif t[0] == 'function':
        functions[t[1]] = (t[2], t[3])

    elif t[0] == 'return':
        raise ReturnValue(evalExpr(t[1]))

    else:
        print(f"Erreur interne : instruction inconnue {t}")


def call_function(name, args):
    if name not in functions:
        print(f"Erreur : Fonction '{name}' non definie")
        return 0

    params, body = functions[name]
    if len(params) != len(args):
        print(f"Erreur : Fonction '{name}' attend {len(params)} parametre(s), recu {len(args)}")
        return 0

    local_scope = dict(zip(params, args))
    scopes.append(local_scope)
    try:
        eval_block(body)
    except ReturnValue as returned:
        return returned.value
    finally:
        scopes.pop()

    return 0


def parse_source(source):
    try:
        return parser.parse(source)
    except SyntaxError as exc:
        print(exc)
        print("--- EXECUTION ANNULEE ---")
        return None


if __name__ == '__main__':
    tests = [
        ('base', 'x=4;x=x+3;print(x);'),
        ('while', 'x=0;while(x<3){print(x);x++;};'),
        ('for', 'for(i=0;i<4;i=i+1){print(i*i);};'),
        ('chaines_print', 'var nom="mini langage";print("Projet", nom, 13);'),
        ('multi_assign', 'a,b=2,3;print(a,b);a+=10;print(a);'),
        ('fonction_retour', 'function carre(x){return x*x;}print(carre(5));'),
        ('fonction_sans_retour', 'function bonjour(){print("bonjour");}bonjour();'),
        ('return_coupe_circuit', 'function test(){return 7;print(666);}print(test());'),
        ('recursion_terminale', 'function fact(n,acc){if(n==0){return acc;}else{return fact(n-1,acc*n);}}print(fact(5,1));'),
        ('erreur_variable', 'print(inconnue);'),
        ('erreur_syntaxe', 'for(i=0;i<3;i=i+1;){print(i);};'),
    ]

    for name, source in tests:
        reset_environment()
        print(f"\n{'-' * 50}")
        print(f"  {name} : {source}")
        print('-' * 50)
        parse_source(source)
