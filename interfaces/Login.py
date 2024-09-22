import streamlit as st

# Crear el formulario de login
with st.form("login_form"):
    st.markdown("### JavePOS")

    # Inputs para el nombre de usuario y contraseña
    username = st.text_input("Usuario", key="user")
    password = st.text_input("Contraseña", type="password", key="password")

    # Botón de submit
    submit = st.form_submit_button("Iniciar sesión", type="primary")

# Lógica para manejar el submit
if submit:
    # Aquí puedes agregar la lógica de autenticación
    st.success(f"Bienvenido {username}!")
