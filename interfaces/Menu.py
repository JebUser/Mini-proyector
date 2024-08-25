import streamlit as st

def mostrar_inicio():
    return """
        ## Bienvenid@ a nuestro proyecto de sistema POS\n
        ### El proyecto fue elaborado por:
        * Juan Esteban Becerra Gutiérrez
        *  * 
        * Alejandro Sarmiento
        *  * 
        * Maria José Pava Echeverri
        *  * 
        * José Daniel Ramirez
        *  * 
        * Matero Ramirez
        *
        """

st.header("Menu")
st.write(f"Bienvenido {st.session_state.role}.")
st.write(mostrar_inicio())