# DAy10.py - SocialEagle AI Workshop Registration (fixed - full file, export button persistent)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import random
import hashlib
import re

# Page configuration
st.set_page_config(
    page_title="🚀 SocialEagle AI Workshop Registration",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------- Styling -----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        from { box-shadow: 0 15px 50px rgba(0,0,0,0.3); }
        to { box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4); }
    }
    
    .workshop-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .workshop-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 2px solid #fff;
    }
    
    .location-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .location-card:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    
    .registration-form {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .success-animation {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        animation: successBounce 1s ease-out;
    }
    
    @keyframes successBounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        80% { transform: translateY(-10px); }
    }
    
    .feature-badge {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        padding: 5px 15px;
        border-radius: 20px;
        color: #333;
        font-weight: bold;
        font-size: 12px;
        margin: 5px;
        display: inline-block;
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: 200px 0; }
    }
    
    .capacity-bar {
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .capacity-fill {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
        position: relative;
    }
    
    .eagle-icon {
        font-size: 3em;
        animation: fly 4s ease-in-out infinite;
    }
    
    @keyframes fly {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    .workshop-badge {
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 10px;
        font-weight: bold;
        margin: 2px;
        display: inline-block;
    }
    
    .beginner { background: #4CAF50; color: white; }
    .intermediate { background: #FF9800; color: white; }
    .advanced { background: #F44336; color: white; }
    
    .timeline-item {
        border-left: 3px solid #667eea;
        padding-left: 20px;
        margin: 15px 0;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ----------- Data -----------
WORKSHOP_DATA = {
    "AI Fundamentals": {
        "description": "Introduction to Artificial Intelligence concepts and applications",
        "duration": "4 hours",
        "level": "beginner",
        "instructor": "Dr. Sarah Chen",
        "capacity": 50,
        "price": "₹2,999",
        "features": ["Hands-on Labs", "Certificate", "Learning Materials", "Q&A Session"],
        "prerequisites": "Basic programming knowledge",
        "schedule": "10:00 AM - 2:00 PM"
    },
    "Machine Learning Mastery": {
        "description": "Deep dive into ML algorithms, model training, and deployment",
        "duration": "6 hours",
        "level": "intermediate",
        "instructor": "Prof. Rajesh Kumar",
        "capacity": 30,
        "price": "₹4,999",
        "features": ["Project Work", "Industry Case Studies", "Certificate", "Mentorship"],
        "prerequisites": "Python programming, statistics basics",
        "schedule": "9:00 AM - 4:00 PM"
    },
    "Deep Learning Workshop": {
        "description": "Neural networks, CNN, RNN, and advanced deep learning techniques",
        "duration": "8 hours",
        "level": "advanced",
        "instructor": "Dr. Priya Sharma",
        "capacity": 25,
        "price": "₹7,999",
        "features": ["GPU Access", "Real Projects", "Research Papers", "Industry Connect"],
        "prerequisites": "ML experience, Python, TensorFlow/PyTorch",
        "schedule": "9:00 AM - 6:00 PM"
    },
    "NLP & ChatGPT Integration": {
        "description": "Natural Language Processing and ChatGPT API integration",
        "duration": "5 hours",
        "level": "intermediate",
        "instructor": "Mr. Amit Verma",
        "capacity": 40,
        "price": "₹3,999",
        "features": ["API Access", "Live Coding", "Build Chatbot", "Deployment Guide"],
        "prerequisites": "Python, basic API knowledge",
        "schedule": "11:00 AM - 5:00 PM"
    },
    "Computer Vision Bootcamp": {
        "description": "Image processing, object detection, and computer vision applications",
        "duration": "7 hours",
        "level": "advanced",
        "instructor": "Dr. Meera Patel",
        "capacity": 20,
        "price": "₹6,999",
        "features": ["OpenCV", "Live Camera Projects", "Industry Use Cases", "Portfolio Build"],
        "prerequisites": "Python, image processing basics",
        "schedule": "9:00 AM - 5:00 PM"
    },
    "AI Ethics & Future Trends": {
        "description": "Ethical AI, bias detection, and future of artificial intelligence",
        "duration": "3 hours",
        "level": "beginner",
        "instructor": "Prof. Ananya Gupta",
        "capacity": 60,
        "price": "₹1,999",
        "features": ["Interactive Discussion", "Case Studies", "Future Roadmap", "Network Session"],
        "prerequisites": "General interest in AI",
        "schedule": "2:00 PM - 5:00 PM"
    }
}

LOCATIONS = {
    "Mumbai": {
        "venue": "SocialEagle Tech Hub",
        "address": "Bandra-Kurla Complex, Mumbai, Maharashtra 400051",
        "capacity": 150,
        "facilities": ["WiFi", "Projector", "AC", "Parking", "Food Court", "Metro Access"],
        "contact": "+91 98765 43210",
        "coordinates": {"lat": 19.0596, "lon": 72.8295}
    },
    "Bangalore": {
        "venue": "Innovation Center",
        "address": "Electronic City, Bangalore, Karnataka 560100",
        "capacity": 120,
        "facilities": ["WiFi", "Smart Boards", "AC", "Parking", "Cafeteria", "Bus Stop"],
        "contact": "+91 98765 43211",
        "coordinates": {"lat": 12.9716, "lon": 77.5946}
    },
    "Delhi": {
        "venue": "AI Learning Hub",
        "address": "Connaught Place, New Delhi, Delhi 110001",
        "capacity": 100,
        "facilities": ["WiFi", "Audio System", "AC", "Metro Station", "Restaurant", "Parking"],
        "contact": "+91 98765 43212",
        "coordinates": {"lat": 28.6139, "lon": 77.2090}
    },
    "Hyderabad": {
        "venue": "Tech Valley Center",
        "address": "HITEC City, Hyderabad, Telangana 500081",
        "capacity": 80,
        "facilities": ["WiFi", "Lab Setup", "AC", "Parking", "Food Court", "IT Corridor"],
        "contact": "+91 98765 43213",
        "coordinates": {"lat": 17.3850, "lon": 78.4867}
    },
    "Chennai": {
        "venue": "Digital Learning Center",
        "address": "OMR, Chennai, Tamil Nadu 600119",
        "capacity": 90,
        "facilities": ["WiFi", "Projectors", "AC", "Parking", "Canteen", "IT Park Access"],
        "contact": "+91 98765 43214",
        "coordinates": {"lat": 13.0827, "lon": 80.2707}
    },
    "Pune": {
        "venue": "Innovation Campus",
        "address": "Hinjewadi, Pune, Maharashtra 411057",
        "capacity": 70,
        "facilities": ["WiFi", "Smart Classroom", "AC", "Parking", "Food Zone", "IT Hub"],
        "contact": "+91 98765 43215",
        "coordinates": {"lat": 18.5204, "lon": 73.8567}
    }
}

# ----------- Session state init -----------
def init_session_state():
    if 'registrations' not in st.session_state:
        st.session_state.registrations = []
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'selected_workshop' not in st.session_state:
        st.session_state.selected_workshop = None
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = None
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    # IMPORTANT: tab_selection must exist
    if 'tab_selection' not in st.session_state:
        st.session_state.tab_selection = "home"

# ----------- Utilities -----------
def generate_registration_id():
    """Generate unique registration ID"""
    timestamp = str(datetime.now().timestamp()) + str(random.random())
    return hashlib.md5(timestamp.encode()).hexdigest()[:8].upper()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_workshop_capacity():
    """Calculate current capacity for each workshop"""
    capacity_data = {}
    for workshop in WORKSHOP_DATA.keys():
        registered_count = len([r for r in st.session_state.registrations if r['workshop'] == workshop])
        capacity_data[workshop] = {
            'registered': registered_count,
            'capacity': WORKSHOP_DATA[workshop]['capacity'],
            'percentage': (registered_count / WORKSHOP_DATA[workshop]['capacity']) * 100 if WORKSHOP_DATA[workshop]['capacity'] else 0
        }
    return capacity_data

# ----------- Analytics & Maps -----------
def create_registration_analytics():
    """Create analytics charts for registrations"""
    if not st.session_state.registrations:
        return None

    df = pd.DataFrame(st.session_state.registrations)

    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Registrations by Workshop', 'Registrations by Location', 
                       'Experience Level Distribution', 'Registration Timeline'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "pie"}, {"type": "scatter"}]]
    )

    # Workshop distribution
    workshop_counts = df['workshop'].value_counts()
    fig.add_trace(
        go.Bar(x=workshop_counts.index, y=workshop_counts.values, 
               name='Workshops', marker_color='#667eea'),
        row=1, col=1
    )

    # Location distribution
    location_counts = df['location'].value_counts()
    fig.add_trace(
        go.Pie(labels=location_counts.index, values=location_counts.values,
               name='Locations'),
        row=1, col=2
    )

    # Experience level distribution
    if 'experience' in df.columns:
        exp_counts = df['experience'].value_counts()
        fig.add_trace(
            go.Pie(labels=exp_counts.index, values=exp_counts.values,
                   name='Experience'),
            row=2, col=1
        )

    # Timeline
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    timeline_data = df.groupby('date').size().reset_index(name='count')
    fig.add_trace(
        go.Scatter(x=timeline_data['date'], y=timeline_data['count'],
                  mode='lines+markers', name='Daily Registrations',
                  line=dict(color='#764ba2', width=3)),
        row=2, col=2
    )

    fig.update_layout(height=650, showlegend=False, title_text="📊 Registration Analytics Dashboard")
    return fig

def create_location_map():
    """Create interactive map of workshop locations"""
    locations_df = []
    for city, info in LOCATIONS.items():
        registered_count = len([r for r in st.session_state.registrations if r['location'] == city])
        locations_df.append({
            'City': city,
            'Latitude': info['coordinates']['lat'],
            'Longitude': info['coordinates']['lon'],
            'Venue': info['venue'],
            'Registrations': registered_count,
            'Capacity': info['capacity'],
            'Address': info['address']
        })

    df = pd.DataFrame(locations_df)

    fig = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        size='Registrations',
        hover_name='City',
        hover_data=['Venue', 'Registrations', 'Capacity'],
        color='Registrations',
        color_continuous_scale='viridis',
        size_max=30,
        zoom=4,
        center={'lat': 20.5937, 'lon': 78.9629},
        title='🗺️ Workshop Locations & Registrations'
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig

# ----------- Pages -----------
def home_page():
    """Main landing page"""
    st.markdown("""
    <div class="main-header">
        <div class="eagle-icon">🦅</div>
        <h1 style="margin: 20px 0; font-size: 3em;">SocialEagle AI Workshop</h1>
        <h2 style="margin: 10px 0; opacity: 0.9;">Master the Future of Artificial Intelligence</h2>
        <p style="font-size: 1.2em; margin: 20px 0;">Join India's Premier AI Learning Experience</p>
        <div style="margin: 20px 0;">
            <span class="feature-badge">🎓 Expert Instructors</span>
            <span class="feature-badge">🏆 Industry Certified</span>
            <span class="feature-badge">💻 Hands-on Labs</span>
            <span class="feature-badge">🤝 Networking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats
    total_registrations = len(st.session_state.registrations)
    unique_locations = len(set(r['location'] for r in st.session_state.registrations)) if st.session_state.registrations else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="stats-card"><h2 style="color: #333; margin: 0;">🎯</h2><h3 style="color: #333; margin: 5px 0;">6 Workshops</h3><p style="color: #666; margin: 0;">Different Specializations</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stats-card"><h2 style="color: #333; margin: 0;">👥</h2><h3 style="color: #333; margin: 5px 0;">{total_registrations}</h3><p style="color: #666; margin: 0;">Registered Participants</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="stats-card"><h2 style="color: #333; margin: 0;">🏙️</h2><h3 style="color: #333; margin: 5px 0;">6 Cities</h3><p style="color: #666; margin: 0;">Across India</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="stats-card"><h2 style="color: #333; margin: 0;">⭐</h2><h3 style="color: #333; margin: 5px 0;">4.9/5</h3><p style="color: #666; margin: 0;">Average Rating</p></div>""", unsafe_allow_html=True)

    # Featured workshops
    st.markdown("## 🚀 Featured AI Workshops")
    capacity_data = calculate_workshop_capacity()
    for workshop_name, workshop_info in list(WORKSHOP_DATA.items())[:3]:
        current_capacity = capacity_data.get(workshop_name, {'registered': 0, 'capacity': 50, 'percentage': 0})
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="workshop-card">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0;">{workshop_name}</h3>
                    <span class="workshop-badge {workshop_info['level']}">{workshop_info['level'].upper()}</span>
                </div>
                <p style="margin: 10px 0; opacity: 0.9;">{workshop_info['description']}</p>
                <div style="display: flex; justify-content: between; align-items: center; margin-top: 15px;">
                    <div>
                        <strong>👨‍🏫 {workshop_info['instructor']}</strong><br>
                        <small>⏱️ {workshop_info['duration']} | 💰 {workshop_info['price']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Capacity: {current_capacity['registered']}/{current_capacity['capacity']}**")
            progress_value = min(current_capacity['percentage'] / 100, 1.0)
            st.progress(progress_value)
            if current_capacity['percentage'] < 70:
                st.success("🟢 Available")
            elif current_capacity['percentage'] < 90:
                st.warning("🟡 Filling Fast")
            else:
                st.error("🔴 Almost Full")

    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Register Now", type="primary", use_container_width=True):
            st.session_state.tab_selection = "registration"
            st.rerun()

    # Testimonials
    st.markdown("## 💬 What Our Participants Say")
    testimonials = [
        {"name": "Rahul Sharma", "role": "Software Engineer", "text": "Amazing hands-on experience! The instructors are top-notch.", "rating": 5},
        {"name": "Priya Patel", "role": "Data Scientist", "text": "Best AI workshop I've attended. Practical approach with real projects.", "rating": 5},
        {"name": "Amit Kumar", "role": "ML Engineer", "text": "Great networking opportunities and excellent learning materials.", "rating": 4}
    ]
    cols = st.columns(3)
    for i, testimonial in enumerate(testimonials):
        with cols[i]:
            stars = "⭐" * testimonial['rating']
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin: 10px 0;">
                <div style="color: #FFD700; font-size: 18px; margin-bottom: 10px;">{stars}</div>
                <p style="color: #333; font-style: italic; margin-bottom: 15px;">"{testimonial['text']}"</p>
                <div style="color: #667eea; font-weight: bold;">{testimonial['name']}</div>
                <div style="color: #999; font-size: 12px;">{testimonial['role']}</div>
            </div>
            """, unsafe_allow_html=True)

def workshops_page():
    """Detailed workshops information"""
    st.markdown("# 🎓 AI Workshop Catalog")
    st.markdown("Explore our comprehensive range of AI workshops designed for different skill levels")

    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        level_filter = st.selectbox("Filter by Level", ["All", "Beginner", "Intermediate", "Advanced"])
    with col2:
        duration_filter = st.selectbox("Filter by Duration", ["All", "3-4 hours", "5-6 hours", "7+ hours"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Price", "Duration", "Capacity"])

    capacity_data = calculate_workshop_capacity()

    for workshop_name, workshop_info in WORKSHOP_DATA.items():
        # Apply level filter
        if level_filter != "All" and workshop_info['level'] != level_filter.lower():
            continue

        current_capacity = capacity_data.get(workshop_name, {'registered': 0, 'capacity': 50, 'percentage': 0})
        with st.expander(f"🚀 {workshop_name} - {workshop_info['price']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Description:** {workshop_info['description']}")
                st.markdown(f"**👨‍🏫 Instructor:** {workshop_info['instructor']}")
                st.markdown(f"**⏱️ Duration:** {workshop_info['duration']} ({workshop_info['schedule']})")
                st.markdown(f"**📚 Prerequisites:** {workshop_info['prerequisites']}")
                st.markdown("**🎯 What You'll Learn:**")
                for feature in workshop_info['features']:
                    st.markdown(f"• {feature}")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    level_color = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}
                    st.markdown(f"**Level:** {level_color[workshop_info['level']]} {workshop_info['level'].title()}")
                with col_b:
                    st.markdown(f"**Capacity:** {workshop_info['capacity']} seats")
                with col_c:
                    st.markdown(f"**Price:** {workshop_info['price']}")
            with col2:
                st.markdown("### 📊 Current Registration Status")
                st.metric("Registered", f"{current_capacity['registered']}/{current_capacity['capacity']}")
                progress_value = min(current_capacity['percentage'] / 100, 1.0)
                st.progress(progress_value)
                availability_text = "🟢 Available"
                if current_capacity['percentage'] >= 90:
                    availability_text = "🔴 Almost Full"
                elif current_capacity['percentage'] >= 70:
                    availability_text = "🟡 Filling Fast"
                st.markdown(f"**Status:** {availability_text}")
                if st.button(f"Register for {workshop_name}", key=f"reg_{workshop_name}"):
                    st.session_state.selected_workshop = workshop_name
                    st.session_state.tab_selection = "registration"
                    st.rerun()

def locations_page():
    """Workshop locations and venue information"""
    st.markdown("# 🏙️ Workshop Locations")
    st.markdown("Choose from our premium venues across major Indian cities")

    # Location map
    if st.session_state.registrations:
        location_map = create_location_map()
        st.plotly_chart(location_map, use_container_width=True)

    # Location details
    cols = st.columns(2)
    for i, (city, location_info) in enumerate(LOCATIONS.items()):
        registered_count = len([r for r in st.session_state.registrations if r['location'] == city])
        with cols[i % 2]:
            st.markdown(f"""
            <div class="location-card">
                <h3 style="margin: 0 0 15px 0;">📍 {city}</h3>
                <h4 style="margin: 0 0 10px 0; opacity: 0.9;">{location_info['venue']}</h4>
                <p style="margin: 0 0 15px 0; opacity: 0.8; font-size: 14px;">{location_info['address']}</p>
                <div style="display: flex; justify-content: between; margin: 15px 0;">
                    <div>
                        <strong>Capacity:</strong> {location_info['capacity']} seats<br>
                        <strong>Registered:</strong> {registered_count} participants
                    </div>
                </div>
                <div style="margin: 15px 0;">
                    <strong>🏢 Facilities:</strong><br>
                    {' • '.join(location_info['facilities'])}
                </div>
                <div style="margin: 15px 0;">
                    <strong>📞 Contact:</strong> {location_info['contact']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Register for this location button (FIXED: complete statement)
            if st.button(f"Choose {city}", key=f"loc_{city}", type="secondary"):
                st.session_state.selected_location = city
                st.session_state.tab_selection = "registration"
                st.rerun()

def registration_page():
    """Registration form for attendees"""
    st.markdown("# 📝 Register for a Workshop")
    st.markdown("Fill in your details below to reserve your seat.")

    # Preselect workshop/location if chosen earlier
    chosen_workshop = st.session_state.get('selected_workshop', None)
    chosen_location = st.session_state.get('selected_location', None)

    col1, col2 = st.columns(2)
    with col1:
        workshop = st.selectbox("Select Workshop", options=list(WORKSHOP_DATA.keys()), index=list(WORKSHOP_DATA.keys()).index(chosen_workshop) if chosen_workshop in WORKSHOP_DATA else 0)
        name = st.text_input("Full Name")
        email = st.text_input("Email")
    with col2:
        location = st.selectbox("Select Location", options=list(LOCATIONS.keys()), index=list(LOCATIONS.keys()).index(chosen_location) if chosen_location in LOCATIONS else 0)
        phone = st.text_input("Phone Number")
        experience = st.selectbox("Experience Level", options=["Beginner", "Intermediate", "Advanced"])

    agree = st.checkbox("I agree to the terms and confirm the details are correct.")
    if st.button("🔒 Confirm Registration", type="primary"):
        # Validate
        if not name.strip():
            st.error("Please enter your name.")
            return
        if not validate_email(email):
            st.error("Please enter a valid email.")
            return
        if not phone.strip():
            st.error("Please enter a phone number.")
            return
        if not agree:
            st.error("You must agree to the terms to proceed.")
            return

        reg_id = generate_registration_id()
        registration = {
            "id": reg_id,
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "workshop": workshop,
            "location": location,
            "experience": experience,
            "timestamp": datetime.now().isoformat()
        }

        st.session_state.registrations.append(registration)
        st.session_state.registration_success = True
        # reset selected_* so next time user can choose new values
        st.session_state.selected_workshop = None
        st.session_state.selected_location = None

        st.success(f"Registration successful! Your registration ID: **{reg_id}**")
        st.info(f"We've registered you for **{workshop}** at **{location}**.")
        st.rerun()

def admin_page():
    """Simple admin / analytics page"""
    st.markdown("# 🔐 Admin Dashboard")
    if not st.session_state.registrations:
        st.info("No registrations yet.")
    else:
        st.markdown("### 📋 Recent Registrations")
        df = pd.DataFrame(list(reversed(st.session_state.registrations)))
        st.dataframe(df[['timestamp','id','name','email','workshop','location','experience']], use_container_width=True)
        st.markdown("### 📊 Analytics")
        analytics_fig = create_registration_analytics()
        if analytics_fig:
            st.plotly_chart(analytics_fig, use_container_width=True)

# ----------- Main -----------
def main():
    init_session_state()

    # Sidebar navigation - make radio reflect current tab_selection properly
    st.sidebar.title("SocialEagle Admin")
    st.sidebar.markdown("---")

    # Radio options (labels shown to user)
    radio_options = ["Home", "Workshops", "Locations", "Register", "Admin"]

    # Map session tab keys to radio labels
    key_to_label = {
        "home": "Home",
        "workshops": "Workshops",
        "locations": "Locations",
        "registration": "Register",
        "admin": "Admin"
    }

    # Determine the default index for the radio from session state
    current_label = key_to_label.get(st.session_state.get('tab_selection', 'home'), "Home")
    try:
        default_index = radio_options.index(current_label)
    except ValueError:
        default_index = 0

    # Show the radio with correct index so it doesn't stomp session_state on rerun
    page = st.sidebar.radio("Navigate:", radio_options, index=default_index)

    # Map chosen radio label back to session_state key (lower-case key names we use)
    label_to_key = {
        "Home": "home",
        "Workshops": "workshops",
        "Locations": "locations",
        "Register": "registration",
        "Admin": "admin"
    }

    # Update session_state.tab_selection according to radio choice
    st.session_state.tab_selection = label_to_key.get(page, "home")

    # Quick actions
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Go to Home"):
        st.session_state.tab_selection = "home"
        st.rerun()

    # ---------- Export (recommended: always show download button if data exists) ----------
    if st.session_state.registrations:
        df = pd.DataFrame(st.session_state.registrations)
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="📥 Export Registrations as CSV",
            data=csv,
            file_name=f"registrations_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.info("No registrations to export.")

    # Render pages according to tab_selection
    sel = st.session_state.get('tab_selection', 'home')
    if sel == "home":
        home_page()
    elif sel == "workshops":
        workshops_page()
    elif sel == "locations":
        locations_page()
    elif sel == "registration":
        registration_page()
    elif sel == "admin":
        admin_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
