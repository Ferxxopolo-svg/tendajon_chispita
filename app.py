import flet as ft
from dao.ProductosDAO import obtener_productos, actualizar_producto, eliminar_producto
from database.conexion import Conexion

def insertar_producto(nombre, precio, stock):
    conn = Conexion()
    cur = conn.cursor()
    # Calcular el próximo ID como cantidad de registros + 1
    cur.execute("SELECT COUNT(*) + 1 FROM productos")
    nuevo_id = cur.fetchone()[0]
    cur.execute("INSERT INTO productos (id, nombre, precio, stock) VALUES (%s, %s, %s, %s)",
                (nuevo_id, nombre, precio, stock))
    conn.commit()
    cur.close()
    conn.close()

def reordenar_ids():
    conn = Conexion()
    cur = conn.cursor()
    # Reasignar IDs consecutivos empezando desde 1
    cur.execute("""
        WITH renumerados AS (
            SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS nuevo_id
            FROM productos ORDER BY id
        )
        UPDATE productos p
        SET id = r.nuevo_id
        FROM renumerados r
        WHERE p.id = r.id;
    """)
    conn.commit()
    cur.close()
    conn.close()

def main(page: ft.Page):
    page.title = "Inventario de Productos"
    page.vertical_alignment = ft.MainAxisAlignment.START

    nombre = ft.TextField(label="Nombre Del Producto")
    precio = ft.TextField(label="Precio Del Producto")
    stock = ft.TextField(label="Stock")

    boton_agregar = ft.ElevatedButton("Agregar")
    boton_actualizar = ft.ElevatedButton("Actualizar", visible=False)

    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre Del Producto")),
        ft.DataColumn(ft.Text("Precio")),
        ft.DataColumn(ft.Text("Stock")),
        ft.DataColumn(ft.Text("Acciones")),
    ])

    producto_editando = {"id": None}

    def cargar_tabla():
        tabla.rows.clear()
        # Ordenar por ID para que siempre aparezcan consecutivos
        productos = sorted(obtener_productos(), key=lambda x: x[0])
        for p in productos:
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(p[0]))),
                    ft.DataCell(ft.Text(p[1])),
                    ft.DataCell(ft.Text(str(p[2]))),
                    ft.DataCell(ft.Text(str(p[3]))),
                    ft.DataCell(
                        ft.Row([
                            ft.ElevatedButton("Editar", on_click=lambda e, id=p[0], nombre=p[1], precio=p[2], stock=p[3]: editar_producto(id, nombre, precio, stock)),
                            ft.ElevatedButton("Eliminar", on_click=lambda e, id=p[0]: borrar_producto(id))
                        ])
                    )
                ])
            )
        page.update()

    def agregar_producto(e):
        insertar_producto(nombre.value, float(precio.value), int(stock.value))
        nombre.value = ""
        precio.value = ""
        stock.value = ""
        page.update()
        cargar_tabla()

    def editar_producto(id, nombre_actual, precio_actual, stock_actual):
        nombre.value = nombre_actual
        precio.value = str(precio_actual)
        stock.value = str(stock_actual)
        producto_editando["id"] = id
        boton_agregar.visible = False
        boton_actualizar.visible = True
        page.update()

    def actualizar_producto_evento(e):
        if producto_editando["id"] is not None:
            actualizar_producto(producto_editando["id"], nombre.value, float(precio.value), int(stock.value))
            producto_editando["id"] = None
            nombre.value = ""
            precio.value = ""
            stock.value = ""
            boton_agregar.visible = True
            boton_actualizar.visible = False
            reordenar_ids()   # asegurar que IDs queden consecutivos
            cargar_tabla()
            page.update()

    def borrar_producto(id):
        eliminar_producto(id)
        reordenar_ids()   # reordenar IDs después de eliminar
        cargar_tabla()

    boton_agregar.on_click = agregar_producto
    boton_actualizar.on_click = actualizar_producto_evento

    page.add(
        nombre, precio, stock,
        ft.Row([boton_agregar, boton_actualizar]),
        tabla
    )
    cargar_tabla()

ft.app(target=main)