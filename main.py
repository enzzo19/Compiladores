import os
from yacc import parser, lenguaje_objeto, lexer, errores_lexicos, errores_sintacticos

def listar_archivos(carpeta):
    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    return archivos

def seleccionar_archivo(archivos):
    print("\nSeleccione un archivo para traducir:")
    for i, archivo in enumerate(archivos):
        print(f"{i + 1}. {archivo}")
    print(f"{len(archivos) + 1}. Salir")

    while True:
        try:
            seleccion = int(input("Ingrese el número del archivo deseado (o seleccione 'Salir' para salir): ")) - 1
            if seleccion == len(archivos):
                return None
            elif 0 <= seleccion < len(archivos):
                return archivos[seleccion]
            else:
                print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

def compilar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            print("Compilando el archivo...")
            errores = []
            errores_lexicos = []
            errores_sintacticos = []
            lexer.lineno = 1
            codigo = archivo.read()
            resultado = parser.parse(codigo)
            errores = errores_lexicos + errores_sintacticos
            if resultado and len(errores) == 0:
                carpeta_salida = "salidas"
                os.makedirs(carpeta_salida, exist_ok=True)
                
                nombre_salida = os.path.join(carpeta_salida, os.path.splitext(os.path.basename(nombre_archivo))[0] + ".sql")
                
                with open(nombre_salida, 'w') as salida:
                    for instruccion in lenguaje_objeto:
                        salida.write(instruccion + ";\n")
                
                print(f"\nCompilación exitosa. Lenguaje Objeto generado y guardado en '{nombre_salida}'.")
            else:
                #print("\n".join(errores))
                print("Fallo al Compilar --> Corrije los errores")
    except FileNotFoundError:
        print(f"Archivo '{nombre_archivo}' no encontrado.")

if __name__ == "__main__":
    carpeta_entrada = "entradas"
    
    while True:
        archivos = listar_archivos(carpeta_entrada)
        if archivos:
            archivo_seleccionado = seleccionar_archivo(archivos)
            if archivo_seleccionado is None:
                print("Salida del programa.")
                break
            
            archivo_entrada = os.path.join(carpeta_entrada, archivo_seleccionado)
            
            compilar_archivo(archivo_entrada)
            break
        else:
            print("No se encontraron archivos en la carpeta 'entradas'.")
            break
