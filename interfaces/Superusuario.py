import streamlit as st
from connection import connect
from sqlalchemy import text
from controller.hashed_pass import hash_password

# CopyPaste de Registrar ventas, para el boton de añadir entradas a una tabla
def insert_data(query, get_id=False):
    if get_id:
        data = connect.session.execute(text(query)).lastrowid
        return data
    else:
        connect.session.execute(text(query))
        return None

get_db_name = connect.query("SELECT DATABASE();") 

#Function to hash password

table_list_query = f"""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema=\"{get_db_name.iat[0,0]}\";
"""

tables = connect.query(table_list_query) 

if "table_data" not in st.session_state:
    st.session_state.table_data = None

with st.container():
    col_select, col_refresh = st.columns([8, 2])
    with col_select:
        selected_table = st.selectbox('Choose a table to modify:', tables)
    with col_refresh:
        refresh_button = st.button("Refresh")
        # Puede que se tome un poco en ver los cambios
        if refresh_button:
            del st.session_state.table_data
    col1_selectasterisk, col2_editor = st.columns([10, 10])
    with col1_selectasterisk:
        select_all_in_table = f"""
        SELECT * FROM {selected_table}
        """
        data = connect.query(select_all_in_table)
        if not data.empty:
            st.write("Table Data:")
            st.dataframe(data)
        else:
            st.write("The selected table has no data entries.")
    with col2_editor:
        # Se viene una ola de espagueti que no se como evitar!!!!! :D
        # Inputs marcados con (*) es porque no pueden ser nulos a la hora de añadirlos a la base de datos
        if selected_table.lower() == "cliente":
            c_cedula_input = st.number_input("(*) Cedula:", min_value=0, max_value=2147483647, value=1, step=1)
            c_nombre_input = st.text_input("(*) Nombre:", max_chars=50, value=data.loc[data['Cedula'] == c_cedula_input, 'Nombre'].values[0] if (data["Cedula"] == c_cedula_input).any() else "")
            c_correo_input = st.text_input("(*) Correo:", max_chars=50, value=data.loc[data['Cedula'] == c_cedula_input, 'Correo'].values[0] if (data["Cedula"] == c_cedula_input).any() else "")
        elif selected_table == "prod_venta":
            pv_nventa_input = st.number_input("(*) NroVenta:", min_value=0, max_value=2147483647, value=1, step=1)
            pv_idprod_input = st.number_input("(*) ID_Producto:", min_value=0, max_value=2147483647, value=data.loc[data['NroVenta'] == pv_nventa_input, 'ID_Producto'].values[0] if (data['NroVenta'] == pv_nventa_input).any() else 0, step=1)
            pv_cantidad_input = st.number_input("(*) Cantidad:", min_value=0, max_value=2147483647, value=data.loc[data['NroVenta'] == pv_nventa_input, 'Cantidad'].values[0] if (data['NroVenta'] == pv_nventa_input).any() else 0, step=1)
        elif selected_table == "productos":
            p_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=1, step=1)
            p_nombre_input = st.text_input("Nombre:", max_chars=200, value=data.loc[data['id'] == p_id_input, 'nombre'].values[0] if (data['id'] == p_id_input).any() else "")
            p_precio_input = st.number_input("Precio:", value=data.loc[data['id'] == p_id_input, 'precio'].values[0] if (data['id'] == p_id_input).any() else 0.0)
            p_cantidad_input = st.number_input("Cantidad:", min_value=0, max_value=2147483647, value=data.loc[data['id'] == p_id_input, 'cantidad'].values[0] if (data['id'] == p_id_input).any() else 0, step=1)
            p_descripcion_input = st.text_area("Descripcion:", max_chars=500, value=data.loc[data['id'] == p_id_input, 'descripcion'].values[0] if (data['id'] == p_id_input).any() else "")
        elif selected_table == "rol":
            r_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=1, step=1)
            r_nombre_input = st.text_input("Nombre:", max_chars=50, value=data.loc[data['id'] == r_id_input, 'nombre'].values[0] if (data['id'] == r_id_input).any() else "")
        elif selected_table == "usuarios":
            u_id_input = st.number_input("(*) ID:", min_value=0, max_value=2147483647, value=1, step=1)
            u_nombre1_input = st.text_input("Nombre 1:", max_chars=50, value=data.loc[data['id'] == u_id_input, 'nombre1'].values[0] if (data['id'] == u_id_input).any() else "")
            u_nombre2_input = st.text_input("Nombre 2:", max_chars=50, value=data.loc[data['id'] == u_id_input, 'nombre2'].values[0] if (data['id'] == u_id_input).any() else "")
            u_apellido1_input = st.text_input("Apellido 1:", max_chars=50, value=data.loc[data['id'] == u_id_input, 'apellido1'].values[0] if (data['id'] == u_id_input).any() else "")
            u_apellido2_input = st.text_input("Apellido 2:", max_chars=50, value=data.loc[data['id'] == u_id_input, 'apellido2'].values[0] if (data['id'] == u_id_input).any() else "")
            u_usuario_input = st.text_input("Usuario:", max_chars=100, value=data.loc[data['id'] == u_id_input, 'usuario'].values[0] if (data['id'] == u_id_input).any() else "")
            u_contrasena_input = st.text_input("Contrasena:", max_chars=100)
            u_correo_input = st.text_input("Correo:", max_chars=150, value=data.loc[data['id'] == u_id_input, 'correo'].values[0] if (data['id'] == u_id_input).any() else "")
            u_cc_input = st.number_input("C.C:", min_value=0, max_value=2147483647, value=data.loc[data['id'] == u_id_input, 'cc'].values[0] if (data['id'] == u_id_input).any() else 0, step=1)
            u_rol_id_input = st.number_input("Rol ID:", min_value=0, max_value=2147483647, value=data.loc[data['id'] == u_id_input, 'rol_id'].values[0] if (data['id'] == u_id_input).any() else 0, step=1)
        elif selected_table == "venta":
            v_nventa_input = st.number_input("(*) NroVenta:", min_value=0, max_value=2147483647, value=1, step=1)
            v_idcliente_input = st.number_input("(*) ID Cliente:", min_value=0, max_value=2147483647, value=data.loc[data['NroVenta'] == v_nventa_input, 'ID_Cliente'].values[0] if (data['NroVenta'] == v_nventa_input).any() else 0, step=1)
            v_idempleado_input = st.number_input("(*) ID Empleado:", min_value=0, max_value=2147483647, value=data.loc[data['NroVenta'] == v_nventa_input, 'ID_Empleado'].values[0] if (data['NroVenta'] == v_nventa_input).any() else 0, step=1)
            v_fecha_input = st.date_input("(*) Fecha:", value=data.loc[data['NroVenta'] == v_nventa_input, 'Fecha'].values[0] if (data['NroVenta'] == v_nventa_input).any() else None)

    add_part, edit_part, delete_part = st.columns(3)
    with add_part:
        add_button = st.button("Add")
        if add_button:
            
            # Guardas de seguridad: Este botón no hace nada si no se han llenado los campos necesarios
            add_query = ""
            if selected_table.lower() == "cliente" and c_cedula_input != 0 and c_nombre_input != "" and c_correo_input != "":
                add_query = f"INSERT INTO {selected_table} (Cedula, Nombre, Correo) VALUES ({c_cedula_input}, '{c_nombre_input}', '{c_correo_input}')"
            elif selected_table == "prod_venta" and pv_nventa_input != 0 and pv_idprod_input != 0 and pv_cantidad_input != 0:
                add_query = f"INSERT INTO {selected_table} (NroVenta, ID_Producto, Cantidad) VALUES ({pv_nventa_input}, {pv_idprod_input}, {pv_cantidad_input})"
            elif selected_table == "productos" and p_id_input != 0:
                add_query = f"INSERT INTO {selected_table} (id, nombre, precio, cantidad, descripcion) VALUES ({p_id_input}, '{p_nombre_input}', {p_precio_input}, {p_cantidad_input}, '{p_descripcion_input}')"
            elif selected_table == "rol" and r_id_input != 0:
                add_query = f"INSERT INTO {selected_table} (id, nombre) VALUES ({r_id_input}, '{r_nombre_input}')"
            elif selected_table == "usuarios" and u_id_input != 0:
                hashed_password = hash_password(u_contrasena_input)
                add_query = f"INSERT INTO {selected_table} (id, nombre1, nombre2, apellido1, apellido2, usuario, contrasena, correo, cc, rol_id) VALUES ({u_id_input}, '{u_nombre1_input}', '{u_nombre2_input}', '{u_apellido1_input}', '{u_apellido2_input}', '{u_usuario_input}', '{hashed_password.decode('utf-8')}', '{u_correo_input}', {u_cc_input}, {u_rol_id_input})"
            elif selected_table == "venta" and v_nventa_input != 0 and v_idcliente_input != 0 and v_idempleado_input != 0 and v_fecha_input != None:
                add_query = f"INSERT INTO {selected_table} (NroVenta, ID_Cliente, ID_Empleado, Fecha) VALUES ({v_nventa_input}, {v_idcliente_input}, {v_idempleado_input}, {v_fecha_input})"
            
            if add_query != "":
                insert_data(add_query)
                st.success("Usuario registrado correctamente")
            else:
                st.warning('Porfavor rellene los datos')
            
            st.cache_data.clear()
            st.rerun()
    with edit_part:
        edit_button = st.button("Edit")
        if edit_button:
            
            edit_query = ""
            if selected_table.lower() == "cliente" and c_cedula_input != 0:
                edit_query = f"UPDATE {selected_table} SET Nombre='{c_nombre_input}', Correo='{c_correo_input}' WHERE Cedula={c_cedula_input}"
            elif selected_table == "prod_venta" and pv_nventa_input != 0 and pv_idprod_input != 0:
                edit_query = f"UPDATE {selected_table} SET Cantidad={pv_cantidad_input} WHERE NroVenta={pv_nventa_input} AND ID_Producto={pv_idprod_input}"
            elif selected_table == "productos" and p_id_input != 0:
                edit_query = f"UPDATE {selected_table} SET nombre='{p_nombre_input}', precio={p_precio_input}, cantidad={p_cantidad_input}, descripcion='{p_descripcion_input}' WHERE id={p_id_input}"
            elif selected_table == "rol" and r_id_input != 0:
                edit_query = f"UPDATE {selected_table} SET nombre='{r_nombre_input}' WHERE id={r_id_input}"
            elif selected_table == "usuarios" and u_id_input != 0:
                hashed_password = hash_password(u_contrasena_input)
                edit_query = f"UPDATE {selected_table} SET nombre1='{u_nombre1_input}', nombre2='{u_nombre2_input}', apellido1='{u_apellido1_input}', apellido2='{u_apellido2_input}', usuario='{u_usuario_input}', contrasena='{hashed_password.decode('utf-8')}', correo='{u_correo_input}', cc={u_cc_input}, rol_id={u_rol_id_input} WHERE id={u_id_input}"
            elif selected_table == "venta" and v_nventa_input != 0:
                edit_query = f"UPDATE {selected_table} SET ID_Cliente={v_idcliente_input}, ID_Empleado={v_idempleado_input}, Fecha='{v_fecha_input}', WHERE NroVenta={v_nventa_input}"
            
            if edit_query != "":
                insert_data(edit_query)
                st.success("Datos actualizados")

            st.cache_data.clear()
            st.rerun()
    with delete_part:
        delete_button = st.button("Delete")
        if delete_button:
            delete_query = ""
            if selected_table.lower() == "cliente" and c_cedula_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE Cedula={c_cedula_input}"
            elif selected_table == "prod_venta" and pv_nventa_input != 0 and pv_idprod_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE NroVenta={pv_nventa_input} AND ID_Producto={pv_idprod_input}"
            elif selected_table == "productos" and p_id_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE id={p_id_input}"
            elif selected_table == "rol" and r_id_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE id={r_id_input}"
            elif selected_table == "usuarios" and u_id_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE id={u_id_input}"
            elif selected_table == "venta" and v_nventa_input != 0:
                delete_query = f"DELETE FROM {selected_table} WHERE NroVenta={v_nventa_input}"
            
            if delete_query != "":
                insert_data(delete_query)

            st.cache_data.clear()
            st.rerun()

st.cache_data.clear()