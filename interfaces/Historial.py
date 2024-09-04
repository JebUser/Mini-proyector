import streamlit as st
from connection import connect
import pandas as pd

# Filtros
st.subheader("Filters")

with st.container():
    col1_date, col2_price = st.columns([10, 10])

    with col1_date:
        col2, col3 = st.columns([3, 1])
        with col2:
            sale_date = st.date_input("Hello", value=None, label_visibility="collapsed")  # Buscar por fecha

    with col2_price:
        col2, col3 = st.columns([3, 1])
        with col2:
            sale_price = st.number_input("Hello", value=0.0, placeholder="Enter price tag", label_visibility="collapsed")  # Buscar por $ total de venta
    
    col3_product, col4_vendor = st.columns([10, 10]) 

    with col3_product:
        col2, col3 = st.columns([3, 1])
        with col2:
            sale_product = st.text_input("Hello", value="", placeholder="Enter name of product", label_visibility="collapsed")  # Buscar por nombre de producto
    
    with col4_vendor:
        col2, col3 = st.columns([3, 1])
        with col2:
            sale_vendor = st.text_input("Hello", value="", placeholder="Enter username of vendor", label_visibility="collapsed")  # Buscar por nombre de vendedor 

with st.container():
    search_button = st.button("Search")
    data = None
    query = """
    SELECT v.NroVenta, v.fecha, u.usuario AS vendedor, c.Nombre AS cliente 
    FROM venta v 
    JOIN usuarios u ON v.ID_Empleado = u.id 
    JOIN Cliente c ON v.ID_Cliente = c.Cedula
    """  # Query por defecto.
    
    if search_button:
        # En caso tal de que haya alguno de los filtros.
        if (sale_date) or (sale_price != 0.0) or (sale_product != "") or (sale_vendor != ""):
            conditions = []  # Lista a la que se irán agregando las condiciones dadas para filtrar.
            if sale_date:
                conditions.append(f"v.fecha='{sale_date}'")
            if sale_price != 0.0:
                conditions.append(f"(pv.Cantidad * p.precio)={sale_price}")
            if sale_product != "":
                conditions.append(f"p.nombre LIKE '%{sale_product}%'")
            if sale_vendor != "":
                conditions.append(f"u.usuario LIKE '%{sale_vendor}%'")
            query += " WHERE " + (" AND ".join(conditions))  # Se agregan las condiciones al query siguiendo las normas de SQL.
    
    data = connect.query(query)
    
    if not data.empty:
        st.write("Lista de ventas:")
        st.dataframe(data)  # Mostrar todas las ventas sin filtros.
        
        # Seleccionar una venta específica
        selected_sale = st.selectbox("Select Sale", data["NroVenta"].unique())
        
        # Mostrar productos de la venta seleccionada
        if selected_sale:
            product_query = f"""
            SELECT p.nombre, pv.Cantidad, p.precio, CONCAT('$', (pv.Cantidad * p.precio)) AS subtotal 
            FROM prod_venta pv 
            JOIN productos p ON pv.ID_Producto = p.id 
            WHERE pv.NroVenta = {selected_sale}
            """
            products_data = connect.query(product_query)
            st.subheader(f"Products in Sale #{selected_sale}")
            st.dataframe(products_data)
    else:
        st.write("No sales found with the applied filters.")
    
    st.cache_data.clear()