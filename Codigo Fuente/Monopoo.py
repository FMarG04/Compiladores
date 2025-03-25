# -*- coding: utf-8 -*-

import ply.lex as lex

# Lista de tokens
tokens = (
    'OPNUM', 'OPCONDICIONAL', 'OPLOGICO', 'LITERAL', 'TIPODATO', 'ID', 'DATOS',
    'PARIZQUIERDO', 'PARDERECHO', 'PBRESERVADA'
)

# Palabras reservadas
reserved = {
    'si': 'PBRESERVADA', 'para': 'PBRESERVADA', 'mientras': 'PBRESERVADA',
    'imprimir': 'PBRESERVADA', 'entero': 'TIPODATO', 'texto': 'TIPODATO',
    'decimal': 'TIPODATO', 'definir': 'PBRESERVADA', 'retornar': 'PBRESERVADA',
    'sino': 'PBRESERVADA', 'incremento': 'PBRESERVADA', 'romper': 'PBRESERVADA',
    'en': 'PBRESERVADA', 'y': 'OPLOGICO', 'o': 'OPLOGICO'
}

# Expresiones regulares para tokens simples
t_OPNUM = r'\+|\-|\*|\/|\*\*'
t_OPCONDICIONAL = r'==|<=|>=|!='
t_OPLOGICO = r'y|o'
t_LITERAL = r'\"([^\\\n]|(\\.))*?\"'
t_PARIZQUIERDO = r'\('
t_PARDERECHO = r'\)'

# Expresión regular con acción para identificar números
def t_DATOS(t):
    r'-?\d+(\.\d+)?(e-?\d+)?'
    t.value = float(t.value) if '.' in t.value or 'e' in t.value else int(t.value)
    return t

# Expresión regular con acción para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in ('y', 'o'):
        t.type = 'OPLOGICO'
    else:
        t.type = reserved.get(t.value.lower(), 'ID')  # Verifica si es palabra reservada
    return t

# Manejo de espacios y saltos de línea
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Error: Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Pruebas de código en MonoPoo
data = '''
Imprimir("Hola Mundo")
Para(X en 6 Incremento 2)
    Imprimir("Bucle")
    Para(J en 5)
        Imprimir(J)
Entero factorial(Entero n)
    Si(n == 0 o n == 1)
        Retornar 1
    Sino
        Retornar n * factorial(n - 1)
'''

# Alimentar el lexer con los datos
lexer.input(data)

lista_tokens = []

# Tokenización
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
    lista_tokens.append({ 'type': tok.type, 'value': tok.value, 'line': tok.lineno, 'column': tok.lexpos })
