import streamlit as st
import random
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="🧠 Quiz Master Pro",
    page_icon="❓",
    layout="wide"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .quiz-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .question-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .score-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .correct-answer {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        animation: correctBounce 0.6s ease-out;
    }
    
    .wrong-answer {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        animation: shake 0.5s ease-out;
    }
    
    @keyframes correctBounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        80% { transform: translateY(-10px); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 20px;
        border-radius: 10px;
        margin: 20px 0;
        transition: width 0.5s ease-out;
    }
    
    .category-badge {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        padding: 5px 15px;
        border-radius: 15px;
        color: #333;
        font-weight: bold;
        font-size: 12px;
        margin: 5px;
        display: inline-block;
    }
    
    .difficulty-badge {
        padding: 5px 10px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 11px;
        margin: 5px;
        display: inline-block;
    }
    
    .easy { background: #4CAF50; }
    .medium { background: #FF9800; }
    .hard { background: #F44336; }
    
    .timer-display {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        margin: 10px 0;
        border: 2px solid rgba(255,255,255,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Quiz questions database
QUIZ_DATA = {
    "General Knowledge": [
        {
            "question": "🌍 What is the capital of Australia?",
            "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
            "correct": 2,
            "difficulty": "easy",
            "explanation": "Canberra is the capital city of Australia, not Sydney which is the largest city."
        },
        {
            "question": "🏔️ Which is the highest mountain in the world?",
            "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"],
            "correct": 1,
            "difficulty": "easy",
            "explanation": "Mount Everest stands at 8,848.86 meters above sea level."
        },
        {
            "question": "🎨 Who painted the Mona Lisa?",
            "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
            "correct": 2,
            "difficulty": "medium",
            "explanation": "Leonardo da Vinci painted the Mona Lisa between 1503-1519."
        },
        {
            "question": "🌊 What is the largest ocean on Earth?",
            "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
            "correct": 3,
            "difficulty": "easy",
            "explanation": "The Pacific Ocean covers about 46% of the world's water surface."
        },
        {
            "question": "⚛️ What is the chemical symbol for gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "correct": 2,
            "difficulty": "medium",
            "explanation": "Au comes from the Latin word 'aurum' meaning gold."
        }
    ],
    "Science & Technology": [
        {
            "question": "💻 Who is considered the father of computers?",
            "options": ["Alan Turing", "Charles Babbage", "Bill Gates", "Steve Jobs"],
            "correct": 1,
            "difficulty": "medium",
            "explanation": "Charles Babbage designed the first mechanical computer, the Analytical Engine."
        },
        {
            "question": "🧬 What does DNA stand for?",
            "options": ["Deoxyribonucleic Acid", "Dynamic Nuclear Acid", "Diverse Nucleic Acid", "Double Nuclear Acid"],
            "correct": 0,
            "difficulty": "easy",
            "explanation": "DNA (Deoxyribonucleic Acid) contains genetic instructions for all living organisms."
        },
        {
            "question": "🚀 What was the first artificial satellite launched into space?",
            "options": ["Explorer 1", "Vanguard 1", "Sputnik 1", "Luna 1"],
            "correct": 2,
            "difficulty": "medium",
            "explanation": "Sputnik 1 was launched by the Soviet Union on October 4, 1957."
        },
        {
            "question": "🌡️ At what temperature do water molecules freeze?",
            "options": ["0°F", "32°F", "0°C", "100°C"],
            "correct": 2,
            "difficulty": "easy",
            "explanation": "Water freezes at 0°C (32°F) at standard atmospheric pressure."
        },
        {
            "question": "⚡ Who invented the light bulb?",
            "options": ["Nikola Tesla", "Benjamin Franklin", "Thomas Edison", "Alexander Graham Bell"],
            "correct": 2,
            "difficulty": "easy",
            "explanation": "Thomas Edison developed the first practical incandescent light bulb in 1879."
        }
    ],
    "History": [
        {
            "question": "🏛️ In which year did World War II end?",
            "options": ["1944", "1945", "1946", "1947"],
            "correct": 1,
            "difficulty": "easy",
            "explanation": "World War II ended in 1945 with Japan's surrender on September 2, 1945."
        },
        {
            "question": "👑 Who was the first President of the United States?",
            "options": ["John Adams", "Thomas Jefferson", "George Washington", "Benjamin Franklin"],
            "correct": 2,
            "difficulty": "easy",
            "explanation": "George Washington served as the first President from 1789 to 1797."
        },
        {
            "question": "🏺 Which ancient wonder of the world was located in Egypt?",
            "options": ["Hanging Gardens", "Colossus of Rhodes", "Great Pyramid of Giza", "Lighthouse of Alexandria"],
            "correct": 2,
            "difficulty": "medium",
            "explanation": "The Great Pyramid of Giza is the only ancient wonder still standing today."
        },
        {
            "question": "⚔️ The Battle of Hastings took place in which year?",
            "options": ["1066", "1067", "1068", "1069"],
            "correct": 0,
            "difficulty": "hard",
            "explanation": "The Battle of Hastings was fought on 14 October 1066, Norman conquest of England."
        },
        {
            "question": "🗽 The Statue of Liberty was a gift from which country?",
            "options": ["Britain", "France", "Spain", "Italy"],
            "correct": 1,
            "difficulty": "medium",
            "explanation": "France gave the Statue of Liberty to the United States in 1886."
        }
    ],
    "Sports & Entertainment": [
        {
            "question": "⚽ Which country won the FIFA World Cup in 2018?",
            "options": ["Germany", "Brazil", "France", "Argentina"],
            "correct": 2,
            "difficulty": "medium",
            "explanation": "France won the 2018 FIFA World Cup held in Russia."
        },
        {
            "question": "🏀 How many players are on a basketball team on the court at one time?",
            "options": ["4", "5", "6", "7"],
            "correct": 1,
            "difficulty": "easy",
            "explanation": "Each basketball team has 5 players on the court at any given time."
        },
        {
            "question": "🎬 Which movie won the Academy Award for Best Picture in 2020?",
            "options": ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"],
            "correct": 2,
            "difficulty": "hard",
            "explanation": "Parasite became the first non-English film to win Best Picture."
        },
        {
            "question": "🏸 In which sport would you perform a slam dunk?",
            "options": ["Tennis", "Basketball", "Volleyball", "Badminton"],
            "correct": 1,
            "difficulty": "easy",
            "explanation": "A slam dunk is a type of basketball shot where the player jumps and forces the ball through the basket."
        },
        {
            "question": "🎭 Which Shakespeare play features the characters Romeo and Juliet?",
            "options": ["Hamlet", "Macbeth", "Romeo and Juliet", "Othello"],
            "correct": 2,
            "difficulty": "easy",
            "explanation": "Romeo and Juliet is one of Shakespeare's most famous tragic plays."
        }
    ]
}

# Initialize session state
def init_session_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'selected_categories' not in st.session_state:
        st.session_state.selected_categories = []
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_per_question' not in st.session_state:
        st.session_state.time_per_question = []

def create_quiz_questions(categories, num_questions, difficulty_filter=None):
    """Create a mixed quiz from selected categories"""
    all_questions = []
    
    for category in categories:
        if category in QUIZ_DATA:
            category_questions = [q.copy() for q in QUIZ_DATA[category]]
            if difficulty_filter and difficulty_filter != "all":
                category_questions = [q for q in category_questions if q['difficulty'] == difficulty_filter]
            
            for question in category_questions:
                question['category'] = category
                all_questions.append(question)
    
    # Shuffle and select desired number of questions
    random.shuffle(all_questions)
    return all_questions[:num_questions]

def get_difficulty_color(difficulty):
    """Get color class for difficulty badge"""
    colors = {"easy": "easy", "medium": "medium", "hard": "hard"}
    return colors.get(difficulty, "medium")

def create_progress_chart():
    """Create a progress visualization"""
    if not st.session_state.quiz_history:
        return None
    
    history_df = []
    for i, quiz in enumerate(st.session_state.quiz_history):
        history_df.append({
            'Quiz': f"Quiz {i+1}",
            'Score': quiz['score'],
            'Percentage': quiz['percentage'],
            'Questions': quiz['total_questions']
        })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[item['Quiz'] for item in history_df],
        y=[item['Percentage'] for item in history_df],
        mode='lines+markers+text',
        text=[f"{item['Score']}/{item['Questions']}" for item in history_df],
        textposition="top center",
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#764ba2')
    ))
    
    fig.update_layout(
        title='📈 Your Quiz Performance History',
        xaxis_title='Quiz Sessions',
        yaxis_title='Score Percentage',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_category_performance_chart():
    """Create category performance analysis"""
    if not st.session_state.quiz_history:
        return None
    
    category_stats = {}
    for quiz in st.session_state.quiz_history:
        for category in quiz.get('categories', []):
            if category not in category_stats:
                category_stats[category] = {'correct': 0.0, 'total': 0}
            # simplified: accumulate percentage portions
            category_stats[category]['total'] += 1
            category_stats[category]['correct'] += quiz['percentage']  # approximate contribution
    
    if not category_stats:
        return None
    
    categories = list(category_stats.keys())
    percentages = [(stats['correct'] / stats['total']) for stats in category_stats.values()]
    
    fig = px.pie(
        values=percentages,
        names=categories,
        title='🎯 Performance by Category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    return fig

def home_page():
    """Quiz home page with options and statistics"""
    st.markdown("""
    <div class="quiz-header">
        <h1>🧠 Quiz Master Pro</h1>
        <h3>Test Your Knowledge Across Multiple Categories!</h3>
        <p>Choose your categories, difficulty, and number of questions to create a personalized quiz experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quiz statistics
    if st.session_state.quiz_history:
        col1, col2, col3, col4 = st.columns(4)
        
        total_quizzes = len(st.session_state.quiz_history)
        avg_score = sum(q['percentage'] for q in st.session_state.quiz_history) / total_quizzes
        best_score = max(q['percentage'] for q in st.session_state.quiz_history)
        total_questions = sum(q['total_questions'] for q in st.session_state.quiz_history)
        
        with col1:
            st.metric("🎯 Quizzes Taken", total_quizzes)
        with col2:
            st.metric("📊 Average Score", f"{avg_score:.1f}%")
        with col3:
            st.metric("🏆 Best Score", f"{best_score:.1f}%")
        with col4:
            st.metric("❓ Questions Answered", total_questions)
    
    # Quiz setup
    st.markdown("## 🎯 Create Your Quiz")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Select Categories")
        selected_categories = st.multiselect(
            "Choose quiz categories:",
            options=list(QUIZ_DATA.keys()),
            default=list(QUIZ_DATA.keys())[:2],
            help="Select one or more categories for your quiz"
        )
        
        if selected_categories:
            # Show category info
            st.markdown("#### 📚 Selected Categories:")
            for category in selected_categories:
                num_questions = len(QUIZ_DATA[category])
                st.markdown(f"""
                <div class="category-badge">
                    {category} ({num_questions} questions)
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Quiz Settings")
        
        num_questions = st.slider(
            "Number of Questions:",
            min_value=5,
            max_value=20,
            value=10,
            help="Choose how many questions you want in your quiz"
        )
        
        difficulty_filter = st.selectbox(
            "Difficulty Filter:",
            options=["all", "easy", "medium", "hard"],
            format_func=lambda x: x.title() if x != "all" else "All Difficulties",
            help="Filter questions by difficulty level"
        )
        
        time_limit = st.checkbox("Enable Timer ⏰", help="Add time pressure to your quiz!")
    
    # Start quiz button
    if st.button("🚀 Start Quiz!", type="primary", use_container_width=True):
        if selected_categories:
            st.session_state.questions = create_quiz_questions(
                selected_categories, 
                num_questions, 
                difficulty_filter if difficulty_filter != "all" else None
            )
            
            if st.session_state.questions:
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.user_answers = []
                st.session_state.quiz_completed = False
                st.session_state.selected_categories = selected_categories
                st.session_state.start_time = time.time()
                st.session_state.time_per_question = []
                st.rerun()
            else:
                st.warning("No questions found with the selected criteria. Try different settings!")
        else:
            st.warning("Please select at least one category!")
    
    # Performance charts
    if st.session_state.quiz_history:
        st.markdown("## 📊 Your Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            progress_chart = create_progress_chart()
            if progress_chart:
                st.plotly_chart(progress_chart, use_container_width=True)
        
        with col2:
            category_chart = create_category_performance_chart()
            if category_chart:
                st.plotly_chart(category_chart, use_container_width=True)

def quiz_page():
    """Main quiz interface"""
    if not st.session_state.questions:
        st.error("No quiz questions available. Please start a new quiz.")
        return
    
    current_q = st.session_state.current_question
    total_q = len(st.session_state.questions)
    question_data = st.session_state.questions[current_q]
    
    # Progress bar
    progress = (current_q + 1) / total_q
    st.markdown(f"""
    <div style="background: #f0f0f0; border-radius: 10px; margin: 20px 0;">
        <div class="progress-bar" style="width: {progress * 100}%; padding: 10px; text-align: center; color: white;">
            Question {current_q + 1} of {total_q} ({progress * 100:.0f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question card
    difficulty_class = get_difficulty_color(question_data['difficulty'])
    st.markdown(f"""
    <div class="question-card">
        <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 15px;">
            <div class="category-badge">{question_data['category']}</div>
            <div class="difficulty-badge {difficulty_class}">{question_data['difficulty'].upper()}</div>
        </div>
        <h2 style="margin: 15px 0;">{question_data['question']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    st.markdown("### Select your answer:")
    selected_answer = st.radio(
        "Choose the correct option:",
        options=range(len(question_data['options'])),
        format_func=lambda x: f"{chr(65+x)}. {question_data['options'][x]}",
        key=f"question_{current_q}"
    )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous", key="prev_btn"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("✅ Submit Answer", type="primary", key="submit_btn"):
            # Record answer and time
            if st.session_state.start_time is None:
                st.session_state.start_time = time.time()
            question_time = time.time() - st.session_state.start_time - sum(st.session_state.time_per_question)
            st.session_state.time_per_question.append(question_time)
            
            # Store answer
            if len(st.session_state.user_answers) <= current_q:
                st.session_state.user_answers.append(selected_answer)
            else:
                st.session_state.user_answers[current_q] = selected_answer
            
            # Check if correct
            is_correct = selected_answer == question_data['correct']
            if is_correct:
                st.session_state.score += 1
                st.markdown("""
                <div class="correct-answer">
                    🎉 Correct! Great job!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    ❌ Incorrect. The correct answer is: {chr(65+question_data['correct'])}. {question_data['options'][question_data['correct']]}
                </div>
                """, unsafe_allow_html=True)
            
            # Show explanation
            st.info(f"💡 **Explanation:** {question_data['explanation']}")
            
            # Auto advance after short pause
            time.sleep(1.2)
            
            # Move to next question or finish
            if current_q + 1 < total_q:
                st.session_state.current_question += 1
                st.rerun()
            else:
                # Quiz completed
                st.session_state.quiz_completed = True
                
                # Save quiz results
                total_time = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                avg_time = (sum(st.session_state.time_per_question) / len(st.session_state.time_per_question)) if st.session_state.time_per_question else 0
                quiz_result = {
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'score': st.session_state.score,
                    'total_questions': total_q,
                    'percentage': (st.session_state.score / total_q) * 100,
                    'categories': st.session_state.selected_categories,
                    'total_time': total_time,
                    'avg_time_per_question': avg_time
                }
                st.session_state.quiz_history.append(quiz_result)
                st.rerun()
    
    with col3:
        if st.button("🏁 Finish Quiz", key="finish_btn"):
            st.session_state.quiz_completed = True
            # Save partial result if desired
            total_time = time.time() - st.session_state.start_time if st.session_state.start_time else 0
            avg_time = (sum(st.session_state.time_per_question) / len(st.session_state.time_per_question)) if st.session_state.time_per_question else 0
            quiz_result = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'score': st.session_state.score,
                'total_questions': total_q,
                'percentage': (st.session_state.score / total_q) * 100 if total_q else 0,
                'categories': st.session_state.selected_categories,
                'total_time': total_time,
                'avg_time_per_question': avg_time
            }
            st.session_state.quiz_history.append(quiz_result)
            st.rerun()

def results_page():
    """Quiz results and analysis"""
    score = st.session_state.score
    total = len(st.session_state.questions)
    percentage = (score / total) * 100 if total else 0
    
    # Results header
    st.markdown(f"""
    <div class="score-card">
        <h1>🎉 Quiz Completed!</h1>
        <h2>Your Score: {score}/{total} ({percentage:.1f}%)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance message
    if percentage >= 90:
        st.success("🏆 Outstanding! You're a quiz master!")
        st.balloons()
    elif percentage >= 70:
        st.success("🎯 Great job! Well done!")
    elif percentage >= 50:
        st.info("👍 Not bad! Keep practicing!")
    else:
        st.warning("📚 Keep studying and try again!")
    
    # Detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Performance Breakdown")
        
        # Score metrics
        st.metric("Correct Answers", f"{score}/{total}")
        st.metric("Accuracy", f"{percentage:.1f}%")
        
        if st.session_state.time_per_question:
            avg_time = sum(st.session_state.time_per_question) / len(st.session_state.time_per_question)
            st.metric("Avg Time per Question", f"{avg_time:.1f}s")
    
    with col2:
        st.markdown("### 🎯 Category Performance")
        
        # Category breakdown
        category_performance = {}
        for i, question in enumerate(st.session_state.questions):
            category = question['category']
            if category not in category_performance:
                category_performance[category] = {'correct': 0, 'total': 0}
            
            category_performance[category]['total'] += 1
            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == question['correct']:
                category_performance[category]['correct'] += 1
        
        for category, stats in category_performance.items():
            accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] else 0
            st.metric(f"{category}", f"{stats['correct']}/{stats['total']} ({accuracy:.0f}%)")
    
    # Question review
    st.markdown("### 📝 Question Review")
    
    for i, question in enumerate(st.session_state.questions):
        user_answer = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else None
        is_correct = (user_answer == question['correct'])
        
        with st.expander(f"Question {i+1}: {question['question'][:50]}..." + (" ✅" if is_correct else " ❌")):
            st.markdown(f"**Question:** {question['question']}")
            
            # Show all options with indicators
            for j, option in enumerate(question['options']):
                if j == question['correct']:
                    st.markdown(f"✅ **{chr(65+j)}. {option}** (Correct Answer)")
                elif j == user_answer:
                    st.markdown(f"❌ **{chr(65+j)}. {option}** (Your Answer)")
                else:
                    st.markdown(f"{chr(65+j)}. {option}")
            
            st.info(f"💡 **Explanation:** {question['explanation']}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take New Quiz", type="primary"):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.questions = []
            st.rerun()
    
    with col2:
        if st.button("📊 View History"):
            st.session_state.show_history = True
            st.rerun()
    
    with col3:
        if st.button("📥 Export Results"):
            # Create results summary
            results_summary = f"""
Quiz Results Summary
===================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Score: {score}/{total} ({percentage:.1f}%)
Categories: {', '.join(st.session_state.selected_categories)}

Detailed Breakdown:
"""
            for i, question in enumerate(st.session_state.questions):
                user_answer_idx = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else None
                user_answer = question['options'][user_answer_idx] if (user_answer_idx is not None and user_answer_idx < len(question['options'])) else "No answer"
                correct_answer = question['options'][question['correct']]
                status = "✅ Correct" if user_answer_idx == question['correct'] else "❌ Incorrect"
                
                results_summary += f"""
Q{i+1}: {question['question']}
Your Answer: {user_answer}
Correct Answer: {correct_answer}
Status: {status}
"""
            
            st.download_button(
                label="Download Results",
                data=results_summary,
                file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

def history_page():
    """Quiz history and statistics"""
    st.markdown("# 📈 Quiz History & Statistics")
    
    if not st.session_state.quiz_history:
        st.info("No quiz history yet. Take some quizzes to see your progress!")
        return
    
    # Overall statistics
    st.markdown("## 🏆 Overall Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_quizzes = len(st.session_state.quiz_history)
    total_questions = sum(q['total_questions'] for q in st.session_state.quiz_history)
    total_correct = sum(q['score'] for q in st.session_state.quiz_history)
    avg_percentage = sum(q['percentage'] for q in st.session_state.quiz_history) / total_quizzes if total_quizzes else 0
    
    with col1:
        st.metric("Total Quizzes", total_quizzes)
    with col2:
        st.metric("Questions Answered", total_questions)
    with col3:
        st.metric("Correct Answers", total_correct)
    with col4:
        st.metric("Average Score", f"{avg_percentage:.1f}%")
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        progress_chart = create_progress_chart()
        if progress_chart:
            st.plotly_chart(progress_chart, use_container_width=True)
    
    with col2:
        category_chart = create_category_performance_chart()
        if category_chart:
            st.plotly_chart(category_chart, use_container_width=True)
    
    # Detailed history table
    st.markdown("## 📋 Detailed History")
    
    history_data = []
    for i, quiz in enumerate(reversed(st.session_state.quiz_history)):
        history_data.append({
            'Quiz #': total_quizzes - i,
            'Date': quiz['date'],
            'Score': f"{quiz['score']}/{quiz['total_questions']}",
            'Percentage': f"{quiz['percentage']:.1f}%",
            'Categories': ', '.join(quiz['categories']),
            'Time': f"{quiz.get('total_time', 0):.0f}s" if 'total_time' in quiz else 'N/A'
        })
    
    st.dataframe(history_data, use_container_width=True)
    
    # Clear history option (two-step)
    if 'confirm_clear_history' not in st.session_state:
        st.session_state.confirm_clear_history = False
    
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.confirm_clear_history = True
        st.rerun()
    
    if st.session_state.confirm_clear_history:
        st.warning("Are you sure you want to permanently clear all quiz history?")
        col_yes, col_no = st.columns([1,1])
        with col_yes:
            if st.button("Yes, clear history"):
                st.session_state.quiz_history = []
                st.session_state.confirm_clear_history = False
                st.success("Quiz history cleared!")
                st.rerun()
        with col_no:
            if st.button("Cancel"):
                st.session_state.confirm_clear_history = False
                st.rerun()

# Main application
def main():
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🧠 Quiz Master Pro")
    st.sidebar.markdown("---")
    
    # Current session info
    if st.session_state.quiz_started and not st.session_state.quiz_completed:
        st.sidebar.markdown("### 🎯 Current Quiz")
        current = st.session_state.current_question + 1
        total = len(st.session_state.questions)
        if total > 0:
            st.sidebar.progress(current / total)
            st.sidebar.write(f"Question {current} of {total}")
            st.sidebar.write(f"Score: {st.session_state.score}/{max(0, current-1)}")
        
        # Timer (if enabled or started)
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            st.sidebar.markdown(f"""
            <div class="timer-display">
                ⏱️ {elapsed:.0f}s
            </div>
            """, unsafe_allow_html=True)
    
    # Navigation
    if not st.session_state.quiz_started or st.session_state.quiz_completed:
        page = st.sidebar.radio(
            "Navigate:",
            ["🏠 Home", "📈 History"],
            key="nav_radio"
        )
    
    # Quick stats in sidebar
    if st.session_state.quiz_history:
        st.sidebar.markdown("### 📊 Quick Stats")
        recent_quiz = st.session_state.quiz_history[-1]
        st.sidebar.metric("Last Score", f"{recent_quiz['percentage']:.0f}%")
        
        best_score = max(q['percentage'] for q in st.session_state.quiz_history)
        st.sidebar.metric("Best Score", f"{best_score:.0f}%")
    
    # Motivational quotes
    motivational_quotes = [
        "🧠 Knowledge is power!",
        "🎯 Every expert was once a beginner!",
        "📚 Learning never exhausts the mind!",
        "🌟 Curiosity is the key to discovery!",
        "💡 The more you learn, the more you grow!"
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.info(random.choice(motivational_quotes))
    
    # Reset quiz button
    if st.session_state.quiz_started:
        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 Restart Quiz", type="secondary"):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.rerun()
    
    # Main content
    if not st.session_state.quiz_started:
        if 'page' in locals() and page == "📈 History":
            history_page()
        else:
            home_page()
    elif st.session_state.quiz_completed:
        results_page()
    else:
        quiz_page()

if __name__ == "__main__":
    main()
