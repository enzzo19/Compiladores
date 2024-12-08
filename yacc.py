import ply.yacc as yacc
from lex import tokens, lexer, errores_lexicos
errores_sintacticos = []
lenguaje_objeto = []
# Declaración de precedencia y asociatividad de los operadores
precedence = (
    ('left', 'TK_OPERATOR_EQUAL'),
    ('left', 'TK_OPERADORES')
)

# Definición de la gramática en una lista de tuplas
def p_S(t):
    '''S : TK_INICIO Instrucciones TK_FIN'''
    if len(errores_sintacticos) == 0 and len(errores_lexicos) == 0 :
        t[0] = True
        # print("Compilacion Exitosa")
    else:
        t[0] = False
        # print("Fallo al Compilar --> Corrije los errores")

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
        # print(f"Instruccion '{t[1]}' parseada correctamente")
        pass
    else:
         t[0] = None  # Evita que se quede sin valor


def p_DeclaracionTabla(t):
    '''DeclaracionTabla : TK_FORM TK_TABLE TK_IDENTIFIER TK_WITH TK_OPEN_BRACKET Campos TK_CLOSE_BRACKET TK_DOT'''
    t[0] = f"Tabla {t[3]}"  # Devuelve información sobre la declaración
    # print(f"Declaración de tabla '{t[3]}' parseada correctamente")
    campos_sql = ", ".join(t[6])
    lenguaje_objeto.append(f"CREATE TABLE {t[3]} ({campos_sql})")


def p_Campos(t):
    '''Campos : Campos TK_COMMA Campo
            | Campo'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]


def p_Campo(t):
    '''Campo : TK_IDENTIFIER TK_COLON Tipo'''
    t[0] = f"{t[1]} {t[3]}"  # Guarda el identificador y tipo

def p_Tipo(t):
    '''Tipo : TK_DECIMAL
          | TK_STRING
          | TK_DATETIME'''
    t[0] = t[1]  # Devuelve el tipo como resultado
    if t.slice[1].type == 'TK_STRING':
        t[0] = "VARCHAR(255)"
    elif t.slice[1].type == 'DECIMAL':
        t[0] = "DECIMAL(10, 2)"
    elif t.slice[1].type == 'TK_DATETIME':
        t[0] = "DATETIME"

def p_Seleccion(t):
    '''Seleccion : TK_QUERY ListaCampos TK_FROM TK_IDENTIFIER Filtro TK_DOT'''
    # print(f"Consulta '{t[2]}' de la tabla '{t[4]}' parseada correctamente")
    lenguaje_objeto.append(f"SELECT {t[2]} FROM {t[4]} WHERE {t[5]}")

def p_ListaCampos(t):
    '''ListaCampos : TK_IDENTIFIER TK_COMMA ListaCampos
                   | TK_IDENTIFIER'''
    if len(t) == 4:  # Caso 'TK_IDENTIFIER TK_COMMA ListaCampos'
         t[0] = f"{t[1]}, {t[3]}"
    else:  # Caso 'TK_IDENTIFIER'
        t[0] = t[1]


def p_Filtro(t):
    '''Filtro : TK_FILTER TK_BY Condicion'''
    if len(t) == 4:  # Caso con condición
        t[0] = t[3]
        # print("Filtro parseado correctamente")
    else:
        t[0] = None


def p_Condicion(t):
    '''Condicion : TK_IDENTIFIER TK_OPERADORES TK_IDENTIFIER
                 | TK_IDENTIFIER TK_OPERATOR_EQUAL TK_IDENTIFIER
                 | TK_IDENTIFIER TK_OPERADORES Valor
                 | TK_IDENTIFIER TK_OPERATOR_EQUAL Valor
                 | TK_IDENTIFIER TK_OPERATOR_EQUAL STR
                 | TK_IDENTIFIER TK_OPERADORES Expresion
                 | TK_IDENTIFIER TK_OPERATOR_EQUAL Expresion
                 '''
    # Convertir la condición en una cadena SQL válida
    t[0] = f"{t[1]} {t[2]} {t[3]}"
    # print(f"Condición '{t[1]} {t[2]} {t[3]}' parseada correctamente")


def p_Expresion(t):
    '''Expresion : Expresion TK_MAS Termino
                 | Expresion TK_MENOS Termino
                 | Termino'''
    if len(t) == 4:
        # Combina las partes de la operación en una cadena
        t[0] = f"{t[1]} {t[2]} {t[3]}"
    else:
        t[0] = t[1]

def p_Termino(t):
    '''Termino : Termino TK_MULT Factor
               | Termino TK_DIV Factor
               | Factor'''
    if len(t) == 4:
        # Combina las partes de la operación en una cadena
        t[0] = f"{t[1]} {t[2]} {t[3]}"
    else:
        t[0] = t[1]


def p_Factor(t):
    '''Factor : TK_PARAB Expresion TK_PARCI
              | Valor'''
    if len(t) == 4:
        t[0] = t[2]  # Eliminar los paréntesis
    else:
        t[0] = t[1]

def p_STR(t):
    '''STR : TK_STRING'''
    t[0] = t[1]

def p_Valor(t):
    '''Valor : TK_NUMBER'''
    t[0] = t[1]


def p_Actualizacion(t):
    '''Actualizacion : TK_ALTER TK_IDENTIFIER TK_COLUMN Asignaciones TK_WHERE Condicion TK_DOT'''
    t[0] = f"Actualizar {t[2]}"
    # Convertir las asignaciones en una cadena SQL válida
    asignaciones_sql = ", ".join([f"{asignacion[0]} = {asignacion[1]}" for asignacion in t[4]])
    # Agregar la condición parseada como una cadena SQL
    condicion_sql = t[6]
    lenguaje_objeto.append(f"UPDATE {t[2]} SET {asignaciones_sql} WHERE {condicion_sql}")
    # print(f"Actualización parseada correctamente: UPDATE {t[2]} SET {asignaciones_sql} WHERE {condicion_sql}")


def p_Asignaciones(t):
    '''Asignaciones : TK_IDENTIFIER TK_OPERATOR_EQUAL Expresion TK_COMMA Asignaciones
                    | TK_IDENTIFIER TK_OPERATOR_EQUAL Expresion'''
    if len(t) == 4:  # Caso de 'TK_IDENTIFIER = Expresion'
        t[0] = [(t[1], t[3])]
        # print(f"Asignación '{t[1]} = {t[3]}' parseada correctamente")
    elif len(t) == 6:  # Caso de 'TK_IDENTIFIER = Expresion , Asignaciones'
        t[0] = [(t[1], t[3])] + t[5]
        # print(f"Asignación '{t[1]} = {t[3]}' parseada correctamente")


def p_Eliminacion(t):
    '''Eliminacion : TK_DROP TK_IDENTIFIER TK_COMPLETELY TK_DOT'''
    # print(f"Eliminacion de la tabla '{t[2]}' parseada correctamente")
    lenguaje_objeto.append(f"DROP TABLE {t[2]}")

# Manejo de errores sintácticos
def p_error(t):
    if t:
        print(f"Error de sintaxis en la línea {t.lineno}, token inesperado '{t.value}'")
        errores_sintacticos.append(f"Error de sintaxis en la línea {t.lineno}, token inesperado '{t.value}'")
        t.lexer.skip(1)

# Crear el parser
parser = yacc.yacc()
if __name__ == "__main__":
    data = '''
    INICIO
    // Acá comienza el programa ejemplo
    FORM TABLE TABLE productos WITH [nombre:STRING, precio: DECIMAL].QUERY nombre, precio FROM productos FILTER BY precio > 100.
    // otro comentario
    ALTER ventas 50 COLUMN total = 110 + 2 * 5  WHERE nro_cliente = 10 * 2 + 5. DROP ventas COMPLETELY.
    FIN
    INICIO
    '''
    parser.parse(data)
