import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "Empleado"]


def login():

    st.header("Bienvenido")
    role = st.selectbox("Selecciona tu rol", ROLES)

    if st.button("Iniciar sesión"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Salir", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
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

account_pages = [logout_page, settings]
empleado_pages = [Menu, historial, registrar_ventas]
admin_pages = []

st.title("POS Javeriana")

page_dict = {}
if st.session_state.role in ["Empleado", "Admin"]:
    page_dict["Empleado"] = empleado_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
