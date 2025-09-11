import streamlit as st
import math

def main():
    # Page configuration
    st.set_page_config(
        page_title="Simple Calculator", 
        page_icon="🧮",
        layout="centered"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .calculator-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .result-display {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🧮 Simple Calculator</h1>', unsafe_allow_html=True)
    
    # Calculator container
    with st.container():
        st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
        
        # Create two columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Operation selection
            operation = st.selectbox(
                "Choose Operation:",
                ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)", 
                 "Power (^)", "Square Root (√)", "Percentage (%)"],
                index=0
            )
            
            # Number inputs
            if operation == "Square Root (√)":
                num1 = st.number_input("Enter number:", value=0.0, format="%.2f")
                num2 = None
            else:
                num1 = st.number_input("First number:", value=0.0, format="%.2f")
                if operation != "Percentage (%)":
                    num2 = st.number_input("Second number:", value=0.0, format="%.2f")
                else:
                    num2 = None
        
        with col2:
            st.markdown("### Quick Actions")
            if st.button("🔄 Clear", use_container_width=True):
                st.rerun()
            
        # Calculate button
        if st.button("🟰 Calculate", use_container_width=True, type="primary"):
            try:
                result = calculate(operation, num1, num2)
                if result is not None:
                    st.markdown(f'<div class="result-display">Result: {result}</div>', unsafe_allow_html=True)
                    
                    # Show calculation breakdown
                    breakdown = get_calculation_breakdown(operation, num1, num2, result)
                    st.info(f"Calculation: {breakdown}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # History section
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if st.session_state.history:
        st.markdown("### 📜 Recent Calculations")
        for i, calc in enumerate(reversed(st.session_state.history[-5:])):
            st.text(calc)

def calculate(operation, num1, num2):
    """Perform the calculation based on operation"""
    if operation == "Addition (+)":
        result = num1 + num2
    elif operation == "Subtraction (-)":
        result = num1 - num2
    elif operation == "Multiplication (×)":
        result = num1 * num2
    elif operation == "Division (÷)":
        if num2 == 0:
            st.error("Cannot divide by zero!")
            return None
        result = num1 / num2
    elif operation == "Power (^)":
        result = num1 ** num2
    elif operation == "Square Root (√)":
        if num1 < 0:
            st.error("Cannot calculate square root of negative number!")
            return None
        result = math.sqrt(num1)
    elif operation == "Percentage (%)":
        result = num1 / 100
    else:
        return None
    
    # Add to history
    breakdown = get_calculation_breakdown(operation, num1, num2, result)
    st.session_state.history.append(breakdown)
    
    return round(result, 4)

def get_calculation_breakdown(operation, num1, num2, result):
    """Get human-readable calculation breakdown"""
    if operation == "Addition (+)":
        return f"{num1} + {num2} = {result}"
    elif operation == "Subtraction (-)":
        return f"{num1} - {num2} = {result}"
    elif operation == "Multiplication (×)":
        return f"{num1} × {num2} = {result}"
    elif operation == "Division (÷)":
        return f"{num1} ÷ {num2} = {result}"
    elif operation == "Power (^)":
        return f"{num1} ^ {num2} = {result}"
    elif operation == "Square Root (√)":
        return f"√{num1} = {result}"
    elif operation == "Percentage (%)":
        return f"{num1}% = {result}"
    
    return f"Result: {result}"

if __name__ == "__main__":
    main()
