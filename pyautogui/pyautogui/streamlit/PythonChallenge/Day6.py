import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import numpy as np
import json
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="💧 Hydration Hero",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for water-themed UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main {
        padding-top: 1rem;
    }
    
    /* Water wave animation */
    .wave-container {
        position: relative;
        width: 100%;
        height: 200px;
        background: linear-gradient(180deg, #4fc3f7 0%, #29b6f6 100%);
        border-radius: 20px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .wave {
        position: absolute;
        top: 50%;
        left: -100%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: wave 3s linear infinite;
        border-radius: 50%;
    }
    
    @keyframes wave {
        0% { transform: translateX(-100%) rotate(0deg); }
        100% { transform: translateX(100%) rotate(360deg); }
    }
    
    /* Water drop animation */
    .water-drop {
        width: 20px;
        height: 20px;
        background: linear-gradient(135deg, #81c784, #4fc3f7);
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        position: relative;
        animation: drip 2s ease-in-out infinite;
        display: inline-block;
        margin: 0 5px;
    }
    
    @keyframes drip {
        0%, 100% { transform: rotate(-45deg) translateY(0px); }
        50% { transform: rotate(-45deg) translateY(-10px); }
    }
    
    /* Hydration cards */
    .hydration-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .hydration-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.5);
    }
    
    /* Main title with water effect */
    .hydration-title {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #81c784, #4fc3f7, #29b6f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Progress bars with water theme */
    .water-progress {
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 25px;
        height: 30px;
        overflow: hidden;
        position: relative;
        margin: 15px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4fc3f7 0%, #29b6f6 50%, #0277bd 100%);
        border-radius: 25px;
        position: relative;
        transition: width 0.5s ease;
    }
    
    .progress-wave {
        position: absolute;
        top: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: wave-progress 2s linear infinite;
    }
    
    @keyframes wave-progress {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(0%); }
    }
    
    /* Goal achievement celebration */
    .goal-achieved {
        background: linear-gradient(135deg, #4caf50, #81c784);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        animation: celebration 0.5s ease-in-out;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
    }
    
    @keyframes celebration {
        0% { transform: scale(0.8); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Dehydration warning */
    .dehydration-warning {
        background: linear-gradient(135deg, #ff5722, #ff8a65);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Water glass visualization */
    .water-glass {
        width: 120px;
        height: 200px;
        border: 4px solid #4fc3f7;
        border-radius: 0 0 60px 60px;
        position: relative;
        margin: 20px auto;
        background: linear-gradient(to top, #4fc3f7 0%, transparent 100%);
        overflow: hidden;
    }
    
    .water-level {
        position: absolute;
        bottom: 0;
        width: 100%;
        background: linear-gradient(to top, #0277bd 0%, #4fc3f7 100%);
        transition: height 0.8s ease;
        border-radius: 0 0 56px 56px;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4fc3f7;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 5px;
    }
    
    /* Hydration level indicators */
    .hydration-excellent { color: #4caf50; }
    .hydration-good { color: #8bc34a; }
    .hydration-moderate { color: #ffeb3b; }
    .hydration-poor { color: #ff9800; }
    .hydration-critical { color: #f44336; }
    
    /* Water intake buttons */
    .water-btn {
        background: linear-gradient(135deg, #4fc3f7, #29b6f6);
        border: none;
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
    }
    
    .water-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 195, 247, 0.5);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    /* Tips section */
    .hydration-tip {
        background: linear-gradient(135deg, #81c784, #4fc3f7);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'water_data' not in st.session_state:
    st.session_state.water_data = []

if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 3000  # Default 3L in ml

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Hydration Hero',
        'weight': 70,
        'activity_level': 'Moderate',
        'climate': 'Temperate'
    }

# Helper functions
def get_hydration_level(intake_ml, goal_ml):
    percentage = (intake_ml / goal_ml) * 100
    if percentage >= 100:
        return "Excellent", "hydration-excellent", "🌊"
    elif percentage >= 80:
        return "Good", "hydration-good", "💧"
    elif percentage >= 60:
        return "Moderate", "hydration-moderate", "💦"
    elif percentage >= 40:
        return "Poor", "hydration-poor", "🟡"
    else:
        return "Critical", "hydration-critical", "🔴"

def calculate_recommended_intake(weight, activity_level, climate):
    base_intake = weight * 35  # 35ml per kg
    
    activity_multiplier = {
        'Low': 1.0,
        'Moderate': 1.2,
        'High': 1.5,
        'Extreme': 1.8
    }
    
    climate_multiplier = {
        'Cold': 0.9,
        'Temperate': 1.0,
        'Warm': 1.1,
        'Hot': 1.3
    }
    
    recommended = base_intake * activity_multiplier.get(activity_level, 1.2) * climate_multiplier.get(climate, 1.0)
    return int(recommended)

def add_water_intake(amount_ml):
    today = date.today().isoformat()
    current_time = datetime.now().strftime("%H:%M")
    
    # Check if there's already an entry for today
    today_entries = [entry for entry in st.session_state.water_data if entry['date'] == today]
    
    if today_entries:
        # Add to existing day
        for entry in st.session_state.water_data:
            if entry['date'] == today:
                entry['intake'] += amount_ml
                entry['log'].append({'time': current_time, 'amount': amount_ml})
                break
    else:
        # Create new day entry
        st.session_state.water_data.append({
            'date': today,
            'intake': amount_ml,
            'goal': st.session_state.daily_goal,
            'log': [{'time': current_time, 'amount': amount_ml}]
        })

def get_today_intake():
    today = date.today().isoformat()
    today_data = next((entry for entry in st.session_state.water_data if entry['date'] == today), None)
    return today_data['intake'] if today_data else 0

def get_week_data():
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    week_data = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.isoformat()
        day_data = next((entry for entry in st.session_state.water_data if entry['date'] == date_str), None)
        
        week_data.append({
            'date': current_date,
            'intake': day_data['intake'] if day_data else 0,
            'goal': day_data['goal'] if day_data else st.session_state.daily_goal,
            'day_name': current_date.strftime('%A')[:3]
        })
    
    return week_data

# Main App Layout
st.markdown('<h1 class="hydration-title">💧 Hydration Hero</h1>', unsafe_allow_html=True)

# Animated water drops
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <div class="water-drop"></div>
    <div class="water-drop" style="animation-delay: 0.5s;"></div>
    <div class="water-drop" style="animation-delay: 1s;"></div>
    <div class="water-drop" style="animation-delay: 1.5s;"></div>
</div>
""", unsafe_allow_html=True)

# Sidebar - User Profile & Settings
with st.sidebar:
    st.markdown("## 👤 User Profile")
    
    with st.expander("⚙️ Settings", expanded=True):
        st.session_state.user_profile['name'] = st.text_input("Name", st.session_state.user_profile['name'])
        st.session_state.user_profile['weight'] = st.number_input("Weight (kg)", 40, 200, st.session_state.user_profile['weight'])
        st.session_state.user_profile['activity_level'] = st.selectbox(
            "Activity Level", 
            ['Low', 'Moderate', 'High', 'Extreme'], 
            index=['Low', 'Moderate', 'High', 'Extreme'].index(st.session_state.user_profile['activity_level'])
        )
        st.session_state.user_profile['climate'] = st.selectbox(
            "Climate", 
            ['Cold', 'Temperate', 'Warm', 'Hot'], 
            index=['Cold', 'Temperate', 'Warm', 'Hot'].index(st.session_state.user_profile['climate'])
        )
    
    # Calculate recommended intake
    recommended = calculate_recommended_intake(
        st.session_state.user_profile['weight'],
        st.session_state.user_profile['activity_level'],
        st.session_state.user_profile['climate']
    )
    
    st.info(f"🎯 Recommended: {recommended}ml/day")
    
    # Daily goal setting
    st.session_state.daily_goal = st.number_input(
        "Daily Goal (ml)", 
        500, 
        8000, 
        st.session_state.daily_goal,
        step=250
    )
    
    st.markdown("---")
    
    # Quick add buttons
    st.markdown("## 🥤 Quick Add")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💧 250ml", key="btn1"):
            add_water_intake(250)
            st.rerun()
        if st.button("🥤 500ml", key="btn2"):
            add_water_intake(500)
            st.rerun()
    
    with col2:
        if st.button("🍶 750ml", key="btn3"):
            add_water_intake(750)
            st.rerun()
        if st.button("🧴 1000ml", key="btn4"):
            add_water_intake(1000)
            st.rerun()
    
    # Custom amount
    custom_amount = st.number_input("Custom (ml)", 1, 2000, 250, key="custom")
    if st.button("➕ Add Custom", key="btn_custom"):
        add_water_intake(custom_amount)
        st.rerun()
    
    st.markdown("---")
    
    # Hydration tips
    tips = [
        "💡 Start your day with a glass of water",
        "⏰ Set hourly water reminders",
        "🍎 Eat water-rich fruits and vegetables",
        "🏃‍♂️ Drink extra water during exercise",
        "☀️ Increase intake in hot weather",
        "🍵 Herbal teas count towards hydration",
        "📱 Use apps to track your progress"
    ]
    
    st.markdown("### 💡 Hydration Tips")
    tip_index = datetime.now().day % len(tips)
    st.markdown(f'<div class="hydration-tip">{tips[tip_index]}</div>', unsafe_allow_html=True)

# Main content area
today_intake = get_today_intake()
progress_percentage = (today_intake / st.session_state.daily_goal) * 100
hydration_status, status_class, status_emoji = get_hydration_level(today_intake, st.session_state.daily_goal)

# Today's Progress Section
st.markdown('<div class="hydration-card">', unsafe_allow_html=True)
st.markdown("## 📊 Today's Hydration Progress")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{today_intake}</div>
        <div class="metric-label">ml consumed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{st.session_state.daily_goal}</div>
        <div class="metric-label">ml goal</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{progress_percentage:.0f}%</div>
        <div class="metric-label">completed</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value {status_class}">{status_emoji}</div>
        <div class="metric-label">{hydration_status}</div>
    </div>
    """, unsafe_allow_html=True)

# Progress bar with water animation
progress_width = min(progress_percentage, 100)
st.markdown(f"""
<div class="water-progress">
    <div class="progress-fill" style="width: {progress_width}%;">
        <div class="progress-wave"></div>
    </div>
</div>
<div style="text-align: center; color: white; font-weight: 600; margin-top: 10px;">
    {today_intake}ml / {st.session_state.daily_goal}ml ({progress_percentage:.1f}%)
</div>
""", unsafe_allow_html=True)

# Water glass visualization
glass_fill_percentage = min(progress_percentage, 100)
st.markdown(f"""
<div style="text-align: center;">
    <div class="water-glass">
        <div class="water-level" style="height: {glass_fill_percentage}%;"></div>
    </div>
    <p style="color: white; margin-top: 10px;">Virtual Water Glass</p>
</div>
""", unsafe_allow_html=True)

# Achievement or warning message
if progress_percentage >= 100:
    st.markdown(f"""
    <div class="goal-achieved">
        🎉 Congratulations! You've achieved your daily hydration goal! 
        Keep up the excellent work, {st.session_state.user_profile['name']}! 🌊
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
elif progress_percentage < 40:
    remaining = st.session_state.daily_goal - today_intake
    st.markdown(f"""
    <div class="dehydration-warning">
        ⚠️ Hydration Alert! You need {remaining}ml more water today. 
        Your body needs hydration - drink up! 💧
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Weekly Progress Chart
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("## 📈 Weekly Hydration Trend")

week_data = get_week_data()
df_week = pd.DataFrame(week_data)

# Create dual-axis chart
fig = make_subplots(
    rows=1, cols=1,
    specs=[[{"secondary_y": True}]]
)

# Add intake bars
fig.add_trace(
    go.Bar(
        x=df_week['day_name'],
        y=df_week['intake'],
        name="Water Intake",
        marker_color='rgba(79, 195, 247, 0.8)',
        marker_line=dict(color='rgba(79, 195, 247, 1)', width=2)
    ),
    secondary_y=False
)

# Add goal line
fig.add_trace(
    go.Scatter(
        x=df_week['day_name'],
        y=df_week['goal'],
        mode='lines+markers',
        name="Daily Goal",
        line=dict(color='red', width=3, dash='dash'),
        marker=dict(size=8, color='red')
    ),
    secondary_y=False
)

# Add percentage achievement
percentages = [(intake/goal)*100 for intake, goal in zip(df_week['intake'], df_week['goal'])]
fig.add_trace(
    go.Scatter(
        x=df_week['day_name'],
        y=percentages,
        mode='lines+markers',
        name="Achievement %",
        line=dict(color='green', width=2),
        marker=dict(size=6, color='green'),
        yaxis='y2'
    ),
    secondary_y=True
)

# Update layout
fig.update_layout(
    title="Weekly Hydration Performance",
    template="plotly_dark",
    height=400,
    showlegend=True,
    hovermode='x unified'
)

fig.update_yaxes(title_text="Water Intake (ml)", secondary_y=False)
fig.update_yaxes(title_text="Achievement (%)", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Detailed Daily Log
if today_intake > 0:
    st.markdown('<div class="hydration-card">', unsafe_allow_html=True)
    st.markdown("## 📝 Today's Water Log")
    
    today_data = next((entry for entry in st.session_state.water_data if entry['date'] == date.today().isoformat()), None)
    
    if today_data and today_data['log']:
        log_df = pd.DataFrame(today_data['log'])
        log_df['cumulative'] = log_df['amount'].cumsum()
        
        # Time-based intake chart
        fig_timeline = go.Figure()
        
        fig_timeline.add_trace(go.Scatter(
            x=list(range(len(log_df))),
            y=log_df['cumulative'],
            mode='lines+markers',
            name='Cumulative Intake',
            line=dict(color='#4fc3f7', width=3),
            marker=dict(size=8, color='#29b6f6'),
            fill='tonexty',
            fillcolor='rgba(79, 195, 247, 0.3)'
        ))
        
        fig_timeline.add_hline(
            y=st.session_state.daily_goal, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Daily Goal"
        )
        
        fig_timeline.update_layout(
            title="Hydration Timeline Today",
            xaxis_title="Water Intake Session",
            yaxis_title="Cumulative Intake (ml)",
            template="plotly_dark",
            height=300
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Log table
        st.markdown("### 💧 Intake Log")
        for i, entry in enumerate(today_data['log']):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"⏰ {entry['time']}")
            with col2:
                st.write(f"💧 {entry['amount']}ml")
            with col3:
                st.write(f"📊 {log_df.iloc[i]['cumulative']}ml")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Hydration Analytics
st.markdown('<div class="hydration-card">', unsafe_allow_html=True)
st.markdown("## 📊 Hydration Analytics")

if len(st.session_state.water_data) > 0:
    analytics_df = pd.DataFrame(st.session_state.water_data)
    analytics_df['achievement_rate'] = (analytics_df['intake'] / analytics_df['goal']) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_intake = analytics_df['intake'].mean()
        st.metric("📈 Avg Daily Intake", f"{avg_intake:.0f}ml")
    
    with col2:
        avg_achievement = analytics_df['achievement_rate'].mean()
        st.metric("🎯 Avg Achievement", f"{avg_achievement:.0f}%")
    
    with col3:
        best_day = analytics_df['intake'].max()
        st.metric("🏆 Best Day", f"{best_day}ml")
    
    with col4:
        consistency = len([x for x in analytics_df['achievement_rate'] if x >= 80])
        st.metric("✅ Good Days", f"{consistency}/{len(analytics_df)}")
    
    # Monthly trend if enough data
    if len(analytics_df) > 7:
        fig_trend = px.line(
            analytics_df, 
            x='date', 
            y='intake',
            title="Long-term Hydration Trend",
            template="plotly_dark"
        )
        fig_trend.add_hline(y=st.session_state.daily_goal, line_dash="dash", line_color="red")
        st.plotly_chart(fig_trend, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer with motivational message
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: white; padding: 20px;">
    <h3>🌊 Keep Flowing, {st.session_state.user_profile['name']}! 🌊</h3>
    <p>Every drop counts towards your health and wellness journey.</p>
    <p><em>"Water is life's matter and matrix, mother and medium. There is no life without water." - Albert Szent-Gyorgyi</em></p>
</div>
""", unsafe_allow_html=True)

# Data management
with st.expander("🔧 Data Management"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Today's Data"):
            today = date.today().isoformat()
            st.session_state.water_data = [entry for entry in st.session_state.water_data if entry['date'] != today]
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset All Data"):
            st.session_state.water_data = []
            st.rerun()
    
    # Export data
    if st.session_state.water_data:
        df_export = pd.DataFrame(st.session_state.water_data)
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"hydration_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )