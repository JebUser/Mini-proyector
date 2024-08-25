import streamlit as st
import pandas as pd
from connection import connect

tab1, tab2, tab3,tab4 = st.tabs(["Till", "Sales", "Reports","Settings"])

column_configuration = {
    "id": st.column_config.TextColumn("ID", help="ID del producto", max_chars=100),
    "nombre": st.column_config.TextColumn("Nombre", help="Descripcion del Producto", max_chars=300),
    "precio": st.column_config.NumberColumn("Precio (COP)", help="Precio del Producto", min_value=0),
    "cantidad": st.column_config.NumberColumn("Cantidad", help="Cantidad del Producto", min_value=0),
    "descripcion": st.column_config.TextColumn("Descripcion", help="Descripcion del Producto", max_chars=300),
}

if "selected_products" not in st.session_state:
    st.session_state.selected_products = {}

if "searched_products" not in st.session_state:
    st.session_state.searched_products = None



def update_selected_products(event, df):

    products = event.selection.rows
    filtered = df.iloc[products]

    for index, row in filtered.iterrows():
        ide = row['id']
        nombre = row['nombre']
        if ide not in st.session_state.selected_products:
            st.session_state.selected_products[ide] = nombre

    dic = st.session_state.selected_products
    
    dic


with tab1:
    with st.container():

        col1_add,col2_search = st.columns([10,8])

        with col1_add:
            with st.form("stock-add-form"):
                col2, col3 = st.columns([3,1])
                with col2:
                    prompt_id = st.text_input("Hello",value="",placeholder="Enter Stock Code",label_visibility="collapsed") # Buscar por ID.
                with col3:
                    submitid = st.form_submit_button("Find")
        
        with col2_search:
            with st.form("stock-search-form"):
                col2, col3 = st.columns([3,1])
                with col2:
                    prompt_name = st.text_input("Hello",value="",placeholder="Enter Stock Name",label_visibility="collapsed") # Buscar por nombre.
                with col3:
                    submitname = st.form_submit_button("Find")

    with st.container():
        refresh = st.button("Refresh")

        df = st.session_state.searched_products

        if refresh or submitid or submitname: # Si el usuario refresca la info o inicia una búsqueda con filtro.
            if submitid and prompt_id != "":
                df = connect.query(f"SELECT * FROM productos WHERE id={prompt_id}")
            elif submitname and prompt_name != "":
                df = connect.query(f"SELECT * FROM productos WHERE nombre LIKE '%{prompt_name}%'")
            else:
                df = connect.query("SELECT * FROM productos") # Cargar todos los productos.

            st.session_state.searched_products =  df


        event = st.dataframe(pd.DataFrame(df),use_container_width=True,hide_index=True,on_select="rerun",selection_mode="multi-row")
    

        st.header("Productos Seleccionados")
        update_selected_products(event,df)

        

with tab2:
    st.header("Sales")
with tab3:
    st.header("Reports")
with tab4:
    st.header("Settings")
