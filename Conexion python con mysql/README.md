# Sistema de Gestión de Biblioteca Hogareña con Python y MySQL

TP FINAL 
Materia: Tecnicas Avanzadas de Programacion
Estudiante: Alexis Sosa Casco
Sistema completo para gestionar una biblioteca hogareña usando Python y MySQL, con interfaz de menú interactivo.

## 📋 Descripción

Este proyecto implementa un sistema de gestión de biblioteca personal que permite:
- Gestionar el inventario de libros
- Organizar libros por categorías
- Registrar préstamos y devoluciones
- Consultar estadísticas de la biblioteca

Todo mediante una conexión segura a MySQL usando PyMySQL.

## 🚀 Instalación

### Requisitos Previos
- Python 3.7 o superior
- MySQL Server instalado y ejecutándose
- Base de datos MySQL creada

### Instalar Dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente
pip install pymysql python-dotenv
```

## ⚙️ Configuración de la Base de Datos

### 1. Crear la Base de Datos en MySQL

```sql
CREATE DATABASE nombre_base_datos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configurar Variables de Entorno

1. **Copia el archivo de ejemplo**:
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env`** con tus credenciales:
   ```env
   DB_HOST=localhost
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_NAME=nombre_base_datos
   DB_PORT=3306
   ```

   ⚠️ **IMPORTANTE**: Nunca subas el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

## 🔌 Conexión con MySQL

El proyecto utiliza **PyMySQL** para establecer la conexión con MySQL de forma segura.

### Archivos de Configuración

- **`config_database.py`**: Maneja la configuración y carga las variables de entorno desde `.env`
- **`conexion_pymysql.py`**: Contiene todas las funciones del sistema de biblioteca

### Estructura de la Conexión

```python
import pymysql
from config_database import get_pymysql_config

# Obtener configuración desde variables de entorno
config = get_pymysql_config()

# Establecer conexión
conexion = pymysql.connect(**config)
```

### Características de la Conexión

- ✅ Uso de variables de entorno para credenciales (seguro)
- ✅ Cierre automático de conexiones
- ✅ Manejo de errores robusto
- ✅ Consultas preparadas (prevención de SQL injection)
- ✅ Transacciones para operaciones críticas

## 📚 Sistema de Biblioteca Hogareña

### 🚀 Inicio Rápido

```bash
python conexion_pymysql.py
```

El sistema automáticamente:
1. Verifica la conexión a la base de datos MySQL
2. Crea la estructura de tablas necesarias (si no existen)
3. Inicializa categorías predeterminadas (Ficción, No Ficción, Ciencia, Historia, Biografía, Infantil)
4. Abre el menú interactivo

### 📋 Estructura de la Base de Datos

El sistema crea automáticamente las siguientes tablas:

#### Tabla `categorias`
- Organiza los libros por género/temática
- Campos: `id`, `nombre`, `descripcion`, `fecha_creacion`

#### Tabla `libros`
- Almacena información completa de cada libro
- Campos: `id`, `titulo`, `autor`, `isbn`, `editorial`, `año_publicacion`, `categoria_id`, `paginas`, `estado`, `ubicacion`, `notas`, `fecha_registro`
- Estados posibles: `Disponible`, `Prestado`, `Perdido`, `En reparación`
- Relación con `categorias` mediante clave foránea

#### Tabla `prestamos`
- Registra todos los préstamos realizados
- Campos: `id`, `libro_id`, `persona_prestamo`, `fecha_prestamo`, `fecha_devolucion_esperada`, `fecha_devolucion_real`, `estado`, `notas`
- Estados: `Prestado`, `Devuelto`, `Vencido`
- Relación con `libros` mediante clave foránea

### 🎯 Funcionalidades del Menú Interactivo

#### 1. 📖 Agregar Libro
Agrega nuevos libros a la biblioteca con información completa:
- Título y autor (obligatorios)
- ISBN, editorial, año de publicación (opcionales)
- Categoría, número de páginas, ubicación física (opcionales)
- Notas adicionales

#### 2. 📋 Listar Libros
Muestra todos los libros con opciones de filtrado:
- Todos los libros
- Solo disponibles
- Solo prestados
- Por categoría específica

#### 3. 🔍 Buscar Libro
Búsqueda flexible por:
- Título
- Autor
- ISBN

#### 4. ✏️ Actualizar Libro
Actualiza cualquier campo del libro de forma selectiva:
- Solo necesitas proporcionar los campos que deseas modificar
- Permite actualizar estado, ubicación, notas, etc.

#### 5. 🗑️ Eliminar Libro
Elimina un libro de la biblioteca:
- Requiere confirmación antes de eliminar
- Mantiene la integridad referencial de la base de datos

#### 6. 📂 Ver Categorías
Lista todas las categorías disponibles con sus descripciones.

#### 7. ➕ Agregar Categoría
Crea nuevas categorías para organizar mejor los libros.

#### 8. 📤 Prestar Libro
Registra un préstamo:
- Valida que el libro esté disponible
- Actualiza automáticamente el estado del libro a "Prestado"
- Permite establecer fecha de devolución esperada y notas

#### 9. 📥 Devolver Libro
Registra la devolución:
- Busca automáticamente el préstamo activo
- Actualiza el estado del libro a "Disponible"
- Registra la fecha real de devolución

#### 10. 📋 Ver Préstamos
Lista todos los préstamos con filtros:
- Todos los préstamos
- Solo préstamos activos
- Solo préstamos devueltos

#### 11. 📊 Estadísticas
Muestra un resumen completo de la biblioteca:
- Total de libros
- Libros por estado (Disponible, Prestado, etc.)
- Libros por categoría
- Total de categorías
- Préstamos activos

### 💻 Uso Programático

También puedes usar las funciones directamente desde Python sin el menú:

```python
from conexion_pymysql import (
    agregar_libro, listar_libros, buscar_libro,
    actualizar_libro, eliminar_libro,
    listar_categorias, agregar_categoria,
    prestar_libro, devolver_libro,
    listar_prestamos, estadisticas_biblioteca
)

# Ejemplo: Agregar un libro
agregar_libro(
    titulo="El Quijote",
    autor="Miguel de Cervantes",
    isbn="978-84-376-0494-7",
    editorial="Cátedra",
    año=1605,
    categoria_id=1,
    paginas=1200,
    ubicacion="Estante Principal"
)

# Ejemplo: Buscar libros
buscar_libro("Quijote")

# Ejemplo: Listar solo libros disponibles
listar_libros(estado="Disponible", mostrar_todos=False)

# Ejemplo: Prestar un libro
prestar_libro(libro_id=1, persona="Juan Pérez")

# Ejemplo: Ver estadísticas
estadisticas_biblioteca()
```

### 📝 Funciones Disponibles

Todas las funciones del sistema incluyen:
- ✅ Validación de datos de entrada
- ✅ Manejo robusto de errores
- ✅ Mensajes informativos de éxito/error
- ✅ Cierre automático de conexiones a la base de datos
- ✅ Uso de transacciones para operaciones críticas
- ✅ Consultas preparadas para seguridad

### 🎨 Características del Menú Interactivo

- **Interfaz intuitiva**: Menú numerado fácil de navegar
- **Validación de entrada**: Previene errores del usuario
- **Navegación clara**: Opciones bien organizadas
- **Feedback inmediato**: Mensajes claros de éxito o error
- **Pausa entre operaciones**: Permite leer resultados antes de continuar

## 🛡️ Buenas Prácticas de Seguridad

- ✅ **Variables de entorno**: Las credenciales nunca están en el código
- ✅ **Consultas preparadas**: Previene SQL injection en todas las consultas
- ✅ **Cierre de conexiones**: Todas las conexiones se cierran adecuadamente
- ✅ **Manejo de errores**: Errores manejados sin exponer información sensible
- ✅ **Transacciones**: Operaciones críticas usan transacciones

## 🐛 Solución de Problemas

### Error de conexión a MySQL

**Problema**: `Access denied for user...`
- Verifica que las credenciales en `.env` sean correctas
- Verifica que el usuario de MySQL tenga permisos en la base de datos
- Asegúrate de que MySQL esté ejecutándose

**Problema**: `Can't connect to MySQL server`
- Verifica que MySQL esté ejecutándose: `sudo systemctl status mysql` (Linux) o Services (Windows)
- Verifica el puerto en `.env` (por defecto 3306)
- Verifica que el host sea correcto (localhost o IP del servidor)

### Error de instalación de PyMySQL

```bash
# En Windows
pip install --upgrade pip
pip install pymysql

# En Linux/Mac
sudo apt-get install python3-dev  # Solo si hay errores de compilación
pip install pymysql
```

### Error al crear tablas

- Verifica que la base de datos existe y tienes permisos
- Verifica que no haya caracteres especiales en el nombre de la base de datos
- Revisa los logs de MySQL para más detalles

## 📁 Estructura del Proyecto

```
biblioteca-hogareña/
├── .env                    # Variables de entorno (NO subir al repositorio)
├── .env.example            # Plantilla de configuración
├── .gitignore              # Archivos excluidos de Git
├── README.md               # Esta documentación
├── requirements.txt        # Dependencias del proyecto
├── config_database.py      # Configuración de conexión a MySQL
└── conexion_pymysql.py     # Sistema principal de biblioteca
```

## 📝 Notas Importantes

- El archivo `.env` con tus credenciales **NO debe subirse** al repositorio Git
- El sistema crea automáticamente las tablas al ejecutarse por primera vez
- Las categorías iniciales se crean automáticamente si no existen
- Todas las conexiones se cierran automáticamente, incluso si hay errores

## 🔗 Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación
- **PyMySQL**: Biblioteca para conectar Python con MySQL
- **python-dotenv**: Manejo seguro de variables de entorno
- **MySQL**: Base de datos relacional

---

**Desarrollado como proyecto de gestión de biblioteca hogareña con conexión a MySQL**
