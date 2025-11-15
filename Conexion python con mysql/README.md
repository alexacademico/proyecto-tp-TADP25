# Conexión Python con MySQL

Este proyecto contiene ejemplos de cómo conectar Python con MySQL usando diferentes bibliotecas.

## 📚 Bibliotecas Disponibles

### 1. mysql-connector-python (Oficial de Oracle)
- **Ventajas**: Conector oficial, muy estable, soporte completo de MySQL
- **Desventajas**: Más pesado, requiere compilación en algunos sistemas
- **Archivo**: `conexion_mysql_connector.py`

### 2. PyMySQL (Pura Python)
- **Ventajas**: Ligera, fácil instalación, compatible con MySQLdb
- **Desventajas**: Menos optimizada para consultas complejas
- **Archivo**: `conexion_pymysql.py`

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar individualmente
pip install mysql-connector-python
# O
pip install pymysql
```

## ⚙️ Configuración

1. **Copia el archivo de configuración**:
   ```bash
cp .env.example .env
   ```

2. **Edita el archivo `.env`** con tus credenciales:
   ```
   DB_HOST=localhost
   DB_USER=administrador
   DB_PASSWORD=Devesencuando01.
   DB_NAME=clientes_datos
   DB_PORT=3306
   ```

## 📖 Uso Básico

### Con mysql-connector-python:
```python
import mysql.connector
from config_database import get_database_config

config = get_database_config()
conexion = mysql.connector.connect(**config)
```

### Con PyMySQL:
```python
import pymysql
from config_database import get_pymysql_config

config = get_pymysql_config()
conexion = pymysql.connect(**config)
```

## 🔧 Ejemplos Incluidos

1. **Conexión básica**: Establecer conexión y verificar
2. **Consultas SELECT**: Obtener datos de la base de datos
3. **Operaciones CRUD**: Crear, leer, actualizar y eliminar registros
4. **Manejo de errores**: Gestión adecuada de excepciones
5. **Configuración segura**: Uso de variables de entorno

## 📚 Sistema de Gestión de Biblioteca Hogareña

El archivo `conexion_pymysql.py` incluye un sistema completo para gestionar una biblioteca hogareña con interfaz de menú interactivo.

### 🚀 Inicio Rápido

```bash
python conexion_pymysql.py
```

El sistema automáticamente:
1. Verifica la conexión a la base de datos
2. Crea la estructura de tablas necesarias (si no existen)
3. Inicializa categorías predeterminadas
4. Abre el menú interactivo

### 📋 Estructura de la Base de Datos

El sistema crea las siguientes tablas:

- **`categorias`**: Para organizar libros por género/temática
- **`libros`**: Información completa de cada libro (título, autor, ISBN, editorial, año, páginas, estado, ubicación, etc.)
- **`prestamos`**: Registro de préstamos con fechas y estado

### 🎯 Funcionalidades del Menú

#### 1. 📖 Agregar Libro
- Permite agregar nuevos libros a la biblioteca
- Campos opcionales: ISBN, editorial, año, páginas, ubicación física, notas
- Asociación opcional con categorías existentes

#### 2. 📋 Listar Libros
- Muestra todos los libros o filtrados por:
  - Estado (Disponible, Prestado, Perdido, En reparación)
  - Categoría
- Muestra información completa de cada libro

#### 3. 🔍 Buscar Libro
- Búsqueda por título, autor o ISBN
- Muestra resultados con información relevante

#### 4. ✏️ Actualizar Libro
- Actualiza cualquier campo del libro
- Solo necesitas proporcionar los campos que deseas cambiar

#### 5. 🗑️ Eliminar Libro
- Elimina un libro de la biblioteca
- Requiere confirmación antes de eliminar

#### 6. 📂 Ver Categorías
- Lista todas las categorías disponibles con sus descripciones

#### 7. ➕ Agregar Categoría
- Crea nuevas categorías para organizar los libros

#### 8. 📤 Prestar Libro
- Registra un préstamo
- Actualiza automáticamente el estado del libro a "Prestado"
- Permite establecer fecha de devolución esperada y notas

#### 9. 📥 Devolver Libro
- Registra la devolución de un libro
- Actualiza automáticamente el estado del libro a "Disponible"
- Registra la fecha real de devolución

#### 10. 📋 Ver Préstamos
- Lista todos los préstamos o filtrados por estado:
  - Prestados (activos)
  - Devueltos
- Muestra información completa del préstamo y libro asociado

#### 11. 📊 Estadísticas
- Muestra un resumen completo de la biblioteca:
  - Total de libros
  - Libros por estado
  - Libros por categoría
  - Total de categorías
  - Préstamos activos

### 💻 Uso Programático

También puedes usar las funciones directamente desde Python:

```python
from conexion_pymysql import (
    agregar_libro, listar_libros, buscar_libro,
    actualizar_libro, eliminar_libro,
    listar_categorias, agregar_categoria,
    prestar_libro, devolver_libro,
    listar_prestamos, estadisticas_biblioteca
)

# Agregar un libro
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

# Buscar libros
buscar_libro("Quijote")

# Listar libros disponibles
listar_libros(estado="Disponible", mostrar_todos=False)

# Prestar un libro
prestar_libro(libro_id=1, persona="Juan Pérez")

# Ver estadísticas
estadisticas_biblioteca()
```

### 📝 Funciones Disponibles

Todas las funciones incluyen:
- ✅ Validación de datos de entrada
- ✅ Manejo de errores robusto
- ✅ Mensajes informativos
- ✅ Cierre automático de conexiones
- ✅ Transacciones seguras

### 🎨 Características del Menú Interactivo

- **Interfaz intuitiva**: Menú numerado fácil de usar
- **Validación de entrada**: Previene errores de usuario
- **Navegación clara**: Opciones bien organizadas
- **Feedback inmediato**: Mensajes de éxito/error claros
- **Pausa entre operaciones**: Permite leer los resultados antes de continuar

## 🛡️ Buenas Prácticas

- ✅ Siempre cerrar conexiones
- ✅ Usar variables de entorno para credenciales
- ✅ Manejar excepciones apropiadamente
- ✅ Usar consultas preparadas para evitar SQL injection
- ✅ Implementar pooling de conexiones para aplicaciones de producción

## 🐛 Solución de Problemas

### Error de conexión:
- Verificar que MySQL esté ejecutándose
- Comprobar credenciales
- Verificar que el puerto 3306 esté abierto

### Error de instalación:
```bash
# En Windows, puede necesitar:
pip install --upgrade pip
pip install mysql-connector-python

# En Linux/Mac, puede necesitar:
sudo apt-get install python3-dev libmysqlclient-dev
pip install mysql-connector-python
```

## 📝 Notas Adicionales

- Para aplicaciones de producción, considera usar un ORM como SQLAlchemy
- Para conexiones concurrentes, implementa un pool de conexiones
- Siempre usa transacciones para operaciones críticas


