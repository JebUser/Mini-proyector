import streamlit as st


# Create the form
with st.form("My form"):
    st.markdown("### JavePOS")  

    first = st.text_input("User", key="user")
    last = st.text_input("Password", key="password", type="password")
    
    submit = st.form_submit_button("Submit")

   

# Apply additional custom CSS for the form
css = """
<style>
    [data-testid="stForm"] {
        background: #10B981;
        padding: 20px;
        border-radius: 30px;
    }
    [data-testid="stForm"] h3 {
        text-align: center;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)

