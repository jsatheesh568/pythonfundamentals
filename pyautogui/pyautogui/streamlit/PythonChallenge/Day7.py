import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="💪 Gym Workout Logger",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Initialize session state
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = []

# Simple exercise database
EXERCISES = {
    'Chest': ['Bench Press', 'Push-ups', 'Dumbbell Flyes', 'Incline Press', 'Dips'],
    'Back': ['Pull-ups', 'Deadlift', 'Barbell Rows', 'Lat Pulldowns', 'T-Bar Rows'],
    'Legs': ['Squats', 'Leg Press', 'Lunges', 'Leg Curls', 'Calf Raises'],
    'Shoulders': ['Overhead Press', 'Lateral Raises', 'Shoulder Shrugs', 'Arnold Press'],
    'Arms': ['Bicep Curls', 'Tricep Dips', 'Hammer Curls', 'Close-Grip Push-ups'],
    'Core': ['Plank', 'Crunches', 'Russian Twists', 'Dead Bug', 'Mountain Climbers']
}

# Motivational quotes
QUOTES = [
    "💪 The pain you feel today will be the strength you feel tomorrow!",
    "🔥 Success isn't given. It's earned in the gym!",
    "⚡ Your only limit is your mind!"
]

def calculate_volume(weight, sets, reps):
    """Calculate training volume"""
    return weight * sets * reps

def create_progress_chart():
    """Create simple progress visualization"""
    if not st.session_state.workout_data:
        return None
    
    df = pd.DataFrame(st.session_state.workout_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Daily volume chart
    daily_volume = df.groupby('date')['volume'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_volume['date'],
        y=daily_volume['volume'],
        mode='lines+markers',
        name='Daily Volume',
        line=dict(color='#667eea', width=3)
    ))
    
    fig.update_layout(
        title='📈 Weekly Progress - Training Volume',
        xaxis_title='Date',
        yaxis_title='Volume (kg)',
        height=400
    )
    
    return fig

# Main app
st.title("🏋️‍♂️ Gym Workout Logger")
st.markdown("Track your workouts and see your progress!")

# Motivational quote
st.info(random.choice(QUOTES))

# Quick stats
if st.session_state.workout_data:
    df = pd.DataFrame(st.session_state.workout_data)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workouts", len(df))
    with col2:
        st.metric("Total Volume", f"{df['volume'].sum():,.0f} kg")
    with col3:
        st.metric("Avg Volume", f"{df['volume'].mean():.0f} kg")
    with col4:
        favorite = df['exercise'].mode().iloc[0] if not df.empty else "None"
        st.metric("Top Exercise", favorite)

st.divider()

# Workout entry form
st.subheader("📝 Log New Workout")

col1, col2 = st.columns([2, 1])

with col1:
    muscle_group = st.selectbox("💪 Muscle Group", list(EXERCISES.keys()))
    exercise = st.selectbox("🏃‍♂️ Exercise", EXERCISES[muscle_group])
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        weight = st.number_input("⚖️ Weight (kg)", min_value=0.0, value=20.0, step=2.5)
    with col_b:
        sets = st.number_input("🔢 Sets", min_value=1, value=3, step=1)
    with col_c:
        reps = st.number_input("🔁 Reps", min_value=1, value=10, step=1)
    
    notes = st.text_area("📝 Notes", placeholder="How did this feel?")

with col2:
    st.markdown("### 📊 Workout Stats")
    volume = calculate_volume(weight, sets, reps)
    st.metric("Volume", f"{volume:,.0f} kg")
    
    if st.session_state.workout_data:
        df = pd.DataFrame(st.session_state.workout_data)
        exercise_history = df[df['exercise'] == exercise]
        if not exercise_history.empty:
            last_weight = exercise_history.iloc[-1]['weight']
            best_weight = exercise_history['weight'].max()
            st.metric("Last Weight", f"{last_weight} kg")
            st.metric("Best Weight", f"{best_weight} kg")

# Submit button
if st.button("✅ Log Workout", type="primary"):
    workout_entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M'),
        'muscle_group': muscle_group,
        'exercise': exercise,
        'weight': weight,
        'sets': sets,
        'reps': reps,
        'volume': volume,
        'notes': notes
    }
    
    st.session_state.workout_data.append(workout_entry)
    st.success("🎉 Workout logged successfully!")
    st.rerun()

st.divider()

# Progress visualization
if st.session_state.workout_data:
    st.subheader("📊 Your Progress")
    
    # Show progress chart
    fig = create_progress_chart()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Exercise frequency chart
    df = pd.DataFrame(st.session_state.workout_data)
    exercise_counts = df['exercise'].value_counts().head(5)
    
    if not exercise_counts.empty:
        fig2 = px.bar(
            x=exercise_counts.values,
            y=exercise_counts.index,
            orientation='h',
            title='🏆 Top 5 Exercises',
            labels={'x': 'Frequency', 'y': 'Exercise'}
        )
        st.plotly_chart(fig2, use_container_width=True)

# Workout history
if st.session_state.workout_data:
    st.subheader("📚 Recent Workouts")
    
    df = pd.DataFrame(st.session_state.workout_data)
    
    # Show last 10 workouts
    recent_df = df.tail(10).copy()
    recent_df = recent_df[['date', 'exercise', 'weight', 'sets', 'reps', 'volume']]
    
    st.dataframe(recent_df, use_container_width=True)
    
    # Export data option
    if st.button("📥 Export All Data"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"workout_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Sidebar with additional features
with st.sidebar:
    st.title("🏋️‍♂️ Quick Stats")
    
    if st.session_state.workout_data:
        df = pd.DataFrame(st.session_state.workout_data)
        
        # This week's workouts
        df['date'] = pd.to_datetime(df['date'])
        this_week = df[df['date'] >= datetime.now() - timedelta(days=7)]
        st.metric("This Week", f"{len(this_week)} workouts")
        
        # Muscle group distribution
        st.subheader("💪 Muscle Focus")
        muscle_counts = df['muscle_group'].value_counts()
        for muscle, count in muscle_counts.items():
            st.write(f"{muscle}: {count} workouts")
    
    st.divider()
    
    # Clear data option
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.workout_data = []
        st.success("Data cleared!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💪 **Keep pushing your limits!** Track consistently to see amazing progress!")