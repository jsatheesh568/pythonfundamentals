import streamlit as st

st.title("PyAutoGUI Streamlit Demo")
st.write("This is a simple Streamlit app to demonstrate PyAutoGUI functionality.")

name = st.text_input("Enter your name:")
if st.button("Greet Me"):
    if name:
        st.success(f"Hello, {name}! Welcome to the PyAutoGUI Streamlit Demo.")
    else:
        st.error("Please enter your name to be greeted.")

st.write("You can extend this app to include more PyAutoGUI features!")

