import ply.yacc as yacc
from lex import tokens


lenguaje_objeto = []

# Declaración de precedencia y asociatividad de los operadores (si es necesario)
precedence = (
    ('left', 'TK_OR'),
    ('left', 'TK_AND'),
    ('left', 'TK_OPERADORES'),
    ('left', 'TK_OPERATOR_EQUAL'),
)

# Definición de la gramática en una lista de tuplas
def p_S(t):
    '''S : TK_INICIO Instrucciones TK_FIN'''
    t[0] = True
    print("\nCompilación exitosa.\n")

def p_Instrucciones(t):
    '''Instrucciones : Instruccion 
                     | Instrucciones Instruccion'''
    pass  # No se hace nada si es una instrucción vacía

def p_Instruccion(t):
    '''Instruccion : DeclaracionTabla
                 | Seleccion
                 | Actualizacion
                 | Eliminacion '''
    if t[1] is not None:
        print(f"Instruccion '{t[1]}' parseada correctamente")
    else:
        print("Error: t[1] es None")


def p_DeclaracionTabla(t):
    '''DeclaracionTabla : TK_FORM TK_TABLE TK_IDENTIFIER TK_WITH TK_OPEN_BRACKET Campos TK_CLOSE_BRACKET TK_DOT'''
    t[0] = f"Tabla {t[3]}"  # Devuelve información sobre la declaración
    print(f"Declaración de tabla '{t[3]}' parseada correctamente")


def p_Campos(t):
    '''Campos : Campo TK_COMMA Campos
            | Campo'''
    if len(t) == 4:  # Caso de 'Campo TK_COMMA Campos'
        pass  # No se necesita hacer nada en este caso
    elif len(t) == 2:  # Caso de solo 'Campo'
        print(f"Campo '{t[1][0]}' con tipo '{t[1][1]}' parseado correctamente")

def p_Campo(t):
    '''Campo : TK_IDENTIFIER TK_COLON Tipo'''
    t[0] = (t[1], t[3])  # Guarda el identificador y tipo

def p_Tipo(t):
    '''Tipo : TK_DECIMAL
          | TK_STRING
          | TK_DATETIME'''
    t[0] = t[1]  # Devuelve el tipo como resultado

def p_Seleccion(t):
    '''Seleccion : TK_QUERY ListaCampos TK_FROM TK_IDENTIFIER Filtro TK_DOT'''
    print(f"Consulta '{t[2]}' de la tabla '{t[4]}' parseada correctamente")

def p_ListaCampos(t):
    '''ListaCampos : TK_IDENTIFIER TK_COMMA ListaCampos
                   | TK_IDENTIFIER'''
    if len(t) == 4:  # Caso 'TK_IDENTIFIER TK_COMMA ListaCampos'
        t[0] = [t[1]] + t[3]
    else:  # Caso 'TK_IDENTIFIER'
        t[0] = [t[1]]


def p_Filtro(t):
    '''Filtro : TK_FILTER TK_BY Condicion'''
    if len(t) == 4:  # Caso con condición
        t[0] = t[3]
        print("Filtro parseado correctamente")
    else:
        t[0] = None


def p_Condicion(t):
    '''Condicion : TK_IDENTIFIER TK_OPERADORES TK_IDENTIFIER
               | TK_IDENTIFIER TK_OPERADORES Valor'''
    print(f"Condicion '{t[1]} {t[2]} {t[3]}' parseada correctamente")

def p_Valor(t):
    '''Valor : TK_NUMBER
           | TK_STRING'''
    t[0] = t[1]  # Devuelve el valor como resultado

def p_Actualizacion(t):
    '''Actualizacion : TK_ALTER TK_IDENTIFIER TK_COLUMN Asignaciones TK_WHERE Condicion TK_DOT'''
    t[0] = f"Actualizar {t[2]}"
    print(f"Actualización de la tabla '{t[2]}' parseada correctamente")


def p_Asignaciones(t):
    '''Asignaciones : TK_IDENTIFIER TK_OPERATOR_EQUAL Valor TK_COMMA Asignaciones
                  | TK_IDENTIFIER TK_OPERATOR_EQUAL Valor'''
    if len(t) == 4:  # Caso de 'TK_IDENTIFIER TK_OPERATOR_EQUAL Valor'
        print(f"Asignación '{t[1]} = {t[3]}' parseada correctamente")
    elif len(t) == 6:  # Caso de 'TK_IDENTIFIER TK_OPERATOR_EQUAL Valor TK_COMMA Asignaciones'
        pass  # No se necesita hacer nada adicional

def p_Eliminacion(t):
    '''Eliminacion : TK_DROP TK_IDENTIFIER TK_COMPLETELY TK_DOT'''
    print(f"Eliminacion de la tabla '{t[2]}' parseada correctamente")


# Manejo de errores sintácticos
def p_error(t):
    if t:
        print(f"Error de sintaxis en la línea {t.lineno - 1}, token inesperado '{t.value}'")
    else:
        print("Error de sintaxis: no se pudo identificar el token")


# Crear el parser
# Asegúramos que el analizador use el seguimiento de líneas de la entrada léxica:
parser = yacc.yacc(debug=True, write_tables=False, errorlog=yacc.NullLogger())

# Ejemplo de prueba
if __name__ == "__main__":
    
    data = '''
    INICIO
    FORM TABLE ejemplo WITH [campo1 : DECIMAL, campo2 : STRING].
    QUERY campo1, campo2 FROM ejemplo FILTER BY campo1 > 10.
    ALTER ejemplo COLUMN campo1 = 15 WHERE campo2 = 'valor'.
    DROP ejemplo COMPLETELY.
    FIN
    '''
    parser.parse(data)
    """
    data = '''
    INICIO
    FORM TABLE ejemplo WITH [campo1 : DECIMAL, campo2 : STRING].
    QUERY campo1, campo2 FROM ejemplo FILTER BY campo1 > 5.
    ALTER ejemplo COLUMN campo1 = 15 WHERE campo2 = 'valor'.
    DROP ejemplo COMPLETELY.
    FIN
    '''
    parser.parse(data)
    """
