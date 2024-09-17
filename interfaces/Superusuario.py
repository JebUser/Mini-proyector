import streamlit as st
from connection import connect
from sqlalchemy import text

# CopyPaste de Registrar ventas, para el boton de añadir entradas a una tabla
def insert_data(query, get_id=False):
    if get_id:
        data = connect.session.execute(text(query)).lastrowid
        return data
    else:
        connect.session.execute(text(query))
        return None

get_db_name = connect.query("SELECT DATABASE();") 

table_list_query = f"""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema=\"{get_db_name.iat[0,0]}\";
"""

tables = connect.query(table_list_query) 

with st.container():
    col_select, col_refresh = st.columns([8, 2])
    with col_select:
        selected_table = st.selectbox('Choose a table to modify:', tables)
    with col_refresh:
        refresh_button = st.button("Refresh")
        if refresh_button:
            del st.session_state.selected_table
    col1_selectasterisk, col2_editor = st.columns([10, 10])
    with col1_selectasterisk:
        select_all_in_table = f"""
        SELECT * FROM {selected_table}
        """
        data = connect.query(select_all_in_table)
        if not data.empty:
            st.write("Table Data:")
            # TODO: Utilizar session states para reflejar los cambios hechos a la DB en vivo
            # Por ahora toca irse a otra pestaña (Historial de ventas) y volver a esta para que se vean los cambios
            st.dataframe(data)
        else:
            st.write("The selected table has no data entries.")
    with col2_editor:
        # Se viene una ola de espagueti que no se como evitar!!!!! :D
        # Inputs marcados con (*) es porque no pueden ser nulos a la hora de añadirlos a la base de datos
        if selected_table == "cliente":
            c_cedula_input = st.number_input("(*) Cedula:", min_value=0, max_value=2147483647, value=1, step=1)
            c_nombre_input = st.text_input("(*) Nombre:")
            c_correo_input = st.text_input("(*) Correo:")
        elif selected_table == "prod_venta":
            pv_nventa_input = st.number_input("(*) NroVenta:", min_value=0, max_value=2147483647, value=1, step=1)
            pv_idprod_input = st.number_input("(*) ID_Producto:", min_value=0, max_value=2147483647, value=0, step=1)
            pv_cantidad_input = st.number_input("(*) Cantidad:", min_value=0, max_value=2147483647, value=0, step=1)
        elif selected_table == "productos":
            p_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=0, step=1)
            p_nombre_input = st.text_input("Nombre:")
            p_precio_input = st.number_input("Precio:")
            p_cantidad_input = st.number_input("Cantidad:", min_value=0, max_value=2147483647, value=0, step=1)
            p_descripcion_input = st.text_input("Descripcion:")
        elif selected_table == "rol":
            r_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=0, step=1)
            r_nombre_input = st.text_input("Nombre:")
        elif selected_table == "usuarios":
            u_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=0, step=1)
            u_nombre1_input = st.text_input("Nombre 1:")
            u_nombre2_input = st.text_input("Nombre 2:")
            u_apellido1_input = st.text_input("Apellido 1:")
            u_apellido2_input = st.text_input("Apellido 2:")
            u_usuario_input = st.text_input("Usuario:")
            u_contrasena_input = st.text_input("Contrasena:")
            u_correo_input = st.text_input("Correo:")
            u_cc_input = st.number_input("C.C:", min_value=0, max_value=2147483647, value=0, step=1)
            u_rol_id_input = st.number_input("Rol ID:", min_value=0, max_value=2147483647, value=0, step=1)
        elif selected_table == "venta":
            v_nventa_input = st.number_input("(*) NroVenta:", min_value=0, max_value=2147483647, value=1, step=1)
            v_idcliente_input = st.number_input("(*) ID Cliente:", min_value=0, max_value=2147483647, value=0, step=1)
            v_idempleado_input = st.number_input("(*) ID Empleado:", min_value=0, max_value=2147483647, value=0, step=1)
            v_fecha_input = st.date_input("(*) Fecha:", value=None)

    add_part, edit_part, delete_part = st.columns(3)
    with add_part:
        add_button = st.button("Add")
        add_query = ""
        if add_button:
            # Antes de que me tiren hate por el espagueti:
            # Intenté hacer una implementación mas simplificada usando un diccionario para definir cada caso de querys en funcion al selected_table,
            # pero streamlit es chistosito y me mandaba error que porque las variables de input de las demás tablas no estaban definidas... xdn't
            if selected_table == "cliente":
                add_query = f"INSERT INTO cliente (Cedula, Nombre, Correo) VALUES ({c_cedula_input}, '{c_nombre_input}', '{c_correo_input}')"
            elif selected_table == "prod_venta":
                add_query = f"INSERT INTO prod_venta (NroVenta, ID_Producto, Cantidad) VALUES ({pv_nventa_input}, {pv_idprod_input}, {pv_cantidad_input})"
            elif selected_table == "productos":
                add_query = f"INSERT INTO productos (id, nombre, precio, cantidad, descripcion) VALUES ({p_id_input}, '{p_nombre_input}', {p_precio_input}, {p_cantidad_input}, '{p_descripcion_input}')"
            elif selected_table == "rol":
                add_query = f"INSERT INTO rol (id, nombre) VALUES ({r_id_input}, '{r_nombre_input}')"
            elif selected_table == "usuarios":
                add_query = f"INSERT INTO usuarios (id, nombre1, nombre2, apellido1, apellido2, usuario, contrasena, correo, cc, rol_id) VALUES ({u_id_input}, '{u_nombre1_input}', '{u_nombre2_input}', '{u_apellido1_input}', '{u_apellido2_input}', '{u_usuario_input}', '{u_contrasena_input}', '{u_correo_input}', {u_cc_input}, {u_rol_id_input})"
            elif selected_table == "venta":
                add_query = f"INSERT INTO venta (NroVenta, ID_Cliente, ID_Empleado, Fecha) VALUES ({v_nventa_input}, {v_idcliente_input}, {v_idempleado_input}, {v_fecha_input})"
            insert_data(add_query)
    with edit_part:
        edit_button = st.button("Edit")
        edit_query = ""
        if edit_button:
            if selected_table == "cliente":
                edit_query = f"UPDATE cliente SET Nombre='{c_nombre_input}', Correo='{c_correo_input}' WHERE Cedula={c_cedula_input}"
            elif selected_table == "prod_venta":
                edit_query = f"UPDATE prod_venta SET Cantidad={pv_cantidad_input} WHERE NroVenta={pv_nventa_input} AND ID_Producto={pv_idprod_input}"
            elif selected_table == "productos":
                edit_query = f"UPDATE productos SET nombre='{p_nombre_input}', precio={p_precio_input}, cantidad={p_cantidad_input}, descripcion='{p_descripcion_input}' WHERE id={p_id_input}"
            elif selected_table == "rol":
                edit_query = f"UPDATE rol SET nombre='{r_nombre_input}' WHERE id={r_id_input}"
            elif selected_table == "usuarios":
                edit_query = f"UPDATE usuarios SET nombre1='{u_nombre1_input}', nombre2='{u_nombre2_input}', apellido1='{u_apellido1_input}', apellido2='{u_apellido2_input}', usuario='{u_usuario_input}', contrasena='{u_contrasena_input}', correo='{u_correo_input}', cc={u_cc_input}, rol_id={u_rol_id_input} WHERE id={u_id_input}"
            elif selected_table == "venta":
                edit_query = f"UPDATE venta SET ID_Cliente={v_idcliente_input}, ID_Empleado={v_idempleado_input}, Fecha='{v_fecha_input}', WHERE NroVenta={v_nventa_input}"
            insert_data(edit_query)
    with delete_part:
        delete_button = st.button("Delete")
        delete_query = ""
        if delete_button:
            if selected_table == "cliente":
                delete_query = f"DELETE FROM cliente WHERE Cedula={c_cedula_input}"
            elif selected_table == "prod_venta":
                delete_query = f"DELETE FROM prod_venta WHERE NroVenta={pv_nventa_input} AND ID_Producto={pv_idprod_input}"
            elif selected_table == "productos":
                delete_query = f"DELETE FROM productos WHERE id={p_id_input}"
            elif selected_table == "rol":
                delete_query = f"DELETE FROM rol WHERE id={r_id_input}"
            elif selected_table == "usuarios":
                delete_query = f"DELETE FROM usuarios WHERE id={u_id_input}"
            elif selected_table == "venta":
                delete_query = f"DELETE FROM venta WHERE NroVenta={v_nventa_input}"
            insert_data(delete_query)