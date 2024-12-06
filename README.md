Paso 0. Abrir la terminal desde el directorio del repo

Ejecuta el siguiente comando para crear el entorno virtual:

```bash
python -m venv venv
```

Paso 1. Activa el entorno virtual:

En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:
```bash
source venv/bin/activate
```

Se deberia ver como
```bash
 (venv) /tu_path> $ 
```


Paso 2. Usar `requirements.txt` para Instalar Dependencias
Si necesitas instalar todas las dependencias listadas en el archivo `requirements.txt`, ejecuta:

```bash
pip install -r requirements.txt
```

Paso 3. Para desactivar el entorno virtual:

```bash
deactivate 
```
