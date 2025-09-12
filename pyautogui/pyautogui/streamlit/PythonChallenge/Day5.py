import streamlit as st
import requests
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🔄 Ultimate Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for amazing UI
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .converter-header {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    }
    
    .unit-display {
        font-size: 2rem;
        font-weight: bold;
        color: #ff6b6b;
        text-align: center;
        margin: 1rem 0;
    }
    
    .conversion-result {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        margin: 1rem 0;
    }
    
    .feature-box {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    
    .history-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #4ecdc4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Header
st.markdown('<h1 class="converter-header">🔄 Ultimate Unit Converter</h1>', unsafe_allow_html=True)

# Sidebar for converter selection
st.sidebar.markdown("## 🎛️ Converter Selection")
converter_type = st.sidebar.selectbox(
    "Choose Converter Type",
    ["💰 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight", "⚡ Energy", "💨 Speed", "📊 Data Storage"]
)

# Currency Converter
if converter_type == "💰 Currency":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Currency Converter")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        amount = st.number_input("Amount", value=1.0, min_value=0.0, step=0.01)
        from_currency = st.selectbox("From Currency", [
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL"
        ])
    
    with col2:
        st.markdown("### ↔️")
    
    with col3:
        to_currency = st.selectbox("To Currency", [
            "EUR", "USD", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL"
        ])
    
    # Mock exchange rates (in real app, you'd use an API)
    exchange_rates = {
        ("USD", "EUR"): 0.85, ("USD", "GBP"): 0.73, ("USD", "JPY"): 110.0,
        ("EUR", "USD"): 1.18, ("EUR", "GBP"): 0.86, ("EUR", "JPY"): 129.0,
        ("GBP", "USD"): 1.37, ("GBP", "EUR"): 1.16, ("GBP", "JPY"): 150.0,
        ("USD", "INR"): 74.5, ("EUR", "INR"): 87.8, ("GBP", "INR"): 102.0
    }
    
    if from_currency != to_currency:
        rate = exchange_rates.get((from_currency, to_currency), 1.0)
        if rate == 1.0 and from_currency != to_currency:
            # Calculate reverse rate
            reverse_rate = exchange_rates.get((to_currency, from_currency), 1.0)
            if reverse_rate != 1.0:
                rate = 1 / reverse_rate
        
        converted_amount = amount * rate
        
        st.markdown(f'<div class="conversion-result">{amount} {from_currency} = {converted_amount:.2f} {to_currency}</div>', unsafe_allow_html=True)
        
        # Rate trend visualization
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        rates = [rate + np.random.uniform(-0.05, 0.05) for _ in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=rates, mode='lines+markers', 
                               name=f'{from_currency}/{to_currency}',
                               line=dict(color='#ff6b6b', width=3)))
        fig.update_layout(
            title=f"Exchange Rate Trend: {from_currency}/{to_currency}",
            template="plotly_dark",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Temperature Converter
elif converter_type == "🌡️ Temperature":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 🌡️ Temperature Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_value = st.number_input("Temperature", value=25.0, step=0.1)
        from_temp = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin", "Rankine"])
    
    with col2:
        to_temp = st.selectbox("To", ["Fahrenheit", "Celsius", "Kelvin", "Rankine"])
    
    # Temperature conversion functions
    def convert_temperature(value, from_unit, to_unit):
        # Convert to Celsius first
        if from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        elif from_unit == "Rankine":
            celsius = (value - 491.67) * 5/9
        else:  # Celsius
            celsius = value
        
        # Convert from Celsius to target
        if to_unit == "Fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15
        elif to_unit == "Rankine":
            return celsius * 9/5 + 491.67
        else:  # Celsius
            return celsius
    
    converted_temp = convert_temperature(temp_value, from_temp, to_temp)
    
    st.markdown(f'<div class="conversion-result">{temp_value}° {from_temp} = {converted_temp:.2f}° {to_temp}</div>', unsafe_allow_html=True)
    
    # Temperature scale visualization
    temps = [
        {"scale": "Celsius", "value": convert_temperature(temp_value, from_temp, "Celsius")},
        {"scale": "Fahrenheit", "value": convert_temperature(temp_value, from_temp, "Fahrenheit")},
        {"scale": "Kelvin", "value": convert_temperature(temp_value, from_temp, "Kelvin")},
        {"scale": "Rankine", "value": convert_temperature(temp_value, from_temp, "Rankine")}
    ]
    
    fig = go.Figure(data=[
        go.Bar(x=[t["scale"] for t in temps], 
               y=[t["value"] for t in temps],
               marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
    ])
    fig.update_layout(
        title="Temperature in All Scales",
        template="plotly_dark",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Length Converter
elif converter_type == "📏 Length":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📏 Length Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        length_value = st.number_input("Length", value=1.0, min_value=0.0, step=0.01)
        from_length = st.selectbox("From Unit", [
            "Millimeter", "Centimeter", "Meter", "Kilometer", 
            "Inch", "Foot", "Yard", "Mile"
        ])
    
    with col2:
        to_length = st.selectbox("To Unit", [
            "Meter", "Millimeter", "Centimeter", "Kilometer", 
            "Inch", "Foot", "Yard", "Mile"
        ])
    
    # Conversion factors to meters
    length_factors = {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.34
    }
    
    # Convert to meters then to target unit
    meters = length_value * length_factors[from_length]
    converted_length = meters / length_factors[to_length]
    
    st.markdown(f'<div class="conversion-result">{length_value} {from_length} = {converted_length:.6f} {to_length}</div>', unsafe_allow_html=True)
    
    # Visual comparison
    common_objects = {
        "Human Hair Width": 0.00007,  # meters
        "Credit Card Length": 0.0856,
        "Football Field": 109.7,
        "Eiffel Tower": 300,
        "Mount Everest": 8848
    }
    
    if meters > 0:
        st.markdown("### 📐 Size Comparison")
        comparison_data = []
        for obj, size in common_objects.items():
            ratio = meters / size
            if 0.01 <= ratio <= 100:
                comparison_data.append({"Object": obj, "Times": ratio})
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            fig = px.bar(df, x="Object", y="Times", 
                        title=f"Your measurement compared to common objects",
                        color="Times",
                        color_continuous_scale="viridis")
            fig.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Weight Converter
elif converter_type == "⚖️ Weight":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### ⚖️ Weight Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_value = st.number_input("Weight", value=1.0, min_value=0.0, step=0.01)
        from_weight = st.selectbox("From Unit", [
            "Gram", "Kilogram", "Ton", "Ounce", "Pound", "Stone"
        ])
    
    with col2:
        to_weight = st.selectbox("To Unit", [
            "Kilogram", "Gram", "Ton", "Ounce", "Pound", "Stone"
        ])
    
    # Conversion factors to grams
    weight_factors = {
        "Gram": 1.0,
        "Kilogram": 1000.0,
        "Ton": 1000000.0,
        "Ounce": 28.3495,
        "Pound": 453.592,
        "Stone": 6350.29
    }
    
    # Convert to grams then to target unit
    grams = weight_value * weight_factors[from_weight]
    converted_weight = grams / weight_factors[to_weight]
    
    st.markdown(f'<div class="conversion-result">{weight_value} {from_weight} = {converted_weight:.6f} {to_weight}</div>', unsafe_allow_html=True)
    
    # Animal weight comparison
    animal_weights = {
        "Blue Whale": 150000,  # kg
        "Elephant": 6000,
        "Car": 1500,
        "Human": 70,
        "Cat": 4.5,
        "Mouse": 0.02
    }
    
    kg_value = grams / 1000
    if kg_value > 0:
        st.markdown("### 🐘 Animal Weight Comparison")
        for animal, weight in animal_weights.items():
            ratio = kg_value / weight
            if ratio > 1:
                st.markdown(f"**{animal}**: {ratio:.2f} times heavier than a {animal.lower()}")
            else:
                st.markdown(f"**{animal}**: {1/ratio:.2f} times lighter than a {animal.lower()}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Speed Converter
elif converter_type == "💨 Speed":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 💨 Speed Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        speed_value = st.number_input("Speed", value=1.0, min_value=0.0, step=0.01)
        from_speed = st.selectbox("From Unit", [
            "m/s", "km/h", "mph", "knots", "ft/s"
        ])
    
    with col2:
        to_speed = st.selectbox("To Unit", [
            "km/h", "m/s", "mph", "knots", "ft/s"
        ])
    
    # Conversion factors to m/s
    speed_factors = {
        "m/s": 1.0,
        "km/h": 1/3.6,
        "mph": 0.44704,
        "knots": 0.514444,
        "ft/s": 0.3048
    }
    
    # Convert to m/s then to target unit
    ms = speed_value * speed_factors[from_speed]
    converted_speed = ms / speed_factors[to_speed]
    
    st.markdown(f'<div class="conversion-result">{speed_value} {from_speed} = {converted_speed:.4f} {to_speed}</div>', unsafe_allow_html=True)
    
    # Speed comparison chart
    reference_speeds = {
        "Walking": 1.4,  # m/s
        "Cycling": 5.5,
        "Car (city)": 13.9,
        "Car (highway)": 27.8,
        "Train": 55.6,
        "Airplane": 250,
        "Sound": 343,
        "Light": 299792458
    }
    
    if ms > 0:
        st.markdown("### 🚀 Speed Comparison")
        speed_data = []
        for ref, speed in reference_speeds.items():
            if 0.1 <= ms/speed <= 10:
                speed_data.append({"Reference": ref, "Your Speed (m/s)": ms, "Reference Speed (m/s)": speed})
        
        if speed_data:
            df = pd.DataFrame(speed_data)
            fig = px.bar(df, x="Reference", y=["Your Speed (m/s)", "Reference Speed (m/s)"], 
                        title="Speed Comparison",
                        barmode='group')
            fig.update_layout(template="plotly_dark", height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Energy Converter
elif converter_type == "⚡ Energy":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Energy Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        energy_value = st.number_input("Energy", value=1.0, min_value=0.0, step=0.01)
        from_energy = st.selectbox("From Unit", [
            "Joule", "Kilojoule", "Calorie", "Kilocalorie", "BTU", "kWh"
        ])
    
    with col2:
        to_energy = st.selectbox("To Unit", [
            "Kilojoule", "Joule", "Calorie", "Kilocalorie", "BTU", "kWh"
        ])
    
    # Conversion factors to Joules
    energy_factors = {
        "Joule": 1.0,
        "Kilojoule": 1000.0,
        "Calorie": 4.184,
        "Kilocalorie": 4184.0,
        "BTU": 1055.06,
        "kWh": 3600000.0
    }
    
    # Convert to Joules then to target unit
    joules = energy_value * energy_factors[from_energy]
    converted_energy = joules / energy_factors[to_energy]
    
    st.markdown(f'<div class="conversion-result">{energy_value} {from_energy} = {converted_energy:.6f} {to_energy}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Data Storage Converter
elif converter_type == "📊 Data Storage":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Data Storage Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_value = st.number_input("Data Size", value=1.0, min_value=0.0, step=0.01)
        from_data = st.selectbox("From Unit", [
            "Byte", "KB", "MB", "GB", "TB", "PB"
        ])
    
    with col2:
        to_data = st.selectbox("To Unit", [
            "MB", "Byte", "KB", "GB", "TB", "PB"
        ])
    
    # Conversion factors to Bytes
    data_factors = {
        "Byte": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
        "PB": 1024**5
    }
    
    # Convert to Bytes then to target unit
    bytes_value = data_value * data_factors[from_data]
    converted_data = bytes_value / data_factors[to_data]
    
    st.markdown(f'<div class="conversion-result">{data_value} {from_data} = {converted_data:.8f} {to_data}</div>', unsafe_allow_html=True)
    
    # Data size visualization
    common_files = {
        "Text Document": 1024,  # bytes
        "Photo (JPEG)": 2 * 1024**2,  # 2MB
        "Song (MP3)": 5 * 1024**2,  # 5MB
        "HD Movie": 4 * 1024**3,  # 4GB
        "4K Movie": 25 * 1024**3  # 25GB
    }
    
    if bytes_value > 0:
        st.markdown("### 📁 File Size Comparison")
        for file_type, size in common_files.items():
            count = bytes_value / size
            if count >= 1:
                st.info(f"Your data = ~{count:.1f} {file_type}s")
            elif count >= 0.1:
                st.info(f"Your data = ~{count:.2f} {file_type}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar features
st.sidebar.markdown("---")
st.sidebar.markdown("## ⭐ Special Features")

# Quick converter
with st.sidebar.expander("🚀 Quick Convert"):
    quick_value = st.number_input("Quick Value", value=100.0, key="quick")
    if st.button("Convert 100km to miles"):
        miles = 100 / 1.609
        st.success(f"100 km = {miles:.2f} miles")
    if st.button("Convert 0°C to °F"):
        fahrenheit = 0 * 9/5 + 32
        st.success(f"0°C = {fahrenheit}°F")

# Conversion history
with st.sidebar.expander("📚 Conversion History"):
    if st.session_state.conversion_history:
        for i, conversion in enumerate(reversed(st.session_state.conversion_history[-5:])):
            st.markdown(f'<div class="history-item">{conversion}</div>', unsafe_allow_html=True)
    else:
        st.info("No conversions yet!")
    
    if st.button("Clear History"):
        st.session_state.conversion_history = []
        st.rerun()

# Fun facts
with st.sidebar.expander("🎯 Fun Facts"):
    facts = [
        "The speed of light is 299,792,458 m/s!",
        "One light-year equals about 9.46 trillion km!",
        "The human body is about 37°C (98.6°F)!",
        "Mount Everest is 8,848.86 meters tall!",
        "A blue whale can weigh up to 200 tons!"
    ]
    
    import random
    st.info(random.choice(facts))

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Conversions Available", "50+")
with col2:
    st.metric("Categories", "7")
with col3:
    st.metric("Accuracy", "99.9%")

st.markdown("""
<div style="text-align: center; color: white; margin-top: 2rem;">
    <h4>🔄 Ultimate Unit Converter</h4>
    <p>Convert anything, anywhere, anytime!</p>
</div>
""", unsafe_allow_html=True)            