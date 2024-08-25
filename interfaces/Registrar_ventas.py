import streamlit as st
import pandas as pd
from connection import connect

tab1, tab2, tab3, tab4 = st.tabs(["Till", "Sales", "Reports", "Settings"])

# Inicialización de estados en Streamlit
if "selected_products" not in st.session_state:
    st.session_state.selected_products = {}

if "searched_products" not in st.session_state:
    st.session_state.searched_products = None

def add_product_to_selection(product_id, product_name, quantity=1):
    st.session_state.selected_products[product_id] = {
        "name": product_name,
        "quantity": quantity
    }

def update_selected_products(selected_rows, df):
    for row_idx in selected_rows:
        row = df.iloc[row_idx]
        product_id = row['id']
        product_name = row['nombre']
        if product_id not in st.session_state.selected_products:
            add_product_to_selection(product_id, product_name)

def execute_query(query):
    connect.query(query)
    connect.commit() 

def display_selected_products():
    st.subheader("Productos Seleccionados")
    if st.session_state.selected_products:
        total = 0
        for product_id, details in st.session_state.selected_products.items():
            col1, col2, col3 = st.columns([6, 2, 2])
            col1.write(details["name"])
            quantity = col2.number_input(f"Cantidad ({details['name']})", min_value=1, value=details["quantity"], key=f"qty_{product_id}")
            details["quantity"] = quantity
            precio = connect.query(f"SELECT precio FROM productos WHERE id={product_id}").iloc[0]['precio']
            subtotal = precio * quantity
            col3.write(f"Subtotal: {subtotal} COP")
            total += subtotal
        st.write(f"Total: {total} COP")
    else:
        st.write("No hay productos seleccionados.")

with tab1:
    with st.container():
        col1_add, col2_search = st.columns([10, 8])

        with col1_add:
            with st.form("stock-add-form"):
                col2, col3 = st.columns([3, 1])
                with col2:
                    prompt_id = st.text_input("Buscar por ID", value="", placeholder="Ingrese código de producto", label_visibility="collapsed")
                with col3:
                    submitid = st.form_submit_button("Buscar")

        with col2_search:
            with st.form("stock-search-form"):
                col2, col3 = st.columns([3, 1])
                with col2:
                    prompt_name = st.text_input("Buscar por Nombre", value="", placeholder="Ingrese nombre del producto", label_visibility="collapsed")
                with col3:
                    submitname = st.form_submit_button("Buscar")

    with st.container():
        refresh = st.button("Refrescar")

        if refresh or submitid or submitname:
            if submitid and prompt_id != "":
                df = connect.query(f"SELECT * FROM productos WHERE id={prompt_id}")
            elif submitname and prompt_name != "":
                df = connect.query(f"SELECT * FROM productos WHERE nombre LIKE '%{prompt_name}%'")
            else:
                df = connect.query("SELECT * FROM productos")

            st.session_state.searched_products = df

        df = st.session_state.searched_products
        if df is not None:
            selected_rows = st.multiselect("Selecciona productos", df.index, format_func=lambda x: f"{df.loc[x, 'nombre']} - {df.loc[x, 'id']}")
            update_selected_products(selected_rows, df)

    display_selected_products()

# Aquí continuarías con el código para la sección de Ventas, Reportes y Configuraciones...


# TAB 2: Sales (Registro de Ventas)
with tab2:
    st.header("Sales")

    # Selección de Cliente
    st.subheader("Cliente")
    with st.form("cliente-form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            cliente_cc = st.text_input("Cédula del Cliente", placeholder="Ingrese la cédula del cliente")
        with col2:
            buscar_cliente = st.form_submit_button("Buscar")

        if buscar_cliente and cliente_cc:
            try:
                # Convertir cliente_cc a entero para la consulta
                cliente_cc = int(cliente_cc)
                cliente_data = connect.query(f"SELECT * FROM Cliente WHERE Cedula={cliente_cc}")
                
                if not cliente_data.empty:
                    st.write(f"Cliente: {cliente_data.iloc[0]['Nombre']}, Correo: {cliente_data.iloc[0]['Correo']}")
                else:
                    st.warning("Cliente no encontrado. Puedes registrar un nuevo cliente.")
                    nuevo_nombre = st.text_input("Nombre del Cliente")
                    nuevo_correo = st.text_input("Correo del Cliente")
                    
                    # Aquí manejamos la lógica de registrar un nuevo cliente dentro del mismo formulario
                    registrar_cliente = st.form_submit_button("Registrar Cliente")

                    if registrar_cliente and nuevo_nombre and nuevo_correo:
                        connect.query(f"INSERT INTO Cliente (Cedula, Nombre, Correo) VALUES ({cliente_cc}, '{nuevo_nombre}', '{nuevo_correo}')")
                        st.success("Cliente registrado exitosamente")
                    elif registrar_cliente:
                        st.warning("Por favor, completa los campos de nombre y correo.")
            
            except ValueError:
                st.error("La cédula debe ser un número entero válido.")


    # Lista de Productos Seleccionados
    st.subheader("Productos Seleccionados")
    selected_products = st.session_state.selected_products

    if selected_products:
        for i, (prod_id, prod_info) in enumerate(selected_products.items()):
        # Acceso correcto al nombre del producto y a la cantidad
            prod_name = prod_info["name"]
            quantity = prod_info["quantity"]
            
            col1, col2 = st.columns([7, 3])
            col1.write(prod_name)
            
            # Usamos 'i' para asegurar una clave única para cada widget
            quantity = col2.number_input(f"Cantidad para {prod_name}", min_value=1, value=quantity, key=f"qty_{prod_id}_{i}")
            
            # Actualizar la cantidad en el diccionario de productos seleccionados
            st.session_state.selected_products[prod_id] = {
                "name": prod_name,
                "quantity": quantity
            }
    # Resumen de Venta y Confirmación
    st.subheader("Resumen de la Venta")
    total = 0
    if selected_products:
        for prod_id, details in selected_products.items():
            prod_name = details["name"]
            qty = details["quantity"]
            precio = connect.query(f"SELECT precio FROM productos WHERE id={prod_id}").iloc[0]['precio']
            subtotal = precio * qty
            st.write(f"{prod_name}: {qty} x {precio} = {subtotal} COP")
            total += subtotal

        st.write(f"Total: {total} COP")

    if st.button("Confirmar Venta"):
        try:
            # Registrar la venta y actualizar inventario
            for prod_id, details in st.session_state.selected_products.items():
                qty = details["quantity"]

                # Registrar la venta
                execute_query(f"""
                    INSERT INTO Venta (Fecha, IDProducto, IDEmpleado, cantidad, Comprador)
                    VALUES (CURRENT_DATE, {prod_id}, {1}, {qty}, {cliente_cc})
                """)
                
                # Actualizar la cantidad de productos en la tabla productos
                execute_query(f"""
                    UPDATE productos
                    SET cantidad = cantidad - {qty}
                    WHERE id = {prod_id}
                """)
            
            st.success("Venta confirmada")
            st.session_state.selected_products.clear()  # Limpiar productos seleccionados después de confirmar la venta
        except Exception as e:
            st.error(f"Error al registrar la venta: {e}")


with tab3:
    st.header("Reports")
with tab4:
    st.header("Settings")
