import streamlit as st
from connection import connect
from sqlalchemy import text

# Inicialización de estados en Streamlit
if "selected_products" not in st.session_state:
    st.session_state.selected_products = {}

if "searched_products" not in st.session_state:
    st.session_state.searched_products = None

if "new_client" not in st.session_state:
    st.session_state.new_client = False

#Agregar un producto seleccionado
def add_product_to_selection(product_id, product_name, quantity=1):
    st.session_state.selected_products[product_id] = {
        "name": product_name,
        "quantity": quantity
    }

#Actualiza los productos que han sido seleccionados
def update_selected_products(selected_rows, df):
    for row_idx in selected_rows:
        row = df.iloc[row_idx]
        product_id = row['id']
        product_name = row['nombre']
        if product_id not in st.session_state.selected_products:
            add_product_to_selection(product_id, product_name)


#ejecutar un query
def execute_query(query):
    connect.query(query)
    connect.commit() 

#verificamos si el usuario unde el boton para buscar algun producto
def search_check(refresh, submitid, submitname):
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

# Hacer una inserción y obtener el id resultante de esa inserción de ser requerido.
def insert_data(query, get_id=False):
    if get_id:
        data = connect.session.execute(text(query)).lastrowid
        return data
    else:
        connect.session.execute(text(query))
        return None

#confirmar una venta
def check_out(cliente_cc):
    if st.button("Confirmar Venta"):
        try:

            # Insertar en la tabla venta
            query = f"""
                INSERT INTO venta (ID_Cliente, ID_Empleado,Fecha)
                VALUES ({cliente_cc}, {1}, CURRENT_DATE)
            """
            # Obtener el número de la venta que se desea agregar.
            nro_venta = insert_data(query, get_id=True)

            # Registrar los productos de la venta en prod_venta y actualizar inventario
            for prod_id, details in st.session_state.selected_products.items():
                qty = details["quantity"]

                # Insertar en prod_venta
                query = f"""
                    INSERT INTO prod_venta (NroVenta, ID_Producto, Cantidad)
                    VALUES ({nro_venta}, {prod_id}, {qty})
                """
                insert_data(query)

                # Actualizar la cantidad de productos en la tabla productos
                query = f"""
                    UPDATE productos
                    SET cantidad = cantidad - {qty}
                    WHERE id = {prod_id}
                """
                insert_data(query)
            
            st.success("Venta confirmada")
            st.session_state.selected_products.clear()  # Limpiar productos seleccionados después de confirmar la venta
        except Exception as e:
            st.error(f"Error al registrar la venta: {e}")

#registrar un cliente
def registrar_cliente(cliente_cc):
    with st.form("cliente-register-form"):
        nuevo_nombre = st.text_input("Nombre del Cliente")
        nuevo_correo = st.text_input("Correo del Cliente")        
        # Aquí manejamos la lógica de registrar un nuevo cliente dentro del mismo formulario
        registrar_cliente = st.form_submit_button("Registrar Cliente")

        if registrar_cliente and nuevo_nombre and nuevo_correo and cliente_cc is not None:
            query = f"INSERT INTO Cliente (Cedula, Nombre, Correo) VALUES ({cliente_cc}, '{nuevo_nombre}', '{nuevo_correo}')"
            insert_data(query)
            st.success("Cliente registrado exitosamente")
        elif registrar_cliente:
            st.warning("Por favor, completa los campos de nombre y correo.")

#buscar cliente
def buscar_cliente():
    # Selección de Cliente
    st.subheader("Cliente")
    cliente_cc = None
    
    with st.form("cliente-form"):
        col1, col2 = st.columns([9,11])
        with col1:
            cliente_cc = st.text_input("Cédula del Cliente", placeholder="Ingrese la cédula del cliente")
        with col2:
            buscar_cliente = st.form_submit_button("Buscar")
        if buscar_cliente and cliente_cc:
            # Convertir cliente_cc a entero para la consulta
            cliente_cc = int(cliente_cc)
            cliente_data = connect.query(f"SELECT * FROM Cliente WHERE Cedula={cliente_cc}")
            if not cliente_data.empty:
                st.write(f"Cliente: {cliente_data.iloc[0]['Nombre']}, Correo: {cliente_data.iloc[0]['Correo']}")
                st.session_state.new_client = False
            else:
                st.warning("Cliente no encontrado. Puedes registrar un nuevo cliente abajo.")
                st.session_state.new_client = True

    if st.session_state.new_client == True:
        registrar_cliente(cliente_cc)
        
    return cliente_cc




#mostrar los productos que hayan sido seleccionados
def display_selected_products():
    st.subheader("Productos Seleccionados")
    if st.session_state.selected_products:
        for product_id, details in st.session_state.selected_products.items():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            col1.write(details["name"])
            quantity = col2.number_input(f"Cantidad ({details['name']})", min_value=1, value=details["quantity"], key=f"qty_{product_id}")
            details["quantity"] = quantity
            precio = connect.query(f"SELECT precio FROM productos WHERE id={product_id}").iloc[0]['precio']
            subtotal = precio * quantity
            col3.write(f"Subtotal: {subtotal} COP")

            # TODO: Hasta ahora se puede borrar, pero para que funcione, se debe borrar también del multiselect. Por favor corregir eso.
            # Posibilidad de eliminar un elemento de la selección.
            if col4.button('X', key=f"delete_{product_id}"):
                # Eliminar el producto y refrescar la página.
                del st.session_state.selected_products[product_id]
    else:
        st.write("No hay productos seleccionados.")

with st.container():
    col1_add, col2_search, col3_summary = st.columns([10, 10, 8])
    refresh = False
    submitname = ""
    submitid = ""
    
    with col1_add:
        with st.form("stock-add-form"):
            col2, col3 = st.columns([5, 5])
            with col2:
                prompt_id = st.text_input("Buscar por ID", value="", placeholder="Ingrese código de producto", label_visibility="collapsed")
            with col3:
                submitid = st.form_submit_button("Buscar")
        refresh = st.button("Refrescar")
        search_check(refresh, submitid, submitname)
        display_selected_products() 
    with col2_search:
        with st.form("stock-search-form"):
            col2, col3 = st.columns([5, 5])
            with col2:
                prompt_name = st.text_input("Buscar por Nombre", value="", placeholder="Ingrese nombre del producto", label_visibility="collapsed")
            with col3:
                submitname = st.form_submit_button("Buscar")
          
    with col3_summary:
        # Resumen de Venta y Confirmación
        st.subheader("Resumen de la Venta")
        total = 0
        cliente_cc = None
        if st.session_state.selected_products:
            for prod_id, details in st.session_state.selected_products.items():
                prod_name = details["name"]
                qty = details["quantity"]
                precio = connect.query(f"SELECT precio FROM productos WHERE id={prod_id}").iloc[0]['precio']
                subtotal = precio * qty
                st.write(f"{prod_name}: {qty} x {precio} = {subtotal} COP")
                total += subtotal

            st.metric(label="Total", value=total, delta=None, delta_color="normal", label_visibility="visible")
        

        #si hay algun cliente asociado lo retorna    
        cliente_cc = buscar_cliente()
        check_out(cliente_cc)

st.cache_data.clear()