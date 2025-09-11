import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (m)"""
    return weight / (height ** 2)

def get_bmi_category(bmi):
    """Get BMI category based on WHO standards"""
    if bmi < 18.5:
        return "Underweight", "blue"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "green"
    elif 25 <= bmi < 30:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

# Page config
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# Title and description
st.title("⚖️ BMI Calculator")
st.markdown("Calculate your Body Mass Index and track your health journey!")

# Input section
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=500.0,
        value=70.0,
        step=0.1
    )

with col2:
    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=300.0,
        value=170.0,
        step=0.1
    )

# Convert height to meters
height_m = height / 100

# Calculate BMI
if st.button("Calculate BMI", type="primary"):
    if weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height_m)
        category, color = get_bmi_category(bmi)
        
        # Display results
        st.markdown("---")
        st.subheader("Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BMI", f"{bmi:.1f}")
        
        with col2:
            st.markdown(f"**Category:** :{color}[{category}]")
        
        with col3:
            st.metric("Height", f"{height} cm")
            st.metric("Weight", f"{weight} kg")
        
        # BMI Chart
        st.subheader("BMI Categories")
        
        # Create BMI range chart
        bmi_data = {
            'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
            'Min BMI': [0, 18.5, 25, 30],
            'Max BMI': [18.5, 25, 30, 40],
            'Color': ['blue', 'green', 'orange', 'red']
        }
        
        df = pd.DataFrame(bmi_data)
        
        # Highlight user's BMI
        fig = px.bar(
            df, 
            x='Category', 
            y='Max BMI',
            color='Color',
            title=f'Your BMI: {bmi:.1f} ({category})'
        )
        
        # Add user BMI line
        fig.add_hline(y=bmi, line_dash="dash", line_color="black", 
                     annotation_text=f"Your BMI: {bmi:.1f}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Health recommendations
        st.subheader("Health Recommendations")
        
        if category == "Underweight":
            st.info("💡 Consider consulting a healthcare provider about healthy weight gain strategies.")
        elif category == "Normal weight":
            st.success("✅ Great! Maintain your current lifestyle with balanced diet and regular exercise.")
        elif category == "Overweight":
            st.warning("⚠️ Consider moderate exercise and balanced nutrition to reach a healthier weight.")
        else:
            st.error("🚨 Please consult with a healthcare professional for personalized advice.")

# BMI History Tracker (Optional Enhancement)
st.markdown("---")
st.subheader("📊 BMI History Tracker")

if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []

if st.button("Save Current BMI"):
    if weight > 0 and height > 0:
        bmi = calculate_bmi(weight, height_m)
        st.session_state.bmi_history.append({
            'Date': pd.Timestamp.now().strftime('%Y-%m-%d'),
            'BMI': bmi,
            'Weight': weight,
            'Height': height
        })
        st.success("BMI saved to history!")

if st.session_state.bmi_history:
    df_history = pd.DataFrame(st.session_state.bmi_history)
    
    # Plot BMI trend
    fig_trend = px.line(
        df_history, 
        x='Date', 
        y='BMI',
        title='BMI Trend Over Time',
        markers=True
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Show history table
    st.dataframe(df_history, use_container_width=True)
    
    if st.button("Clear History"):
        st.session_state.bmi_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("**Note:** This calculator is for educational purposes only. Always consult healthcare professionals for medical advice.")
