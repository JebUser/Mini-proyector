import streamlit as st
from connection import connect

# Definición de usuarios y contraseñas (esto debería estar encriptado y almacenado en una base de datos en un entorno real)
# Verificar credenciales en la base de datos
# Cargar todos los usuarios y roles desde la base de datos
# Verificar credenciales en la base de datos
def check_credentials(username, password):
    query = f" SELECT u.usuario, u.contrasena, r.nombre as rol FROM usuarios u JOIN rol r ON u.rol_id = r.id WHERE u.usuario =\"{username}\" "
    result = connect.query(query)
        # Mostramos el DataFrame en Streamlit (opcional)
    st.dataframe(result)
    
    # Nos aseguramos de que hay un resultado
    if not result.empty:
        # Comparamos la contraseña
        if result["contrasena"].iloc[0] == password:
            return result["rol"].iloc[0]
    return None

def login():
    st.header("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        role = check_credentials(username, password)
        if role:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.success(f"Bienvenido {username}!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

#Salir de sesion
def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.cache_data.clear()
    st.rerun()

# Asignación de rol y autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None


role = st.session_state.role
#Paginas predeterminadas
logout_page = st.Page(logout, title="Salir", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

#Paginas para todos los roles
Menu = st.Page(
    "interfaces/Menu.py",
    title="Menu",
    icon=":material/help:",
    default=True,
)
historial = st.Page(
    "interfaces/Historial.py",
    title="Historial de ventas",
    icon=":material/help:",
)
registrar_ventas = st.Page(
    "interfaces/Registrar_ventas.py", 
    title="Registro de ventas", 
    icon=":material/bug_report:",
)
reportes = st.Page(
    "interfaces/Reportes.py", 
    title="Reportes", 
    icon="📊",
)
superusuario = st.Page(
    "interfaces/Superusuario.py",
    title="Gestion de DB",
    icon="🔧"
)

#Paginas para cada rol
account_pages = [logout_page, settings]
empleado_pages = [Menu, registrar_ventas, reportes]
admin_pages = [Menu, historial, registrar_ventas, reportes]
superuser_pages = [Menu, historial, registrar_ventas, reportes, superusuario]

st.title("POS Javeriana")

#Genera un diccionario general en que se asignan las paginas a cada rol
page_dict = {}
if st.session_state.role == "Vendedor":
    page_dict["Vendedor"] = empleado_pages
elif st.session_state.role == "Administrador":
    page_dict["Administrador"] = admin_pages
elif st.session_state.role == "Superusuario":
    page_dict["Superusuario"] = superuser_pages

#Despliega las paginas por rol
if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()

