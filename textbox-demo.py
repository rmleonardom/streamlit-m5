import streamlit as st 

myname = st.text_input('nombre :')

if (myname):
    st.write(f"Tu nombre es : {myname}")


