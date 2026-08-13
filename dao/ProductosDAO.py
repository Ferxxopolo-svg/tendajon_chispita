from database.conexion import Conexion

def insertar_producto(nombre, precio, stock):
    conn = Conexion()
    cur = conn.cursor()
    cur.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", 
                (nombre, precio, stock))
    conn.commit()
    cur.close()
    conn.close()

def obtener_productos():
    conn = Conexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def actualizar_producto(id, nombre, precio, stock):
    conn = Conexion()
    cur = conn.cursor()
    cur.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id=%s", 
                (nombre, precio, stock, id))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_producto(id):
    conn = Conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()