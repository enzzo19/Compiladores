import ply.lex as lex
errores_lexicos = []

# Diccionario de palabras reservadas
reserved = {
    'inicio': 'TK_INICIO',
    'fin': 'TK_FIN',
    'query': 'TK_QUERY',
    'from': 'TK_FROM',
    'filter': 'TK_FILTER',
    'by': 'TK_BY',
    'form': 'TK_FORM',
    'table': 'TK_TABLE',
    'with': 'TK_WITH',
    'alter': 'TK_ALTER',
    'column': 'TK_COLUMN',
    'where': 'TK_WHERE',
    'drop': 'TK_DROP',
    'completely': 'TK_COMPLETELY',
    'decimal': 'TK_DECIMAL',
    'string': 'TK_STRING',
    'datetime': 'TK_DATETIME',
    'when': 'TK_WHEN'
}

# Lista de tokens
tokens = [
    'TK_DOT',
    'TK_COMMA',
    'TK_COLON',
    'TK_OPEN_BRACKET',
    'TK_CLOSE_BRACKET',
    'TK_IDENTIFIER',
    'TK_NUMBER',
    'TK_COMMENT',
    'TK_OPERATOR_EQUAL',
    'TK_OPERADORES',
    'TK_MAS',
    'TK_MENOS',
    'TK_MULT',
    'TK_DIV', 
    'TK_PARAB',
    'TK_PARCI'
] + list(reserved.values())

# Expresiones regulares para los tokens
t_TK_MAS = r'\+'
t_TK_MENOS = r'\-'
t_TK_MULT = r'\*'
t_TK_DIV = r'\/'
t_TK_DOT = r'\.'
t_TK_COMMA = r','
t_TK_COLON = r':'
t_TK_OPEN_BRACKET = r'\['
t_TK_CLOSE_BRACKET = r'\]'
t_TK_OPERATOR_EQUAL = r'(?<![<>!])='
t_TK_OPERADORES = r'(<=|>=|<|>|!=)'
t_TK_COMMENT = r'//.*'
t_TK_STRING = r"'[a-zA-Z]*'"
t_TK_PARAB = r"\("
t_TK_PARCI = r"\)"


def t_TK_NUMBER(t):
    r'(\+|-)?\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Expresiones para identificadores y literal
def t_TK_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    valor_minuscula = t.value.lower()
    t.type = reserved.get(valor_minuscula, 'TK_IDENTIFIER')
    return t


def t_COMMENT(t):
    r'//.*'
    pass

# Regla de ignorar espacios y tabulaciones
t_ignore = ' \t'

# Regla para manejar saltos de línea y obtener el número de línea
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

# Función para manejar errores léxicos
def t_error(t):
    print(f"Error léxico en la línea {t.lineno}: caracter inesperado '{t.value[0]}'")
    errores_lexicos.append(f"Error léxico en la línea {t.lineno}: caracter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Función de prueba para ver cómo se tokeniza una cadena
if __name__ == "__main__":
    # Este ejemplo marca el error de tokens no conocidos
    data = '''
    INICIO
    // comentario
    FORM TABLE casas WITH [numero : DECIMAL, direccion : STRING].
    {}
    QUERY numero, direccion FROM casas FILTER BY numero = 10 + (5 * 4).
    ALTER casas COLUMN numero = -15 + (2 * 2) WHERE direccion = 'Autodromo'.
    DROP casas COMPLETELY.
    FIN
    '''
    lexer.input(data)
    for token in lexer:
        print(token)
