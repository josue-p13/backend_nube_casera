# Nube Casera Backend

Un servidor backend desarrollado con FastAPI que proporciona servicios API para una "nube casera" permitiendo la gestión de archivos y usuarios. Este proyecto funciona como un sistema de almacenamiento de archivos personal accesible a través de una API RESTful.

## Características

- Autenticación de usuarios mediante MongoDB
- Exploración de directorios con rutas seguras
- Subida de archivos de imágenes
- Creación de carpetas
- Visualización de imágenes
- Sistema de rutas protegidas

## Estructura del Proyecto

```
Back_Fast/
├── back.py                # Archivo principal con la configuración de FastAPI
├── buscar_base.py         # Funciones para autenticación de usuarios
├── mongo_con.py           # Configuración de conexión a MongoDB
├── rutas_archivos.py      # Endpoints para explorar y acceder a archivos
├── rutas_gestion.py       # Endpoints para gestionar archivos y carpetas
└── rutas_usuario.py       # Endpoints para gestión de usuarios
```

## Requisitos

- Python 3.13.2
- MongoDB Atlas (cuenta y cluster)
- Los paquetes listados en `requirements.txt`

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/nube-casera.git
cd nube-casera
```

### 2. Configurar un entorno virtual

```bash
# Crear entorno virtual
python -m venv env

# Activar el entorno virtual
# En Windows:
env\Scripts\activate
# En Linux/Mac:
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo requirements.txt (si no existe)

Este es el contenido que debe tener el archivo `requirements.txt`:

```
fastapi>=0.115.0
uvicorn>=0.28.0
pymongo>=4.6.1
python-multipart>=0.0.9
pydantic>=2.5.0
certifi>=2023.11.17
email-validator>=2.0.0
```

## Configuración

### Base de datos MongoDB

Edita el archivo `mongo_con.py` para configurar tu propia conexión a MongoDB:

```python
uri = "mongodb+srv://tu-usuario:tu-contraseña@tu-cluster.mongodb.net/?retryWrites=true&w=majority"
```

### Rutas de directorios

Modifica la función `retorno_path()` en los archivos `rutas_archivos.py`, `rutas_gestion.py` y `rutas_usuario.py` para configurar las rutas de tu sistema:

```python
def retorno_path(opcion):
    match opcion:
        case "usuario1":
            return "/ruta/a/tu/directorio1"
        case "usuario2":
            return "/ruta/a/tu/directorio2"
        # Añadir más usuarios y rutas según sea necesario
        case _:
            raise HTTPException(status_code=404, detail="User path not found")
```

## Ejecución

### Iniciar el servidor

```bash
# Navega al directorio Back_Fast
cd Back_Fast

# Inicia el servidor con uvicorn
uvicorn back:app --reload

# Para especificar un host y puerto
uvicorn back:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en `http://localhost:8000` por defecto.

### Documentación de la API

Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación interactiva de la API:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints principales

- **POST /tomar_datos/**: Autenticación de usuarios
- **GET /browse**: Explorar directorios
- **GET /media/{user}/{file_path}**: Obtener archivos multimedia
- **POST /create_folder/{user}**: Crear carpetas
- **POST /upload/{user}**: Subir archivos

## Consideraciones de seguridad

1. **Credenciales de MongoDB**: Nunca subas tu archivo `mongo_con.py` con las credenciales reales al repositorio. Usa variables de entorno o un archivo `.env` excluido del repositorio.

2. **Rutas del sistema**: Las rutas definidas en `retorno_path()` son específicas del sistema. Cada persona que clone este repositorio debe adaptarlas a su propia estructura de directorios.

3. **Extensiones permitidas**: Por defecto, solo se permiten los siguientes formatos de imagen: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`. Modifica la variable `extensiones_img` en los archivos correspondientes si necesitas permitir otros formatos.

## Problemas comunes

- **Error de conexión a MongoDB**: Verifica que tu URI de conexión sea correcta y que tu IP esté en la lista blanca de MongoDB Atlas.
- **Errores de permisos**: Asegúrate de que las rutas especificadas en `retorno_path()` existan y sean accesibles.
- **Problemas con subpaths**: La API está diseñada para prevenir accesos fuera del directorio base mediante normalización de rutas.

## Contribuir

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Haz push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo [tu licencia elegida] - ver el archivo LICENSE para detalles.
