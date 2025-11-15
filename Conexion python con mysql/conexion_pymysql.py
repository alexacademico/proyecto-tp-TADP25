"""
Ejemplo de conexión Python con MySQL usando PyMySQL
PyMySQL es una biblioteca pura de Python para MySQL
"""
import os
import pymysql
from config_database import get_pymysql_config
from pymysql import Error


def conectar_pymysql():
    """
    Función para establecer conexión con MySQL usando PyMySQL
    """
    # Configuración de la conexión desde archivo .env
    config = get_pymysql_config()
    
    conexion = None
    cursor = None
    
    try:
        # Establecer la conexión
        conexion = pymysql.connect(**config)
        
        if conexion.open:
            print("✅ Conexión exitosa a MySQL con PyMySQL")
            
            # Obtener información del servidor
            cursor = conexion.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 Versión de MySQL: {version[0]}")
            
            # Ejemplo de consulta simple
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("🗄️ Bases de datos disponibles:")
            for db in databases:
                print(f"   - {db[0]}")
                
    except Error as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        
    finally:
        # Cerrar cursor y conexión
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()
            print("🔒 Conexión cerrada")

def ejecutar_consulta_pymysql(consulta, parametros=None):
    """
    Función para ejecutar consultas SQL con PyMySQL
    """
    config = get_pymysql_config()
    
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Ejecutar consulta
        if parametros:
            cursor.execute(consulta, parametros)
        else:
            cursor.execute(consulta)
            
        # Si es una consulta SELECT, obtener resultados
        if consulta.strip().upper().startswith('SELECT'):
            resultados = cursor.fetchall()
            return resultados
        else:
            # Para INSERT, UPDATE, DELETE, hacer commit
            conexion.commit()
            return f"Consulta ejecutada. Filas afectadas: {cursor.rowcount}"
            
    except Error as e:
        print(f"❌ Error al ejecutar consulta: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def ejemplo_crud_pymysql():
    """
    Ejemplo completo de operaciones CRUD con PyMySQL
    """
    config = get_pymysql_config()
    
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Crear tabla de ejemplo
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            edad INT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(crear_tabla)
        print("✅ Tabla 'usuarios' creada o ya existe")
        
        # INSERT - Crear usuario
        insert_query = "INSERT INTO usuarios (nombre, email, edad) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, ("Juan Pérez", "juan@email.com", 25))
        conexion.commit()
        print("✅ Usuario insertado")
        
        # SELECT - Leer usuarios
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        print("📋 Usuarios en la base de datos:")
        for usuario in usuarios:
            print(f"   ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}, Edad: {usuario[3]}")
        
        # UPDATE - Actualizar usuario
        update_query = "UPDATE usuarios SET edad = %s WHERE email = %s"
        cursor.execute(update_query, (26, "juan@email.com"))
        conexion.commit()
        print("✅ Usuario actualizado")
        
        # DELETE - Eliminar usuario
        delete_query = "DELETE FROM usuarios WHERE email = %s"
        cursor.execute(delete_query, ("juan@email.com",))
        conexion.commit()
        print("✅ Usuario eliminado")
        
    except Error as e:
        print(f"❌ Error en operaciones CRUD: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def crear_estructura_biblioteca():
    """
    Crea la estructura completa de la base de datos para la biblioteca hogareña
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # 1. Crear tabla de categorías
        crear_categorias = """
        CREATE TABLE IF NOT EXISTS categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(crear_categorias)
        print("✅ Tabla 'categorias' creada")
        
        # 2. Crear tabla de libros
        crear_libros = """
        CREATE TABLE IF NOT EXISTS libros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            autor VARCHAR(200) NOT NULL,
            isbn VARCHAR(20) UNIQUE,
            editorial VARCHAR(100),
            año_publicacion INT,
            categoria_id INT,
            paginas INT,
            estado ENUM('Disponible', 'Prestado', 'Perdido', 'En reparación') DEFAULT 'Disponible',
            ubicacion VARCHAR(100),
            notas TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
            INDEX idx_titulo (titulo),
            INDEX idx_autor (autor),
            INDEX idx_estado (estado)
        )
        """
        cursor.execute(crear_libros)
        print("✅ Tabla 'libros' creada")
        
        # 3. Crear tabla de préstamos (opcional)
        crear_prestamos = """
        CREATE TABLE IF NOT EXISTS prestamos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            libro_id INT NOT NULL,
            persona_prestamo VARCHAR(100) NOT NULL,
            fecha_prestamo DATE NOT NULL,
            fecha_devolucion_esperada DATE,
            fecha_devolucion_real DATE,
            estado ENUM('Prestado', 'Devuelto', 'Vencido') DEFAULT 'Prestado',
            notas TEXT,
            FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
            INDEX idx_persona (persona_prestamo),
            INDEX idx_estado (estado)
        )
        """
        cursor.execute(crear_prestamos)
        print("✅ Tabla 'prestamos' creada")
        
        # Insertar algunas categorías de ejemplo
        categorias_ejemplo = [
            ("Ficción", "Novelas y literatura de ficción"),
            ("No Ficción", "Libros informativos y educativos"),
            ("Ciencia", "Libros de ciencia y tecnología"),
            ("Historia", "Libros históricos"),
            ("Biografía", "Biografías y autobiografías"),
            ("Infantil", "Libros para niños")
        ]
        
        insert_categoria = "INSERT IGNORE INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        cursor.executemany(insert_categoria, categorias_ejemplo)
        print("✅ Categorías de ejemplo insertadas")
        
        conexion.commit()
        print("\n🎉 Estructura de biblioteca creada exitosamente!")
        print("\n📚 Tablas creadas:")
        print("   - categorias: Para organizar libros por género")
        print("   - libros: Información de cada libro")
        print("   - prestamos: Registro de préstamos (opcional)")
        
    except Error as e:
        print(f"❌ Error al crear estructura: {e}")
        conexion.rollback()
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

# ============================================
# FUNCIONES ÚTILES PARA LA BIBLIOTECA
# ============================================

def agregar_libro(titulo, autor, isbn=None, editorial=None, año=None, categoria_id=None, paginas=None, ubicacion=None, notas=None):
    """
    Agrega un nuevo libro a la biblioteca
    
    Args:
        titulo: Título del libro (requerido)
        autor: Autor del libro (requerido)
        isbn: ISBN del libro (opcional)
        editorial: Editorial (opcional)
        año: Año de publicación (opcional)
        categoria_id: ID de la categoría (opcional)
        paginas: Número de páginas (opcional)
        ubicacion: Ubicación física del libro (opcional)
        notas: Notas adicionales (opcional)
    
    Returns:
        ID del libro insertado o None si hay error
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        insert_query = """
        INSERT INTO libros (titulo, autor, isbn, editorial, año_publicacion, categoria_id, paginas, ubicacion, notas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (titulo, autor, isbn, editorial, año, categoria_id, paginas, ubicacion, notas))
        conexion.commit()
        libro_id = cursor.lastrowid
        print(f"✅ Libro '{titulo}' agregado exitosamente (ID: {libro_id})")
        return libro_id
    except Error as e:
        print(f"❌ Error al agregar libro: {e}")
        conexion.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def listar_libros(estado=None, categoria_id=None, mostrar_todos=True):
    """
    Lista todos los libros, opcionalmente filtrados por estado o categoría
    
    Args:
        estado: Filtrar por estado ('Disponible', 'Prestado', 'Perdido', 'En reparación')
        categoria_id: Filtrar por ID de categoría
        mostrar_todos: Si es True, muestra todos los libros sin filtros
    
    Returns:
        Lista de tuplas con información de los libros
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        query = """
        SELECT l.id, l.titulo, l.autor, l.isbn, l.editorial, l.año_publicacion, 
               l.paginas, l.estado, l.ubicacion, c.nombre as categoria
        FROM libros l
        LEFT JOIN categorias c ON l.categoria_id = c.id
        WHERE 1=1
        """
        params = []
        
        if not mostrar_todos:
            if estado:
                query += " AND l.estado = %s"
                params.append(estado)
            if categoria_id:
                query += " AND l.categoria_id = %s"
                params.append(categoria_id)
        
        query += " ORDER BY l.titulo"
        
        cursor.execute(query, params if params else None)
        libros = cursor.fetchall()
        
        print(f"\n📚 Libros encontrados: {len(libros)}")
        print("-" * 80)
        for libro in libros:
            print(f"   [{libro[0]}] {libro[1]}")
            print(f"       Autor: {libro[2]} | Estado: {libro[7]} | Categoría: {libro[9] or 'Sin categoría'}")
            if libro[3]:
                print(f"       ISBN: {libro[3]}")
            if libro[4]:
                print(f"       Editorial: {libro[4]}")
            if libro[5]:
                print(f"       Año: {libro[5]}")
            if libro[6]:
                print(f"       Páginas: {libro[6]}")
            if libro[8]:
                print(f"       Ubicación: {libro[8]}")
            print()
        
        return libros
    except Error as e:
        print(f"❌ Error al listar libros: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def buscar_libro(termino_busqueda):
    """
    Busca libros por título, autor o ISBN
    
    Args:
        termino_busqueda: Término a buscar en título, autor o ISBN
    
    Returns:
        Lista de libros encontrados
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        query = """
        SELECT l.id, l.titulo, l.autor, l.isbn, l.estado, c.nombre as categoria, l.ubicacion
        FROM libros l
        LEFT JOIN categorias c ON l.categoria_id = c.id
        WHERE l.titulo LIKE %s OR l.autor LIKE %s OR l.isbn LIKE %s
        ORDER BY l.titulo
        """
        busqueda = f"%{termino_busqueda}%"
        cursor.execute(query, (busqueda, busqueda, busqueda))
        libros = cursor.fetchall()
        
        print(f"\n🔍 Resultados de búsqueda para '{termino_busqueda}': {len(libros)} encontrados")
        print("-" * 80)
        for libro in libros:
            print(f"   [{libro[0]}] {libro[1]} - {libro[2]}")
            print(f"       Estado: {libro[4]} | Categoría: {libro[5] or 'Sin categoría'}")
            if libro[6]:
                print(f"       Ubicación: {libro[6]}")
            print()
        
        return libros
    except Error as e:
        print(f"❌ Error al buscar libro: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def actualizar_libro(libro_id, **kwargs):
    """
    Actualiza información de un libro
    
    Args:
        libro_id: ID del libro a actualizar
        **kwargs: Campos a actualizar (titulo, autor, isbn, editorial, año_publicacion, 
                 categoria_id, paginas, estado, ubicacion, notas)
    
    Returns:
        True si se actualizó correctamente, False en caso contrario
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Construir la consulta dinámicamente
        campos_permitidos = ['titulo', 'autor', 'isbn', 'editorial', 'año_publicacion', 
                           'categoria_id', 'paginas', 'estado', 'ubicacion', 'notas']
        campos_actualizar = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos_actualizar.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos_actualizar:
            print("❌ No se proporcionaron campos válidos para actualizar")
            return False
        
        query = f"UPDATE libros SET {', '.join(campos_actualizar)} WHERE id = %s"
        valores.append(libro_id)
        
        cursor.execute(query, valores)
        conexion.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Libro ID {libro_id} actualizado exitosamente")
            return True
        else:
            print(f"⚠️ No se encontró el libro con ID {libro_id}")
            return False
    except Error as e:
        print(f"❌ Error al actualizar libro: {e}")
        conexion.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def eliminar_libro(libro_id):
    """
    Elimina un libro de la biblioteca
    
    Args:
        libro_id: ID del libro a eliminar
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Primero obtener el título para mostrar
        cursor.execute("SELECT titulo FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        
        if not libro:
            print(f"⚠️ No se encontró el libro con ID {libro_id}")
            return False
        
        # Eliminar el libro
        cursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))
        conexion.commit()
        
        print(f"✅ Libro '{libro[0]}' (ID: {libro_id}) eliminado exitosamente")
        return True
    except Error as e:
        print(f"❌ Error al eliminar libro: {e}")
        conexion.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def listar_categorias():
    """
    Lista todas las categorías disponibles
    
    Returns:
        Lista de categorías
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, nombre, descripcion FROM categorias ORDER BY nombre")
        categorias = cursor.fetchall()
        
        print(f"\n📂 Categorías disponibles: {len(categorias)}")
        print("-" * 60)
        for cat in categorias:
            print(f"   [{cat[0]}] {cat[1]}")
            if cat[2]:
                print(f"       {cat[2]}")
            print()
        
        return categorias
    except Error as e:
        print(f"❌ Error al listar categorías: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def agregar_categoria(nombre, descripcion=None):
    """
    Agrega una nueva categoría
    
    Args:
        nombre: Nombre de la categoría
        descripcion: Descripción opcional
    
    Returns:
        ID de la categoría insertada o None si hay error
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        insert_query = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        cursor.execute(insert_query, (nombre, descripcion))
        conexion.commit()
        categoria_id = cursor.lastrowid
        print(f"✅ Categoría '{nombre}' agregada exitosamente (ID: {categoria_id})")
        return categoria_id
    except Error as e:
        print(f"❌ Error al agregar categoría: {e}")
        conexion.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def prestar_libro(libro_id, persona, fecha_devolucion_esperada=None, notas=None):
    """
    Registra un préstamo de libro
    
    Args:
        libro_id: ID del libro a prestar
        persona: Nombre de la persona a quien se presta
        fecha_devolucion_esperada: Fecha esperada de devolución (opcional)
        notas: Notas adicionales (opcional)
    
    Returns:
        ID del préstamo o None si hay error
    """
    from datetime import date
    
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Verificar que el libro existe y está disponible
        cursor.execute("SELECT titulo, estado FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        
        if not libro:
            print(f"❌ No se encontró el libro con ID {libro_id}")
            return None
        
        if libro[1] != 'Disponible':
            print(f"⚠️ El libro '{libro[0]}' no está disponible. Estado actual: {libro[1]}")
            return None
        
        # Insertar préstamo
        insert_prestamo = """
        INSERT INTO prestamos (libro_id, persona_prestamo, fecha_prestamo, fecha_devolucion_esperada, notas)
        VALUES (%s, %s, %s, %s, %s)
        """
        fecha_prestamo = date.today()
        cursor.execute(insert_prestamo, (libro_id, persona, fecha_prestamo, fecha_devolucion_esperada, notas))
        prestamo_id = cursor.lastrowid
        
        # Actualizar estado del libro
        cursor.execute("UPDATE libros SET estado = 'Prestado' WHERE id = %s", (libro_id,))
        
        conexion.commit()
        print(f"✅ Libro '{libro[0]}' prestado a {persona} (Préstamo ID: {prestamo_id})")
        return prestamo_id
    except Error as e:
        print(f"❌ Error al prestar libro: {e}")
        conexion.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def devolver_libro(libro_id, prestamo_id=None):
    """
    Registra la devolución de un libro
    
    Args:
        libro_id: ID del libro a devolver
        prestamo_id: ID del préstamo (opcional, si no se proporciona busca el préstamo activo)
    
    Returns:
        True si se devolvió correctamente, False en caso contrario
    """
    from datetime import date
    
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Si no se proporciona prestamo_id, buscar el préstamo activo
        if not prestamo_id:
            cursor.execute("""
                SELECT id FROM prestamos 
                WHERE libro_id = %s AND estado = 'Prestado' 
                ORDER BY fecha_prestamo DESC LIMIT 1
            """, (libro_id,))
            prestamo = cursor.fetchone()
            if prestamo:
                prestamo_id = prestamo[0]
            else:
                print(f"❌ No se encontró un préstamo activo para el libro ID {libro_id}")
                return False
        
        # Actualizar préstamo
        cursor.execute("""
            UPDATE prestamos 
            SET estado = 'Devuelto', fecha_devolucion_real = %s 
            WHERE id = %s
        """, (date.today(), prestamo_id))
        
        # Actualizar estado del libro
        cursor.execute("UPDATE libros SET estado = 'Disponible' WHERE id = %s", (libro_id,))
        
        conexion.commit()
        print(f"✅ Libro ID {libro_id} devuelto exitosamente")
        return True
    except Error as e:
        print(f"❌ Error al devolver libro: {e}")
        conexion.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def listar_prestamos(estado=None, mostrar_todos=True):
    """
    Lista los préstamos, opcionalmente filtrados por estado
    
    Args:
        estado: Filtrar por estado ('Prestado', 'Devuelto', 'Vencido')
        mostrar_todos: Si es True, muestra todos los préstamos
    
    Returns:
        Lista de préstamos
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        query = """
        SELECT p.id, l.titulo, l.autor, p.persona_prestamo, p.fecha_prestamo, 
               p.fecha_devolucion_esperada, p.fecha_devolucion_real, p.estado
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        WHERE 1=1
        """
        params = []
        
        if not mostrar_todos and estado:
            query += " AND p.estado = %s"
            params.append(estado)
        
        query += " ORDER BY p.fecha_prestamo DESC"
        
        cursor.execute(query, params if params else None)
        prestamos = cursor.fetchall()
        
        print(f"\n📋 Préstamos encontrados: {len(prestamos)}")
        print("-" * 80)
        for p in prestamos:
            print(f"   [{p[0]}] {p[1]} - {p[2]}")
            print(f"       Prestado a: {p[3]} | Fecha préstamo: {p[4]} | Estado: {p[7]}")
            if p[5]:
                print(f"       Devolución esperada: {p[5]}")
            if p[6]:
                print(f"       Devolución real: {p[6]}")
            print()
        
        return prestamos
    except Error as e:
        print(f"❌ Error al listar préstamos: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

def estadisticas_biblioteca():
    """
    Muestra estadísticas de la biblioteca
    
    Returns:
        Diccionario con estadísticas
    """
    config = get_pymysql_config()
    conexion = None
    cursor = None
    
    try:
        conexion = pymysql.connect(**config)
        cursor = conexion.cursor()
        
        # Total de libros
        cursor.execute("SELECT COUNT(*) FROM libros")
        total_libros = cursor.fetchone()[0]
        
        # Libros por estado
        cursor.execute("""
            SELECT estado, COUNT(*) 
            FROM libros 
            GROUP BY estado
        """)
        por_estado = cursor.fetchall()
        
        # Libros por categoría
        cursor.execute("""
            SELECT c.nombre, COUNT(l.id) 
            FROM categorias c
            LEFT JOIN libros l ON c.id = l.categoria_id
            GROUP BY c.id, c.nombre
            ORDER BY COUNT(l.id) DESC
        """)
        por_categoria = cursor.fetchall()
        
        # Préstamos activos
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'Prestado'")
        prestamos_activos = cursor.fetchone()[0]
        
        # Total de categorías
        cursor.execute("SELECT COUNT(*) FROM categorias")
        total_categorias = cursor.fetchone()[0]
        
        print("\n📊 ESTADÍSTICAS DE LA BIBLIOTECA")
        print("=" * 60)
        print(f"📚 Total de libros: {total_libros}")
        print(f"📂 Total de categorías: {total_categorias}")
        print(f"📋 Préstamos activos: {prestamos_activos}")
        print("\n📊 Libros por estado:")
        for estado, cantidad in por_estado:
            print(f"   {estado}: {cantidad}")
        print("\n📊 Libros por categoría:")
        for categoria, cantidad in por_categoria:
            if cantidad > 0:
                print(f"   {categoria}: {cantidad}")
        
        return {
            'total_libros': total_libros,
            'total_categorias': total_categorias,
            'prestamos_activos': prestamos_activos,
            'por_estado': dict(por_estado),
            'por_categoria': dict(por_categoria)
        }
    except Error as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.open:
            conexion.close()

# ============================================
# INTERFAZ DE MENÚ INTERACTIVO
# ============================================

def menu_principal():
    """
    Interfaz de menú interactivo para gestionar la biblioteca
    """
    from datetime import date, timedelta
    
    while True:
        print("\n" + "="*60)
        print("📚 SISTEMA DE GESTIÓN DE BIBLIOTECA HOGAREÑA")
        print("="*60)
        print("\nMENÚ PRINCIPAL:")
        print("  1. 📖 Agregar libro")
        print("  2. 📋 Listar todos los libros")
        print("  3. 🔍 Buscar libro")
        print("  4. ✏️  Actualizar libro")
        print("  5. 🗑️  Eliminar libro")
        print("  6. 📂 Ver categorías")
        print("  7. ➕ Agregar categoría")
        print("  8. 📤 Prestar libro")
        print("  9. 📥 Devolver libro")
        print(" 10. 📋 Ver préstamos")
        print(" 11. 📊 Estadísticas")
        print("  0. 🚪 Salir")
        print("-"*60)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        elif opcion == "1":
            print("\n📖 AGREGAR NUEVO LIBRO")
            print("-"*60)
            titulo = input("Título: ").strip()
            if not titulo:
                print("❌ El título es obligatorio")
                continue
            autor = input("Autor: ").strip()
            if not autor:
                print("❌ El autor es obligatorio")
                continue
            
            isbn = input("ISBN (opcional): ").strip() or None
            editorial = input("Editorial (opcional): ").strip() or None
            año_str = input("Año de publicación (opcional): ").strip()
            año = int(año_str) if año_str.isdigit() else None
            paginas_str = input("Número de páginas (opcional): ").strip()
            paginas = int(paginas_str) if paginas_str.isdigit() else None
            ubicacion = input("Ubicación física (opcional): ").strip() or None
            notas = input("Notas (opcional): ").strip() or None
            
            # Mostrar categorías disponibles
            print("\nCategorías disponibles:")
            categorias = listar_categorias()
            if categorias:
                cat_id_str = input("ID de categoría (opcional, presiona Enter para omitir): ").strip()
                categoria_id = int(cat_id_str) if cat_id_str.isdigit() else None
            else:
                categoria_id = None
            
            agregar_libro(titulo, autor, isbn, editorial, año, categoria_id, paginas, ubicacion, notas)
        
        elif opcion == "2":
            print("\n📋 LISTAR LIBROS")
            print("-"*60)
            print("Filtros opcionales:")
            print("  1. Todos los libros")
            print("  2. Solo disponibles")
            print("  3. Solo prestados")
            print("  4. Por categoría")
            filtro = input("Selecciona opción (1-4, default=1): ").strip() or "1"
            
            if filtro == "1":
                listar_libros(mostrar_todos=True)
            elif filtro == "2":
                listar_libros(estado="Disponible", mostrar_todos=False)
            elif filtro == "3":
                listar_libros(estado="Prestado", mostrar_todos=False)
            elif filtro == "4":
                categorias = listar_categorias()
                if categorias:
                    cat_id_str = input("ID de categoría: ").strip()
                    if cat_id_str.isdigit():
                        listar_libros(categoria_id=int(cat_id_str), mostrar_todos=False)
                    else:
                        print("❌ ID inválido")
                else:
                    print("❌ No hay categorías disponibles")
        
        elif opcion == "3":
            print("\n🔍 BUSCAR LIBRO")
            print("-"*60)
            termino = input("Buscar (título, autor o ISBN): ").strip()
            if termino:
                buscar_libro(termino)
            else:
                print("❌ Debes ingresar un término de búsqueda")
        
        elif opcion == "4":
            print("\n✏️  ACTUALIZAR LIBRO")
            print("-"*60)
            libro_id_str = input("ID del libro a actualizar: ").strip()
            if not libro_id_str.isdigit():
                print("❌ ID inválido")
                continue
            
            libro_id = int(libro_id_str)
            print("\nIngresa los campos a actualizar (presiona Enter para omitir):")
            
            actualizaciones = {}
            titulo = input("Nuevo título: ").strip()
            if titulo:
                actualizaciones['titulo'] = titulo
            
            autor = input("Nuevo autor: ").strip()
            if autor:
                actualizaciones['autor'] = autor
            
            isbn = input("Nuevo ISBN: ").strip()
            if isbn:
                actualizaciones['isbn'] = isbn
            
            editorial = input("Nueva editorial: ").strip()
            if editorial:
                actualizaciones['editorial'] = editorial
            
            año_str = input("Nuevo año: ").strip()
            if año_str.isdigit():
                actualizaciones['año_publicacion'] = int(año_str)
            
            paginas_str = input("Nuevo número de páginas: ").strip()
            if paginas_str.isdigit():
                actualizaciones['paginas'] = int(paginas_str)
            
            ubicacion = input("Nueva ubicación: ").strip()
            if ubicacion:
                actualizaciones['ubicacion'] = ubicacion
            
            print("\nEstados disponibles: Disponible, Prestado, Perdido, En reparación")
            estado = input("Nuevo estado: ").strip()
            if estado in ['Disponible', 'Prestado', 'Perdido', 'En reparación']:
                actualizaciones['estado'] = estado
            
            notas = input("Nuevas notas: ").strip()
            if notas:
                actualizaciones['notas'] = notas
            
            if actualizaciones:
                actualizar_libro(libro_id, **actualizaciones)
            else:
                print("⚠️ No se ingresaron campos para actualizar")
        
        elif opcion == "5":
            print("\n🗑️  ELIMINAR LIBRO")
            print("-"*60)
            libro_id_str = input("ID del libro a eliminar: ").strip()
            if libro_id_str.isdigit():
                confirmar = input(f"¿Estás seguro de eliminar el libro ID {libro_id_str}? (s/n): ").strip().lower()
                if confirmar == 's':
                    eliminar_libro(int(libro_id_str))
                else:
                    print("❌ Operación cancelada")
            else:
                print("❌ ID inválido")
        
        elif opcion == "6":
            print("\n📂 CATEGORÍAS")
            listar_categorias()
        
        elif opcion == "7":
            print("\n➕ AGREGAR CATEGORÍA")
            print("-"*60)
            nombre = input("Nombre de la categoría: ").strip()
            if nombre:
                descripcion = input("Descripción (opcional): ").strip() or None
                agregar_categoria(nombre, descripcion)
            else:
                print("❌ El nombre es obligatorio")
        
        elif opcion == "8":
            print("\n📤 PRESTAR LIBRO")
            print("-"*60)
            libro_id_str = input("ID del libro a prestar: ").strip()
            if not libro_id_str.isdigit():
                print("❌ ID inválido")
                continue
            
            persona = input("Nombre de la persona: ").strip()
            if not persona:
                print("❌ El nombre es obligatorio")
                continue
            
            fecha_str = input("Fecha de devolución esperada (YYYY-MM-DD, opcional): ").strip()
            fecha_devolucion = None
            if fecha_str:
                try:
                    fecha_devolucion = date.fromisoformat(fecha_str)
                except ValueError:
                    print("⚠️ Fecha inválida, se omitirá")
            
            notas = input("Notas (opcional): ").strip() or None
            
            prestar_libro(int(libro_id_str), persona, fecha_devolucion, notas)
        
        elif opcion == "9":
            print("\n📥 DEVOLVER LIBRO")
            print("-"*60)
            libro_id_str = input("ID del libro a devolver: ").strip()
            if libro_id_str.isdigit():
                devolver_libro(int(libro_id_str))
            else:
                print("❌ ID inválido")
        
        elif opcion == "10":
            print("\n📋 PRÉSTAMOS")
            print("-"*60)
            print("  1. Todos los préstamos")
            print("  2. Solo préstamos activos")
            print("  3. Solo préstamos devueltos")
            filtro = input("Selecciona opción (1-3, default=1): ").strip() or "1"
            
            if filtro == "1":
                listar_prestamos(mostrar_todos=True)
            elif filtro == "2":
                listar_prestamos(estado="Prestado", mostrar_todos=False)
            elif filtro == "3":
                listar_prestamos(estado="Devuelto", mostrar_todos=False)
        
        elif opcion == "11":
            estadisticas_biblioteca()
        
        else:
            print("❌ Opción inválida. Por favor selecciona una opción del menú.")
        
        input("\n⏎ Presiona Enter para continuar...")

if __name__ == "__main__":
    # Verificar conexión y crear estructura
    print("🔌 Verificando conexión a la base de datos...")
    conectar_pymysql()
    
    print("\n" + "="*50)
    print("Creando estructura de biblioteca (si no existe)...")
    crear_estructura_biblioteca()
    
    # Iniciar menú interactivo
    menu_principal()