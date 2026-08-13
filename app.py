import flet as ft
from dao.ProductosDAO import insertar_producto, obtener_productos, actualizar_producto, eliminar_producto

def main(page: ft.Page):
    page.title = "Inventario de Productos"
    page.vertical_alignment = ft.MainAxisAlignment.START

    nombre = ft.TextField(label="Nombre Del Producto")
    precio = ft.TextField(label="Precio Del Producto")
    stock = ft.TextField(label="Stock")
    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre Del Producto")),
        ft.DataColumn(ft.Text("Precio")),
        ft.DataColumn(ft.Text("Stock")),
    ])

    def cargar_tabla():
        tabla.rows.clear()
        for p in obtener_productos():
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(p[0]))),
                    ft.DataCell(ft.Text(p[1])),
                    ft.DataCell(ft.Text(str(p[2]))),
                    ft.DataCell(ft.Text(str(p[3]))),
                ])
            )
        page.update()

    def agregar_producto(e):
        insertar_producto(nombre.value, float(precio.value), int(stock.value))
        cargar_tabla()

    page.add(nombre, precio, stock, ft.ElevatedButton("Agregar", on_click=agregar_producto), tabla)
    cargar_tabla()

ft.app(target=main)