import streamlit as st


pg = st.navigation([
    st.Page("interfaces/Historial.py", title="Historial de Ventas"),
    st.Page("interfaces/Registrar_ventas.py", title="Venta"),
    st.Page("interfaces/Login.py", title="Login")
])

st.set_page_config(page_title="POS", page_icon=":material/edit:")

pg.run()
