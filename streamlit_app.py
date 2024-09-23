import streamlit as st
from connection import connect
import bcrypt
import base64

# Función para aplicar personalización global, incluyendo colores persistentes y el ícono
def apply_customization():
    # Si hay color de botones personalizado en la sesión, lo usamos, si no, el predeterminado
    button_color = st.session_state.get("button_color", "#4233ff")

    # Convertir el color hexadecimal en RGBA con transparencia del 50%
    def hex_to_rgba(hex_color, alpha=0.5):
        hex_color = hex_color.lstrip('#')  # Eliminar el "#" inicial si está presente
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  # Convertir a RGB
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"  # Retornar en formato rgba con alpha

    # Color del fondo del formulario con transparencia
    rgba_button_color = hex_to_rgba(button_color, 0.5)

    # Aplicar el estilo con transparencia al fondo del formulario
    st.markdown(f"""
        <style>
        /* Aplicar color personalizado a los botones */
        .stButton>button {{
            background-color: {button_color};
            color: white;
        }}
        
        /* Estilo del formulario con transparencia en el fondo */
        [data-testid="stForm"] {{
            background: {rgba_button_color};  /* Fondo del formulario con transparencia */
            padding: 30px;
            border-radius: 20px;
        }}
        [data-testid="stForm"] h2 {{
            text-align: center;
            color: black;  /* Cambia el color del texto del título */
        }}
        h1 {{
            color: {button_color};  /* Cambia el color del título principal */
            text-align: center;
        }}
        [data-testid="stForm"] input {{
            width: 90% !important;
            border-radius: 10px !important;
            padding: 10px !important;
            margin-bottom: 10px !important;
        }}
        [data-testid="stTitle"] {{
            color: {button_color};
            text-align: center;
            margin-bottom: 20px;
        }}

        /* Degradado radial desde la esquina inferior derecha */
        .gradient-background {{
            background: radial-gradient(circle at bottom right, {button_color}, rgba(255, 255, 255, 0) 25%);
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;  /* Para que quede detrás del contenido */
        }}

        /* Asegurar que los contenedores principales sean transparentes */
        .stApp {{
            background-color: transparent;
        }}
        
        .block-container {{
            background-color: transparent;
        }}

        /* Ubicación y estilo de la imagen en la esquina inferior derecha */
        .bottom-right-image {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 9vw;  /* El tamaño del ícono será del 15% del ancho de la ventana */
            max-width: 200px;  /* El ícono no será más grande que 200px */
            height: auto;
        }}

        /* Reducir aún más el tamaño si la pantalla es más pequeña */
        @media (max-width: 600px) {{
            .bottom-right-image {{
                width: 7vw;  /* El tamaño del ícono será del 10% del ancho de la ventana en pantallas pequeñas */
                max-width: 100px;  /* Limitar el tamaño máximo a 100px en pantallas pequeñas */
            }}
        }}
        </style>
        """, unsafe_allow_html=True)

    # Mostrar el ícono si se ha subido
    if 'icon_image' in st.session_state and st.session_state.icon_image is not None:
        st.markdown(f'<img src="data:image/png;base64,{st.session_state.icon_image}" class="bottom-right-image">', unsafe_allow_html=True)

    # Agregar el div que aplica el degradado en el fondo
    st.markdown('<div class="gradient-background"></div>', unsafe_allow_html=True)






# Función para permitir la subida del ícono (solo para superusuarios)
def upload_icon():
    if st.session_state.role == "Superusuario":
        uploaded_file = st.sidebar.file_uploader("Sube un ícono (imagen) para todas las páginas", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            # Leer el archivo de la imagen
            bytes_data = uploaded_file.read()
            
            # Convertir la imagen a base64
            encoded_image = base64.b64encode(bytes_data).decode("utf-8")
            
            # Guardar la imagen codificada en base64 en session_state
            st.session_state.icon_image = encoded_image


# Nueva funcionalidad: Menú para personalización de color de botones (solo Superusuario)
def customization_menu():
    if st.session_state.role == "Superusuario":
        with st.sidebar:
            st.markdown("## Personalización de los Botones")
            
            # Panel de selección de color (hexadecimal) para los botones
            color_hex = st.color_picker("Escoge un color para los botones", "#4233ff")
            
            # Guardar el color seleccionado en la sesión
            st.session_state["button_color"] = color_hex
            
            st.success(f"Color aplicado a los botones!")



# Definición de usuarios y contraseñas
def check_credentials(username, password):
    query = f" SELECT u.usuario, u.contrasena, r.nombre as rol FROM usuarios u JOIN rol r ON u.rol_id = r.id WHERE u.usuario =\"{username}\" "
    result = connect.query(query)
    
    # Nos aseguramos de que hay un resultado
    if not result.empty:
        #Extraemos la hashed password
        stored_hashed_password = result["contrasena"].iloc[0].encode('utf-8')
        # Comparamos la contraseña
        #st.write(stored_hashed_password, password.encode('utf-8'))
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        #if stored_hashed_password == password.encode('utf-8'):
            return result["rol"].iloc[0]  # Return the user role if the password matches
        
    return None

def login():
    st.markdown("# Jave POS")
    
    with st.form("login_form"):
        st.markdown("## Iniciar Sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        columns = st.columns((2,1,2))
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        submit = columns[1].form_submit_button("Iniciar sesión", type="primary")
        
        if submit:
            role = check_credentials(username, password)
            if role:
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.username = username
                st.success(f"Bienvenido {username}!")
                st.cache_data.clear()
                st.rerun()
            elif username == '' or password == '':
                st.warning("Ingrese credenciales")
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.cache_data.clear()
    st.rerun()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None

role = st.session_state.role

logout_page = st.Page(logout, title="Salir", icon=":material/logout:")
settings = st.Page("interfaces/settings.py", title="Ajustes", icon=":material/settings:")

Menu = st.Page("interfaces/Menu.py", title="Menu", icon=":material/help:", default=True)
historial = st.Page("interfaces/Historial.py", title="Historial de ventas", icon=":material/help:")
registrar_ventas = st.Page("interfaces/Registrar_ventas.py", title="Registro de ventas", icon=":material/bug_report:")
reportes = st.Page("interfaces/Reportes.py", title="Reportes", icon="📊")
superusuario = st.Page("interfaces/Superusuario.py", title="Gestion de DB", icon="🔧")

account_pages = [logout_page, settings]
empleado_pages = [Menu, registrar_ventas, reportes]
admin_pages = [Menu, historial, registrar_ventas, reportes]
superuser_pages = [Menu, historial, registrar_ventas, reportes, superusuario]

page_dict = {}
if st.session_state.role == "Vendedor":
    page_dict["Vendedor"] = empleado_pages
elif st.session_state.role == "Administrador":
    page_dict["Administrador"] = admin_pages
elif st.session_state.role == "Superusuario":
    page_dict["Superusuario"] = superuser_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

# Agregar la funcionalidad de personalización
upload_icon()  # Permite subir un ícono solo para superusuarios
apply_customization()  # Aplica la paleta de colores y muestra el ícono grande en el costado derecho inferior

# Mostrar el menú de personalización de botones solo para Superusuario debajo del ícono
customization_menu()

pg.run()
