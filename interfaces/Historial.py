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
            sale_date = st.date_input("Hello",label_visibility="collapsed") # Buscar por fecha

    # TODO: Averiguar como poner el $$$ de la venta en el dataframe (Precio del producto * Unidades vendidas)
    with col2_price:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_price = st.number_input("Hello",value=0.0,placeholder="Enter price tag",label_visibility="collapsed") # Buscar por precio
    
    col3_product, col4_vendor = st.columns([10, 10]) 

    with col3_product:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_product = st.text_input("Hello",value="",placeholder="Enter name of product",label_visibility="collapsed") # Buscar por nombre de producto
    
    with col4_vendor:
        col2, col3 = st.columns([3,1])
        with col2:
            sale_vendor = st.text_input("Hello",value="",placeholder="Enter name of vendor",label_visibility="collapsed") # Buscar por nombre de vendedor 

# Botón de busqueda con lógica de filtros
with st.container():
    search_button = st.button("Search")
    if search_button:
        if col2_price != 0 or col3_product != "" or col4_vendor != "":
            data = connect.query()
        data = None
        """
        if (sale_date) and (sale_product != "") and (sale_vendor != ""):
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND p.nombre=\"{sale_product}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha, nombre de producto y username del vendedor
        elif (sale_date) and (sale_product != ""):
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND p.nombre=\"{sale_product}\"") # Cargar ventas por fecha y nombre de producto
        elif (sale_date) and (sale_vendor != ""):
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\" AND u.usuario=\"{sale_vendor}\"") # Cargar ventas por fecha y username de vendedor
        elif (sale_date):
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula WHERE v.fecha=\"{sale_date}\"") # Cargar ventas por fecha
        else:
            data = connect.query(f"SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula") # Cargar todas las ventas
        """
        wins = data["total"].str.replace('$', "", regex=False) # Extraer el total de cada fila.
        new_row = {'NroVenta':'total:', 'total':f'${wins.astype(float).sum()}'} # Nueva columna para calcular el total ganado.
        df_new_row = pd.DataFrame([new_row]) # La columna se convierte a dataframe para poder concatenarla.
        data = pd.concat([data, df_new_row], ignore_index=True)
        st.dataframe(data)