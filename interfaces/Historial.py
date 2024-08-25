import streamlit as st
from connection import connect
import pandas as pd

# Filtros
st.subheader("Filters")

with st.container():
    col1_date, col2_price = st.columns([10,10])

    with col1_date:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_date = st.date_input("Hello",value=None,label_visibility="collapsed") # Buscar por fecha

    with col2_price:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_price = st.number_input("Hello",value=0.0,placeholder="Enter price tag",label_visibility="collapsed") # Buscar por $ total de venta
    
    col3_product, col4_vendor = st.columns([10, 10]) 

    with col3_product:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_product = st.text_input("Hello",value="",placeholder="Enter name of product",label_visibility="collapsed") # Buscar por nombre de producto
    
    with col4_vendor:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_vendor = st.text_input("Hello",value="",placeholder="Enter username of vendor",label_visibility="collapsed") # Buscar por nombre de vendedor 

# Botón de busqueda con lógica de filtros
# TODO: Buscar una manera de des-espaguetificar la lógica de condicionales de los filtros
with st.container():
    search_button = st.button("Search")
    if search_button:
        if (sale_date) and (sale_price != 0.0) and (sale_product != "") and (sale_vendor != ""): #1111
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND (v.cantidad*p.precio)={sale_price} AND p.nombre=\"{sale_product}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha, $ total, nombre de producto y username del vendedor
        elif (sale_date) and (sale_price != 0) and (sale_product != ""): #1110
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND (v.cantidad*p.precio)={sale_price} AND p.nombre=\"{sale_product}\"") # Cargar ventas por fecha, $ total y nombre de producto
        elif (sale_date) and(sale_price != 0) and (sale_vendor != ""): #1101
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND (v.cantidad*p.precio)={sale_price} AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha, $ total y username del vendedor
        elif (sale_date) and (sale_product != "") and (sale_vendor != ""): #1011
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND p.nombre=\"{sale_product}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha, nombre de producto y username del vendedor
        elif (sale_price != 0) and (sale_product != "") and (sale_vendor != ""): #0111
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE (v.cantidad*p.precio)={sale_price} AND p.nombre=\"{sale_product}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por $ total, nombre de producto y username del vendedor
        elif (sale_date) and (sale_product != ""): #1010
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND p.nombre=\"{sale_product}\"") # Cargar ventas por fecha y nombre de producto
        elif (sale_date) and (sale_vendor != ""): #1001
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha y username de vendedor
        elif (sale_date) and (sale_price != 0.0): #1100
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND (v.cantidad*p.precio)={sale_price}") # Cargar ventas por fecha y $ total
        elif (sale_price != 0) and (sale_product != ""): #0110
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE (v.cantidad*p.precio)={sale_price} AND p.nombre=\"{sale_product}\"") # Cargar ventas por $ total y nombre de producto
        elif (sale_price != 0) and (sale_vendor != ""): #0101
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE (v.cantidad*p.precio)={sale_price} AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por $ total y username de vendedor
        elif (sale_product != "") and (sale_vendor != ""): #0011
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE p.nombre=\"{sale_product}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por nombre de producto y username de vendedor
        elif (sale_price != 0.0): #0100
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE (v.cantidad*p.precio)={sale_price}") # Cargar ventas por $ total
        elif (sale_product != ""): #0010
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE p.nombre=\"{sale_product}\"") # Cargar ventas por nombre de producto
        elif (sale_vendor != ""): #0001
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE u.usuario=\"{sale_vendor}\"") # Cargar ventas por username de vendedor
        elif (sale_date): #1000
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\"") # Cargar ventas por fecha
        else: #0000
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula") # Cargar todas las ventas
        wins = data["total"].str.replace('$', "", regex=False) # Extraer el total de cada fila.
        new_row = {'NroVenta':'total:', 'total':f'${wins.astype(float).sum()}'} # Nueva columna para calcular el total ganado.
        df_new_row = pd.DataFrame([new_row]) # La columna se convierte a dataframe para poder concatenarla.
        data = pd.concat([data, df_new_row], ignore_index=True)
        st.dataframe(data)