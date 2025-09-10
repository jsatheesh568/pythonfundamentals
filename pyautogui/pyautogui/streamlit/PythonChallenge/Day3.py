import streamlit as st

st.set_page_config(page_title="Streamlit Calculator", layout="centered")

st.title("✨ Interactive Calculator ✨")

# Initialize session state for calculation history and current expression
if "history" not in st.session_state:
    st.session_state.history = []
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Function to handle button clicks
def handle_click(key):
    if key == "=":
        try:
            result = str(eval(st.session_state.expression))
            st.session_state.history.append(f"{st.session_state.expression} = {result}")
            st.session_state.expression = result
        except Exception:
            st.session_state.expression = "Error"
    elif key == "C":
        st.session_state.expression = ""
    elif key == "DEL":
        st.session_state.expression = st.session_state.expression[:-1]
    else:
        st.session_state.expression += key

# Display current expression
st.text_input("Expression", value=st.session_state.expression, disabled=True, label_visibility="collapsed")

# Create the calculator keypad
col1, col2, col3, col4 = st.columns(4)

keys = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("C", "0", "=", "+"),
]

with col1:
    st.button(keys[0][0], on_click=handle_click, args=(keys[0][0],), use_container_width=True)
    st.button(keys[1][0], on_click=handle_click, args=(keys[1][0],), use_container_width=True)
    st.button(keys[2][0], on_click=handle_click, args=(keys[2][0],), use_container_width=True)
    st.button(keys[3][0], on_click=handle_click, args=(keys[3][0],), use_container_width=True)

with col2:
    st.button(keys[0][1], on_click=handle_click, args=(keys[0][1],), use_container_width=True)
    st.button(keys[1][1], on_click=handle_click, args=(keys[1][1],), use_container_width=True)
    st.button(keys[2][1], on_click=handle_click, args=(keys[2][1],), use_container_width=True)
    st.button(keys[3][1], on_click=handle_click, args=(keys[3][1],), use_container_width=True)

with col3:
    st.button(keys[0][2], on_click=handle_click, args=(keys[0][2],), use_container_width=True)
    st.button(keys[1][2], on_click=handle_click, args=(keys[1][2],), use_container_width=True)
    st.button(keys[2][2], on_click=handle_click, args=(keys[2][2],), use_container_width=True)
    st.button(keys[3][2], on_click=handle_click, args=(keys[3][2],), use_container_width=True)

with col4:
    st.button(keys[0][3], on_click=handle_click, args=(keys[0][3],), use_container_width=True)
    st.button(keys[1][3], on_click=handle_click, args=(keys[1][3],), use_container_width=True)
    st.button(keys[2][3], on_click=handle_click, args=(keys[2][3],), use_container_width=True)
    st.button(keys[3][3], on_click=handle_click, args=(keys[3][3],), use_container_width=True)

st.button("DEL", on_click=handle_click, args=("DEL",), use_container_width=True)

st.subheader("Calculation History")
if st.session_state.history:
    for entry in reversed(st.session_state.history):
        st.write(entry)
else:
    st.write("No calculations yet.")