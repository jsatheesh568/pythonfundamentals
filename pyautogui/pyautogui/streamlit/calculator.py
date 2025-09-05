import streamlit as st

# Title
st.title("🧮 Simple Calculator with Streamlit")

# Input numbers
num1 = st.number_input("Enter first number", value=0.0, step=1.0)
num2 = st.number_input("Enter second number", value=0.0, step=1.0)

# Select operation
operation = st.selectbox(
    "Choose operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

# Perform calculation
result = None
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            st.error("❌ Division by zero is not allowed")
        else:
            result = num1 / num2

# Display result
if result is not None:
    st.success(f"✅ Result: {result}")
