import streamlit as st

def mostrar_inicio():
    return """
        ## Bienvenid@ a nuestro proyecto de sistema POS\n
        ### El proyecto fue elaborado por:
        * Juan Esteban Becerra Gutiérrez

        * Alejandro Sarmiento
       
        * Maria José Pava Echeverry
      
        * José Daniel Ramirez

        * Mateo Ramirez

        """

st.header("Menu")
st.write(f"Bienvenido {st.session_state.role}.")
st.write(mostrar_inicio())