import ply.lex as lex

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
    'when': 'TK_WHEN',
    'and': 'TK_AND',
    'or': 'TK_OR',
    'not':'TK_NOT',
    'if': 'TK_IF',
    'else': 'TK_ELSE'
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
    'TK_OPERADORES'
] + list(reserved.values())

# Expresiones regulares para los tokens
t_TK_DOT = r'\.'
t_TK_COMMA = r','
t_TK_COLON = r':'
t_TK_OPEN_BRACKET = r'\['
t_TK_CLOSE_BRACKET = r'\]'
t_TK_OPERATOR_EQUAL = r'='
t_TK_OPERADORES = r'(<=|>=|<|>|=)'
t_TK_COMMENT = r'//.*'
t_TK_NUMBER = r'(\+|-)?\d+(\.\d+)?'
t_TK_STRING = r"'[a-zA-Z0-9!¡¿?_@-]*'"

# Expresiones para identificadores y literal

def t_TK_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    valor_minuscula = t.value.lower()
    t.type = reserved.get(valor_minuscula, 'TK_IDENTIFIER')
    return t

# Regla de ignorar espacios y tabulaciones
t_ignore = ' \t'

# Regla para manejar saltos de línea y obtener el número de línea
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

# Función para manejar errores léxicos
def t_error(t):
    print(f"Error léxico en la línea {t.lineno}: caracter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Función de prueba para ver cómo se tokeniza una cadena
if __name__ == "__main__":
    data = '''
    INICIO
    // comentario
    FORM TABLE casas WITH [numero : DECIMAL, direccion : STRING].
    {}
    QUERY numero, direccion FROM casas FILTER BY numero = 10.
    ALTER casas COLUMN numero = 15 WHERE direccion = 'Autodromo'.
    DROP casas COMPLETELY.
    FIN
    '''
    lexer.input(data)
    for token in lexer:
        print(token)
