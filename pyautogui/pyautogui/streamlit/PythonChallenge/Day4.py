import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="BMI Calculator | BMI கணக்கீடு",
    page_icon="⚖️",
    layout="wide"
)

# Language dictionary
LANGUAGES = {
    'english': {
        'title': '⚖️ BMI Calculator & Health Guide',
        'subtitle': 'Calculate your Body Mass Index and get personalized health insights',
        'select_language': 'Select Language',
        'weight_label': 'Weight (kg)',
        'height_label': 'Height (cm)',
        'calculate_btn': 'Calculate BMI',
        'your_bmi': 'Your BMI',
        'bmi_category': 'BMI Category',
        'health_status': 'Health Status',
        'underweight': 'Underweight',
        'normal': 'Normal Weight',
        'overweight': 'Overweight',
        'obese': 'Obese',
        'health_tips_title': '💡 Health Tips',
        'bmi_meter_title': '📊 BMI Meter',
        'health_videos_title': '🎥 Health & Fitness Videos',
        'tips': {
            'underweight': [
                "🍽️ Eat frequent, nutrient-dense meals",
                "🥜 Include healthy fats like nuts and avocados",
                "🏋️ Focus on strength training exercises",
                "💧 Stay hydrated and get adequate sleep",
                "👨‍⚕️ Consult a healthcare provider for personalized advice"
            ],
            'normal': [
                "🎯 Maintain your current healthy weight",
                "🥗 Continue eating a balanced diet",
                "🏃‍♂️ Stay active with regular exercise",
                "😴 Get 7-9 hours of quality sleep",
                "🧘‍♀️ Manage stress through relaxation techniques"
            ],
            'overweight': [
                "🍎 Focus on portion control and mindful eating",
                "🚶‍♀️ Increase daily physical activity",
                "🥤 Limit sugary drinks and processed foods",
                "📱 Track your food intake and exercise",
                "👥 Consider joining a support group or program"
            ],
            'obese': [
                "👨‍⚕️ Consult with healthcare professionals",
                "🎯 Set realistic, gradual weight loss goals",
                "🍽️ Create a structured meal plan",
                "💪 Start with low-impact exercises",
                "🧠 Address emotional eating patterns"
            ]
        }
    },
    'tamil': {
        'title': '⚖️ BMI கணக்கீடு மற்றும் ஆரோக்கிய வழிகாட்டி',
        'subtitle': 'உங்கள் உடல் நிறை குறியீட்டை கணக்கிட்டு தனிப்பயனாக்கப்பட்ட ஆரோக்கிய தகவல்களைப் பெறுங்கள்',
        'select_language': 'மொழியைத் தேர்ந்தெடுக்கவும்',
        'weight_label': 'எடை (கிலோ)',
        'height_label': 'உயரம் (செ.மீ)',
        'calculate_btn': 'BMI கணக்கிடு',
        'your_bmi': 'உங்கள் BMI',
        'bmi_category': 'BMI வகை',
        'health_status': 'ஆரோக்கிய நிலை',
        'underweight': 'குறைவான எடை',
        'normal': 'சாதாரண எடை',
        'overweight': 'அதிக எடை',
        'obese': 'உடல்பருமன்',
        'health_tips_title': '💡 ஆரோக்கிய குறிப்புகள்',
        'bmi_meter_title': '📊 BMI மீட்டர்',
        'health_videos_title': '🎥 ஆரோக்கியம் & உடற்பயிற்சி வீடியோக்கள்',
        'tips': {
            'underweight': [
                "🍽️ அடிக்கடி சத்துள்ள உணவுகள் உண்ணுங்கள்",
                "🥜 நட்ஸ் மற்றும் வெண்ணெய் பழம் போன்ற ஆரோக்கியமான கொழுப்புகளை சேர்க்கவும்",
                "🏋️ வலிமை பயிற்சி செய்யுங்கள்",
                "💧 நீர் அருந்துங்கள் மற்றும் போதுமான தூக்கம் பெறுங்கள்",
                "👨‍⚕️ தனிப்பயனாக்கப்பட்ட ஆலோசனைக்கு மருத்துவரை அணுகவும்"
            ],
            'normal': [
                "🎯 உங்கள் தற்போதைய ஆரோக்கியமான எடையை பராமரிக்கவும்",
                "🥗 சமச்சீர் உணவை தொடர்ந்து உண்ணுங்கள்",
                "🏃‍♂️ வழக்கமான உடற்பயிற்சியுடன் சுறுசுறுப்பாக இருங்கள்",
                "😴 7-9 மணிநேர தரமான தூக்கம் பெறுங்கள்",
                "🧘‍♀️ தளர்வு நுட்பங்கள் மூலம் மன அழுத்தத்தை நிர்வகிக்கவும்"
            ],
            'overweight': [
                "🍎 பகுதி கட்டுப்பாடு மற்றும் கவனத்துடன் உண்ணுதலில் கவனம் செலுத்துங்கள்",
                "🚶‍♀️ தினசரி உடல் செயல்பாட்டை அதிகரிக்கவும்",
                "🥤 சர்க்கரை பானங்கள் மற்றும் பதப்படுத்தப்பட்ட உணவுகளை குறைக்கவும்",
                "📱 உங்கள் உணவு உட்கொள்ளல் மற்றும் உடற்பயிற்சியை கண்காணிக்கவும்",
                "👥 ஆதரவு குழு அல்லது திட்டத்தில் சேருவதை கருத்தில் கொள்ளுங்கள்"
            ],
            'obese': [
                "👨‍⚕️ சுகாதார நிபுணர்களுடன் ஆலோசனை பெறுங்கள்",
                "🎯 யதார்த்தமான, படிப்படியான எடை இழப்பு இலக்குகளை அமைக்கவும்",
                "🍽️ கட்டமைக்கப்பட்ட உணவு திட்டத்தை உருவாக்கவும்",
                "💪 குறைந்த தாக்க உடற்பயிற்சிகளுடன் தொடங்குங்கள்",
                "🧠 உணர்ச்சி சார்ந்த உணவு முறைகளை கையாளுங்கள்"
            ]
        }
    }
}

# YouTube video recommendations
HEALTH_VIDEOS = {
    'english': [
        {'title': 'Complete Beginner Home Workout', 'id': 'ml6cT4AZdqI'},
        {'title': '10 Minute Morning Yoga', 'id': 'VaoV1PrYft4'},
        {'title': 'Healthy Meal Prep Ideas', 'id': 'sOXB8tAVC3M'},
        {'title': 'BMI Explained by Doctor', 'id': 'J2FCBBhMYW4'},
        {'title': '30 Day Fitness Challenge', 'id': 'TKt_gk5wCTg'}
    ],
    'tamil': [
        {'title': 'தமிழில் யோகா பயிற்சி', 'id': 'kJF_W8TClsw'},
        {'title': 'வீட்டில் உடற்பயிற்சி', 'id': 'MLXzRuJfQpA'},
        {'title': 'ஆரோக்கியமான உணவு', 'id': 'zJ8HE6kh7T8'},
        {'title': 'எடை குறைப்பு டிப்ஸ்', 'id': '7TlNz6WBaJE'},
        {'title': 'பாரம்பரிய தமிழ் உணவு', 'id': 'WHq5P8xvBZY'}
    ]
}

def calculate_bmi(weight, height_cm):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi, lang):
    """Get BMI category and color"""
    lang_data = LANGUAGES[lang]
    if bmi < 18.5:
        return lang_data['underweight'], '#3498db', 'underweight'
    elif 18.5 <= bmi < 25:
        return lang_data['normal'], '#2ecc71', 'normal'
    elif 25 <= bmi < 30:
        return lang_data['overweight'], '#f39c12', 'overweight'
    else:
        return lang_data['obese'], '#e74c3c', 'obese'

def create_bmi_meter(bmi, lang):
    """Create BMI meter visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': LANGUAGES[lang]['bmi_meter_title']},
        delta = {'reference': 22.5},  # Ideal BMI
        gauge = {
            'axis': {'range': [None, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 18.5], 'color': "lightcyan"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "lightyellow"},
                {'range': [30, 40], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    
    fig.update_layout(height=400)
    return fig

def create_bmi_range_chart():
    """Create BMI range visualization"""
    data = {
        'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
        'Min BMI': [0, 18.5, 25, 30],
        'Max BMI': [18.5, 25, 30, 40],
        'Color': ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    }
    
    fig = px.bar(
        x=['Underweight', 'Normal Weight', 'Overweight', 'Obese'],
        y=[18.5, 6.5, 5, 10],
        color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'],
        title="BMI Ranges"
    )
    fig.update_layout(showlegend=False, height=300)
    return fig

# Main app
def main():
    # Language selection
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_lang = st.selectbox(
            "🌐 Select Language | மொழியைத் தேர்ந்தெடுக்கவும்",
            ['english', 'tamil'],
            format_func=lambda x: "English 🇺🇸" if x == 'english' else "தமிழ் 🇮🇳"
        )
    
    lang_data = LANGUAGES[selected_lang]
    
    # Header
    st.title(lang_data['title'])
    st.markdown(f"*{lang_data['subtitle']}*")
    st.divider()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📏 BMI Calculator")
        
        # Input fields
        weight = st.number_input(
            lang_data['weight_label'],
            min_value=1.0,
            max_value=300.0,
            value=70.0,
            step=0.1,
            help="Enter your weight in kilograms"
        )
        
        height = st.number_input(
            lang_data['height_label'],
            min_value=50.0,
            max_value=250.0,
            value=170.0,
            step=0.1,
            help="Enter your height in centimeters"
        )
        
        if st.button(lang_data['calculate_btn'], type="primary"):
            bmi = calculate_bmi(weight, height)
            category, color, cat_key = get_bmi_category(bmi, selected_lang)
            
            # Store in session state
            st.session_state.bmi = bmi
            st.session_state.category = category
            st.session_state.color = color
            st.session_state.cat_key = cat_key
            st.session_state.lang = selected_lang
    
    with col2:
        if hasattr(st.session_state, 'bmi'):
            st.subheader("📊 Results")
            
            # BMI Result
            st.metric(
                label=lang_data['your_bmi'],
                value=f"{st.session_state.bmi}",
                delta=f"{st.session_state.bmi - 22.5:.1f} from ideal"
            )
            
            # Category with color
            st.markdown(f"""
            <div style="padding: 10px; background-color: {st.session_state.color}20; 
                        border-left: 4px solid {st.session_state.color}; margin: 10px 0;">
                <strong>{lang_data['bmi_category']}:</strong> {st.session_state.category}
            </div>
            """, unsafe_allow_html=True)
    
    # BMI Meter
    if hasattr(st.session_state, 'bmi'):
        st.subheader(lang_data['bmi_meter_title'])
        fig_meter = create_bmi_meter(st.session_state.bmi, selected_lang)
        st.plotly_chart(fig_meter, use_container_width=True)
    
    # BMI Range Chart
    st.subheader("📈 BMI Range Reference")
    fig_range = create_bmi_range_chart()
    st.plotly_chart(fig_range, use_container_width=True)
    
    # Health Tips
    if hasattr(st.session_state, 'cat_key'):
        st.subheader(lang_data['health_tips_title'])
        tips = lang_data['tips'][st.session_state.cat_key]
        
        for tip in tips:
            st.markdown(f"• {tip}")
    
    # Health Videos
    st.subheader(lang_data['health_videos_title'])
    
    videos = HEALTH_VIDEOS[selected_lang]
    cols = st.columns(2)
    
    for i, video in enumerate(videos):
        with cols[i % 2]:
            st.markdown(f"""
            **{video['title']}**
            """)
            st.video(f"https://www.youtube.com/watch?v={video['id']}")
            st.markdown("---")
    
    # Footer
    st.markdown("""
    ---
    <div style='text-align: center; color: #666;'>
        <p>⚠️ Disclaimer: This BMI calculator is for informational purposes only. 
        Consult healthcare professionals for medical advice.</p>
        <p>🏥 இந்த BMI கணக்கீடு தகவல் நோக்கங்களுக்காக மட்டுமே. 
        மருத்துவ ஆலோசனைக்கு சுகாதார நிபுணர்களை அணுகவும்.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main(