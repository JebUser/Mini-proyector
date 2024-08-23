import streamlit as st

tab1, tab2, tab3,tab4 = st.tabs(["Till", "Sales", "Reports","Settings"])

with tab1:
    with st.container():

        col1_add,col2_search = st.columns([10,8])

        with col1_add:
            with st.form("stock-add-form"):
                col2, col3 = st.columns([3,1])
                with col2:
                    prompt_add = st.text_input("Hello",value="",placeholder="Enter Stock Code",label_visibility="collapsed")
                with col3:
                    submitted = st.form_submit_button("Add")
        
        with col2_search:
             with st.form("stock-search-form"):
                col2, col3 = st.columns([3,1])
                with col2:
                    prompt_add = st.text_input("Hello",value="",placeholder="Enter Stock Code",label_visibility="collapsed")
                with col3:
                    submitted = st.form_submit_button("Find")



    with st.container():
        st.write("Aquí se verá el dataframe con los datos de los productos")

with tab2:
    st.header("Sales")
with tab3:
    st.header("Reports")
with tab4:
    st.header("Settings")
