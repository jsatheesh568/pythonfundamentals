# rps_championship.py
import streamlit as st
import random
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------
# Page config & CSS
# ---------------------------
st.set_page_config(page_title="🪨📄✂️ Rock Paper Scissors Championship",
                   page_icon="🏆",
                   layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Poppins:wght@300;400;600;700&display=swap');

:root{
  --accent-1: #4facfe;
  --accent-2: #ff6b6b;
  --accent-3: #ffa726;
  --muted: rgba(0,0,0,0.6);
  --card-bg: #ffffff;
}

/* Dark theme overrides (works with Streamlit theme) */
@media (prefers-color-scheme: dark) {
  :root{
    --card-bg: rgba(255,255,255,0.03);
    --muted: rgba(230,230,250,0.7);
  }
}

/* Page header */
.header {
  background: linear-gradient(135deg, var(--accent-1) 0%, #764ba2 100%);
  color: white;
  padding: 28px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.18);
  font-family: 'Fredoka One', cursive;
  margin-bottom: 18px;
}

/* Page subtitle */
.sub {
  font-family: 'Poppins', sans-serif;
  color: white;
  opacity: 0.95;
  margin-top: 6px;
  font-weight: 400;
}

/* Game row */
.game-row {
  display:flex;
  gap:18px;
  flex-wrap:wrap;
}

/* Card */
.card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
  border: 1px solid rgba(0,0,0,0.04);
  min-width: 220px;
}

/* big choice buttons */
.choice-btn {
  background: linear-gradient(135deg,#89f7fe 0%, #66a6ff 100%);
  border-radius: 14px;
  padding: 18px;
  font-size: 46px;
  cursor: pointer;
  border: none;
  width:100%;
  height:120px;
  transition: transform .18s ease, box-shadow .18s ease;
  display:flex;
  align-items:center;
  justify-content:center;
}
.choice-btn:hover { transform: translateY(-6px); box-shadow: 0 14px 36px rgba(0,0,0,0.12); }
.choice-btn:active { transform: translateY(-2px); }

/* smaller variants for columns */
.choice-compact { font-size: 36px; height:90px; }

/* battle arena */
.battle {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  color:white;
  border-radius: 12px;
  padding: 18px;
  text-align:center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

/* outcome badges */
.win { background: linear-gradient(135deg,#56ab2f,#a8e6cf); color:#fff; padding:12px; border-radius:10px; font-weight:700;}
.lose { background: linear-gradient(135deg,#ff416c,#ff4b2b); color:#fff; padding:12px; border-radius:10px; font-weight:700;}
.tie  { background: linear-gradient(135deg,#ffa726,#ffb74d); color:#fff; padding:12px; border-radius:10px; font-weight:700;}

/* achievement pill */
.achievement {
  display:inline-block;
  padding:8px 12px;
  border-radius:20px;
  background: linear-gradient(45deg,#FFD700,#FFA500);
  color:#222;
  font-weight:600;
  margin:6px 6px 6px 0;
}

/* small helpers */
.muted { color: var(--muted); font-size:13px; }
.center { text-align:center; }
.small { font-size:13px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Constants & helpers
# ---------------------------
CHOICES = {"🪨": "Rock", "📄": "Paper", "✂️": "Scissors"}

def init_state():
    if "player_score" not in st.session_state:
        st.session_state.player_score = 0
    if "computer_score" not in st.session_state:
        st.session_state.computer_score = 0
    if "games_played" not in st.session_state:
        st.session_state.games_played = 0
    if "game_history" not in st.session_state:
        st.session_state.game_history = []
    if "player_choice" not in st.session_state:
        st.session_state.player_choice = None
    if "computer_choice" not in st.session_state:
        st.session_state.computer_choice = None
    if "game_result" not in st.session_state:
        st.session_state.game_result = None
    if "win_streak" not in st.session_state:
        st.session_state.win_streak = 0
    if "best_streak" not in st.session_state:
        st.session_state.best_streak = 0
    if "achievements" not in st.session_state:
        st.session_state.achievements = []
    if "show_stats" not in st.session_state:
        st.session_state.show_stats = False

def pick_random_choice():
    return random.choice(list(CHOICES.keys()))

def determine_winner(player, computer):
    if player == computer:
        return "tie"
    rules = {"🪨": "✂️", "📄": "🪨", "✂️": "📄"}
    return "player" if rules[player] == computer else "computer"

def award_achievements():
    new = []
    # first victory
    if st.session_state.player_score == 1 and "First Victory! 🏆" not in st.session_state.achievements:
        st.session_state.achievements.append("First Victory! 🏆")
        new.append("First Victory! 🏆")
    # streaks
    if st.session_state.win_streak == 3 and "Triple Threat! 🔥" not in st.session_state.achievements:
        st.session_state.achievements.append("Triple Threat! 🔥"); new.append("Triple Threat! 🔥")
    if st.session_state.win_streak == 5 and "Unstoppable! ⚡" not in st.session_state.achievements:
        st.session_state.achievements.append("Unstoppable! ⚡"); new.append("Unstoppable! ⚡")
    if st.session_state.win_streak == 10 and "Legend! 🌟" not in st.session_state.achievements:
        st.session_state.achievements.append("Legend! 🌟"); new.append("Legend! 🌟")
    # play count
    if st.session_state.games_played == 10 and "Getting Started! 🎯" not in st.session_state.achievements:
        st.session_state.achievements.append("Getting Started! 🎯"); new.append("Getting Started! 🎯")
    if st.session_state.games_played == 50 and "Dedicated Player! 🎮" not in st.session_state.achievements:
        st.session_state.achievements.append("Dedicated Player! 🎮"); new.append("Dedicated Player! 🎮")
    if st.session_state.games_played == 100 and "Century Club! 💯" not in st.session_state.achievements:
        st.session_state.achievements.append("Century Club! 💯"); new.append("Century Club! 💯")
    if st.session_state.player_score == 10 and "Double Digits! 🔟" not in st.session_state.achievements:
        st.session_state.achievements.append("Double Digits! 🔟"); new.append("Double Digits! 🔟")
    return new

def record_game(player_choice, computer_choice, result):
    st.session_state.games_played += 1
    record = {
        "game_number": st.session_state.games_played,
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.game_history.append(record)
    if result == "player":
        st.session_state.player_score += 1
        st.session_state.win_streak += 1
        if st.session_state.win_streak > st.session_state.best_streak:
            st.session_state.best_streak = st.session_state.win_streak
    elif result == "computer":
        st.session_state.computer_score += 1
        st.session_state.win_streak = 0
    # tie: streak unchanged

# ---------------------------
# UI pieces
# ---------------------------
def render_header():
    st.markdown(
        """
        <div class="header">
            <h1 style="margin:0">🪨📄✂️ Rock Paper Scissors Championship</h1>
            <div class="sub">Human vs Computer — quick rounds, big achievements!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_score_cards():
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        st.markdown(f'<div class="card center"><h4 style="margin:4px">👤 YOU</h4><h2 style="margin:4px;color:var(--accent-1)">{st.session_state.player_score}</h2><div class="muted small">Player wins</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card center"><h4 style="margin:4px">🤖 COMPUTER</h4><h2 style="margin:4px;color:var(--accent-2)">{st.session_state.computer_score}</h2><div class="muted small">Computer wins</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card center"><h4 style="margin:4px">🎮 GAMES</h4><h2 style="margin:4px;color:var(--accent-3)">{st.session_state.games_played}</h2><div class="muted small">Rounds played</div></div>', unsafe_allow_html=True)
    with c4:
        streak_display = f"🔥 {st.session_state.win_streak}" if st.session_state.win_streak > 0 else "0"
        st.markdown(f'<div class="card center"><h4 style="margin:4px">STREAK</h4><h2 style="margin:4px;color:#56ab2f">{streak_display}</h2><div class="muted small">Best: {st.session_state.best_streak}</div></div>', unsafe_allow_html=True)

def render_choices():
    st.markdown("### 🎯 Choose Your Weapon")
    cols = st.columns(3)
    with cols[0]:
        st.button("🪨", key="btn_rock", help="Rock crushes Scissors", on_click=on_choice, args=("🪨",))
    with cols[1]:
        st.button("📄", key="btn_paper", help="Paper covers Rock", on_click=on_choice, args=("📄",))
    with cols[2]:
        st.button("✂️", key="btn_scissors", help="Scissors cuts Paper", on_click=on_choice, args=("✂️",))

def render_battle():
    if st.session_state.game_result is None:
        return
    # show the battle area
    st.markdown('<div class="battle">⚔️ BATTLE ARENA ⚔️</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1,0.4,1])
    with b1:
        st.markdown(f'<div class="card center"><h4 style="margin:4px">YOU</h4><div style="font-size:68px">{st.session_state.player_choice}</div><div class="muted">{CHOICES[st.session_state.player_choice]}</div></div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div style="text-align:center; font-size:28px; margin-top:24px">VS</div>', unsafe_allow_html=True)
    with b3:
        st.markdown(f'<div class="card center"><h4 style="margin:4px">COMPUTER</h4><div style="font-size:68px">{st.session_state.computer_choice}</div><div class="muted">{CHOICES[st.session_state.computer_choice]}</div></div>', unsafe_allow_html=True)

    # result badge
    if st.session_state.game_result == "player":
        st.markdown('<div class="win center" style="margin-top:12px">🎉 YOU WIN! 🎉</div>', unsafe_allow_html=True)
    elif st.session_state.game_result == "computer":
        st.markdown('<div class="lose center" style="margin-top:12px">💔 YOU LOSE! 💔</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="tie center" style="margin-top:12px">🤝 IT\'S A TIE!</div>', unsafe_allow_html=True)

def render_controls():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("🔄 New Round", on_click=reset_round)
    with c2:
        st.button("📊 Toggle Statistics", on_click=toggle_stats)
    with c3:
        st.button("🗑️ Reset Everything", on_click=confirm_reset)

def render_achievements():
    if not st.session_state.achievements:
        return
    st.markdown("### 🏆 Achievements")
    badges = ""
    for ach in st.session_state.achievements:
        badges += f'<span class="achievement">{ach}</span>'
    st.markdown(badges, unsafe_allow_html=True)

def render_stats_panel():
    if not st.session_state.show_stats:
        return
    st.markdown("---")
    st.markdown("## 📊 Statistics & History")
    # Score chart
    fig = go.Figure(go.Bar(x=["Player", "Computer"],
                           y=[st.session_state.player_score, st.session_state.computer_score],
                           marker_color=[ "#4facfe", "#ff6b6b" ],
                           text=[st.session_state.player_score, st.session_state.computer_score],
                           textposition="auto"))
    fig.update_layout(title="Score Comparison", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=360)
    st.plotly_chart(fig, use_container_width=True)

    # Choice distribution
    if st.session_state.game_history:
        counts = {"🪨":0,"📄":0,"✂️":0}
        for g in st.session_state.game_history:
            counts[g["player_choice"]] += 1
        pie = px.pie(values=list(counts.values()), names=[f"{k} {CHOICES[k]}" for k in counts.keys()], title="Your Choice Distribution")
        st.plotly_chart(pie, use_container_width=True)

    # recent games table
    if st.session_state.game_history:
        recent = st.session_state.game_history[-12:][::-1]
        df = pd.DataFrame([{
            "Game #": r["game_number"],
            "You": f'{r["player_choice"]} {CHOICES[r["player_choice"]]}',
            "Computer": f'{r["computer_choice"]} {CHOICES[r["computer_choice"]]}',
            "Result": ("Win" if r["result"]=="player" else "Lose" if r["result"]=="computer" else "Tie"),
            "Time": r["timestamp"]
        } for r in recent])
        st.dataframe(df, use_container_width=True)
        csv = pd.DataFrame(st.session_state.game_history).to_csv(index=False)
        st.download_button("📥 Export Full History (CSV)", csv, file_name=f"rps_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")

# ---------------------------
# Callbacks (safe updates)
# ---------------------------
def on_choice(choice):
    # Choose and resolve round
    st.session_state.player_choice = choice
    comp = pick_random_choice()
    st.session_state.computer_choice = comp
    result = determine_winner(choice, comp)
    st.session_state.game_result = result
    record_game(choice, comp, result)
    new = award_achievements()
    # show a little indicator (streamlit messages persist until rerun)
    if new:
        # flash a success message
        st.success(f"New achievement(s): {', '.join(new)}")

def reset_round():
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.session_state.game_result = None

def toggle_stats():
    st.session_state.show_stats = not st.session_state.show_stats

def confirm_reset():
    # Confirm by showing a st.modal-like flow using st.confirmation pattern:
    if st.session_state.get("_reset_confirm", False):
        # Reset now
        keys = ["player_score","computer_score","games_played","game_history","player_choice","computer_choice","game_result","win_streak","best_streak","achievements"]
        for k in keys:
            if k in st.session_state:
                if isinstance(st.session_state[k], list):
                    st.session_state[k] = []
                else:
                    st.session_state[k] = 0 if isinstance(st.session_state[k], int) else None
        st.success("All progress has been reset.")
        st.session_state["_reset_confirm"] = False
    else:
        st.session_state["_reset_confirm"] = True
        st.warning("Press Reset Everything again to confirm. This is a destructive action.")

# ---------------------------
# App layout
# ---------------------------
def app():
    init_state()
    render_header()
    render_score_cards()

    # Main layout: choices and battle area side by side on wide screens
    left, right = st.columns([2, 1])
    with left:
        render_choices()
        render_battle()
        render_controls()
    with right:
        st.markdown('<div class="card"><h3 style="margin-top:4px">Quick Info</h3><p class="muted small">Click an emoji button to play a round. Use the controls below the arena for new rounds or toggling statistics.</p></div>', unsafe_allow_html=True)
        render_achievements()
        if st.session_state.achievements:
            st.markdown('<div class="muted small" style="margin-top:8px">Tip: achievements persist until you reset them.</div>', unsafe_allow_html=True)

    render_stats_panel()

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app()
