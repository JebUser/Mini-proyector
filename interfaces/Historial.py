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

with st.container():
    search_button = st.button("Search")
    data = None
    query = "SELECT v.NroVenta, v.fecha, p.nombre, u.usuario AS vendedor, c.Nombre AS cliente, v.cantidad, CONCAT('$',(v.cantidad*p.precio)) AS total FROM Venta v JOIN productos p ON v.IDProducto = p.id JOIN usuarios u ON v.IDEmpleado = u.id JOIN Cliente c ON v.Comprador = c.Cedula" # Query por defecto.
    data = connect.query(query)
    if search_button:
        # En caso tal de que haya alguno de los filtros.
        if (sale_date) or (sale_price != 0.0) or (sale_product != "") or (sale_vendor != ""):
            conditions = [] # Lista a la que se irá agregando las condiciones dadas para filtrar.
            if sale_date:
                conditions.append(f"v.fecha=\"{sale_date}\"")
            if sale_price != 0.0:
                conditions.append(f"(v.cantidad*p.precio)={sale_price}")
            if sale_product != "":
                conditions.append(f"p.nombre LIKE \"%{sale_product}%\"")
            if sale_vendor != "":
                conditions.append(f"u.usuario LIKE \"%{sale_vendor}%\"")
            query += " WHERE " + (" AND ".join(conditions)) # Se agregan las condiciones al query siguiendo las normas de queries en SQL.
        data = connect.query(query)
    wins = data["total"].str.replace('$', "", regex=False) # Extraer el total de cada fila.
    new_row = {'NroVenta':'total:', 'total':f'${wins.astype(float).sum()}'} # Nueva columna para calcular el total ganado.
    df_new_row = pd.DataFrame([new_row]) # La columna se convierte a dataframe para poder concatenarla.
    data = pd.concat([data, df_new_row], ignore_index=True)
    st.dataframe(data)
    st.cache_data.clear()