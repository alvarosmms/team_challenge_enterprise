import os
import sqlite3

### Obtener la ruta del directorio actual del script
directorio_actual = os.path.dirname(os.path.abspath(__file__))

### Ruta completa para la base de datos
ruta_db = os.path.join(directorio_actual, "proveedores_piezas.db")

### Conectar a la base de datos y si no existe la creamos
conexion = sqlite3.connect(ruta_db)
cursor = conexion.cursor()

print(f"Base de datos creada o conectada en: {ruta_db}")

### Crear tablas con "IF NOT EXISTS" para evitar errores si ya existen
sql_crear_tablas = """
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    ciudad TEXT NOT NULL,
    provincia TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS piezas (
    id_pieza INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    color TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    id_categoria INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE IF NOT EXISTS suministros (
    id_suministro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_proveedor INTEGER,
    id_pieza INTEGER,
    cantidad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_pieza) REFERENCES piezas(id_pieza)
);
"""

### Ejecutar la creación de tablas
cursor.executescript(sql_crear_tablas)
print("Tablas creadas exitosamente.")

### Insertar datos iniciales en proveedores
datos_proveedores = [
    ("Proveedor A", "Calle Falsa 123", "Madrid", "Madrid"),
    ("Proveedor B", "Avenida Siempreviva 456", "Barcelona", "Cataluña"),
    ("Proveedor C", "Calle del Sol 789", "Valencia", "Valencia")
]
cursor.executemany("""
INSERT INTO proveedores (nombre, direccion, ciudad, provincia)
VALUES (?, ?, ?, ?)
""", datos_proveedores)

### Insertar datos iniciales en categorías
datos_categorias = [
    ("Electrónica",),
    ("Mecánica",),
    ("Textil",)
]
cursor.executemany("""
INSERT INTO categorias (nombre)
VALUES (?)
""", datos_categorias)

### Insertar datos iniciales en piezas
datos_piezas = [
    ("Tornillo", "Plateado", 0.10, 2),  # Relacionado con categoría Mecánica (id_categoria = 2)
    ("Resistor", "Negro", 0.05, 1),    # Relacionado con categoría Electrónica (id_categoria = 1)
    ("Tela Azul", "Azul", 5.50, 3)     # Relacionado con categoría Textil (id_categoria = 3)
]
cursor.executemany("""
INSERT INTO piezas (nombre, color, precio, id_categoria)
VALUES (?, ?, ?, ?)
""", datos_piezas)

### Insertar datos iniciales en suministros
datos_suministros = [
    (1, 1, 100, "2024-11-01"),  # Proveedor 1 suministra 100 tornillos
    (2, 2, 200, "2024-11-05"),  # Proveedor 2 suministra 200 resistores
    (3, 3, 50, "2024-11-10")    # Proveedor 3 suministra 50 telas
]
cursor.executemany("""
INSERT INTO suministros (id_proveedor, id_pieza, cantidad, fecha)
VALUES (?, ?, ?, ?)
""", datos_suministros)

### Confirmar los cambios
conexion.commit()
print("Datos iniciales insertados exitosamente.")

### Consultas para verificar los datos
print("\nVerificando datos:")

### Consulta 1: Proveedores
print("\nProveedores:")
cursor.execute("SELECT * FROM proveedores")
for row in cursor.fetchall():
    print(row)

### Consulta 2: Categorías
print("\nCategorías:")
cursor.execute("SELECT * FROM categorias")
for row in cursor.fetchall():
    print(row)

### Consulta 3: Piezas
print("\nPiezas:")
cursor.execute("SELECT * FROM piezas")
for row in cursor.fetchall():
    print(row)

### Consulta 4: Suministros
print("\nSuministros:")
cursor.execute("SELECT * FROM suministros")
for row in cursor.fetchall():
    print(row)


