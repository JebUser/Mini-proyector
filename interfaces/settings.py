import streamlit as st
from connection import connect
from controller.hashed_pass import hash_password
from sqlalchemy import text
import time

st.header(f"Bienvenid@ {st.session_state.username}")
st.write(f"Tu sesión es de {st.session_state.role}.")

st.subheader("Ajustes")

# CopyPaste de Registrar ventas, para el boton de añadir entradas a una tabla
def insert_data(query, get_id=False):
    if get_id:
        data = connect.session.execute(text(query)).lastrowid
        return data
    else:
        connect.session.execute(text(query))
        return None

with st.container():
    col1, col2 = st.columns([10, 10])

    query = f" SELECT u.nombre1, u.nombre2, u.apellido1, u.apellido2, u.contrasena, u.correo, u.cc from usuarios u WHERE u.usuario =\"{st.session_state.username}\" "
    data = connect.query(query)
    
    with col1:
        u_nombre1_input = st.text_input("Nombre 1:", max_chars=50, value=data['nombre1'].iloc[0])
        u_nombre2_input = st.text_input("Nombre 2:", max_chars=50, value=data['nombre2'].iloc[0])
        u_apellido1_input = st.text_input("Apellido 1:", max_chars=50, value=data['apellido1'].iloc[0])
        u_apellido2_input = st.text_input("Apellido 2:", max_chars=50, value=data['apellido2'].iloc[0])

    with col2:
        u_contrasena_input = st.text_input("Nueva Contraseña:", max_chars=100, type="password")
        u_contrasena_input_2 = st.text_input("Confirmar Contraseña:", max_chars=100, type="password")
        u_correo_input = st.text_input("Correo:", max_chars=150, value=data['correo'].iloc[0])
        u_cc_input = st.number_input("C.C:", min_value=0, max_value=2147483647, value=data['cc'].iloc[0])

with st.container():
    edit_button = st.button("Edit")
    if edit_button:
        if u_contrasena_input == u_contrasena_input_2:
            hashed_password = hash_password(u_contrasena_input)
            edit_query = f"UPDATE usuarios SET nombre1='{u_nombre1_input}', nombre2='{u_nombre2_input}', apellido1='{u_apellido1_input}', apellido2='{u_apellido2_input}', contrasena='{hashed_password.decode('utf-8')}', correo='{u_correo_input}', cc={u_cc_input} WHERE usuario = \"{st.session_state.username}\""

            with st.spinner("Actualizando..."):
                # Wait for 3 seconds (simulate a process)
                insert_data(edit_query)
                time.sleep(3)
                st.success("Datos actualizados")
                time.sleep(1)

            st.cache_data.clear()
            st.rerun()
        else:
            st.error("¡Las contraseñas digitadas no coinciden!")