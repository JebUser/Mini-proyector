import streamlit as st



connect = st.connection("mydb",type="sql",autocommit=True) # Los datos de conexión se encuentran en .streamlit/secrets.toml