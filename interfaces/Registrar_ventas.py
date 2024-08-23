import streamlit as st
from connection import connect
tab1, tab2, tab3,tab4 = st.tabs(["Till", "Sales", "Reports","Settings"])

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
        if refresh or submitid or submitname: # Si el usuario refresca la info o inicia una búsqueda con filtro.
            if submitid and prompt_id != "":
                data = connect.query(f"SELECT * FROM productos WHERE id={prompt_id}")
                st.dataframe(data)
            elif submitname and prompt_name != "":
                data = connect.query(f"SELECT * FROM productos WHERE nombre LIKE '%{prompt_name}%'")
                st.dataframe(data)
            else:
                data = connect.query("SELECT * FROM productos") # Cargar todos los productos.
                st.dataframe(data)

with tab2:
    st.header("Sales")
with tab3:
    st.header("Reports")
with tab4:
    st.header("Settings")
