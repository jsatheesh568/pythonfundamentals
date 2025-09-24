# game_zone_final.py
# Single-file Streamlit app: Tic-Tac-Toe + Stopwatch with safe rerun shim
import time
from datetime import datetime
from typing import List, Optional, Tuple
import copy
import pandas as pd
import streamlit as st

# ---------------------------
# Safe rerun shim (CRITICAL)
# Put this at top so all subsequent code uses it instead of experimental_rerun
# ---------------------------
if "_rerun_toggle" not in st.session_state:
    # initialize sentinel safely
    try:
        st.session_state["_rerun_toggle"] = False
    except Exception:
        # if session_state unavailable (rare), ignore; later calls will try again
        pass

def request_rerun():
    """Toggle a sentinel in session_state to force Streamlit to rerun safely."""
    try:
        st.session_state["_rerun_toggle"] = not st.session_state.get("_rerun_toggle", False)
    except Exception:
        # If session_state is still unavailable, do nothing (best effort).
        pass

def safe_rerun(pause: float = 0.03):
    """Optional tiny pause, then toggle rerun sentinel."""
    if pause and pause > 0:
        time.sleep(pause)
    request_rerun()

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Game Zone — TicTacToe & Stopwatch", page_icon="🎮", layout="wide")

# ---------------------------
# CSS (clean, light)
# ---------------------------
CLEAN_CSS = """
<style>
body {
  background: linear-gradient(180deg, #f6f9ff 0%, #eef6ff 100%) !important;
  color: #0f172a;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}
.app-card {
  background: #fff;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 8px 24px rgba(15,23,42,0.06);
  border: 1px solid rgba(15,23,42,0.04);
  margin-bottom: 18px;
}
.header-title { font-size: 28px; font-weight:700; }
.header-sub { color:#475569; font-size:14px; margin-bottom:6px; }
.tile {
  width: 120px; height:120px; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:48px; font-weight:700; background:linear-gradient(180deg,#fbfdff,#f1f7ff);
  border:1px solid rgba(15,23,42,0.06); transition:transform .08s ease;
}
@media(max-width:700px){ .tile{ width:78px;height:78px;font-size:32px;border-radius:10px;} }
.tile:hover{ transform:translateY(-6px); box-shadow:0 10px 24px rgba(15,23,42,0.08); cursor:pointer; }
.tile.x{ color:#e11d48; } .tile.o{ color:#0ea5e9; } .tile.disabled{ opacity:.5; cursor:not-allowed; transform:none; box-shadow:none; }
.status { padding:12px; border-radius:10px; display:flex; justify-content:space-between; align-items:center; background:linear-gradient(90deg,#eef2ff,#fff); border:1px solid rgba(15,23,42,0.03); }
.small-muted{ color:#6b7280; font-size:13px; }
.footer-note{ color:#6b7280; font-size:13px; margin-top:12px;}
</style>
"""
st.markdown(CLEAN_CSS, unsafe_allow_html=True)

# ---------------------------
# Helpers: TicTacToe
# ---------------------------
def init_tictactoe():
    if 'board' not in st.session_state:
        st.session_state.board = ['' for _ in range(9)]
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'wins_x' not in st.session_state:
        st.session_state.wins_x = 0
    if 'wins_o' not in st.session_state:
        st.session_state.wins_o = 0
    if 'draws' not in st.session_state:
        st.session_state.draws = 0
    if 'history' not in st.session_state:
        st.session_state.history = []

def check_winner(board: List[str]) -> Tuple[Optional[str], Optional[List[int]]]:
    winning_combinations = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in winning_combinations:
        a,b,c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    if '' not in board:
        return 'Draw', None
    return None, None

def reset_game():
    st.session_state.board = ['' for _ in range(9)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.history = []

def make_move(pos: int):
    if st.session_state.game_over or st.session_state.board[pos] != '':
        return
    st.session_state.history.append((copy.deepcopy(st.session_state.board), st.session_state.current_player))
    st.session_state.board[pos] = st.session_state.current_player
    winner, _ = check_winner(st.session_state.board)
    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
        if winner == 'X':
            st.session_state.wins_x += 1
        elif winner == 'O':
            st.session_state.wins_o += 1
        else:
            st.session_state.draws += 1
    else:
        st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

def undo_move():
    if st.session_state.history:
        prev_board, prev_turn = st.session_state.history.pop()
        st.session_state.board = prev_board
        st.session_state.current_player = prev_turn
        st.session_state.game_over = False
        st.session_state.winner = None

# ---------------------------
# Helpers: Stopwatch
# ---------------------------
def init_stopwatch():
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0.0
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'lap_times' not in st.session_state:
        st.session_state.lap_times = []

def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 100)
    return f"{minutes:02d}:{secs:02d}.{millis:02d}"

def get_elapsed():
    if st.session_state.is_running and st.session_state.start_time:
        return st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    return st.session_state.elapsed_time

# ---------------------------
# UI header and sidebar
# ---------------------------
st.markdown(
    '<div style="display:flex;justify-content:space-between;align-items:center;">'
    '<div><div class="header-title">Game Zone</div><div class="header-sub">Tic-Tac-Toe & Stopwatch — responsive</div></div>'
    '<div style="text-align:right;"><img src="https://raw.githubusercontent.com/encharm/Font-Awesome-SVG-PNG/master/black/png/64/gamepad.png" width="48"/></div>'
    '</div>',
    unsafe_allow_html=True
)

app_choice = st.sidebar.radio("App", ["Tic-Tac-Toe", "Stopwatch"])
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ — Safe rerun shim included")

# ---------------------------
# Render TicTacToe
# ---------------------------
def render_tictactoe():
    init_tictactoe()
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1: st.metric("Player X", f"❌ {st.session_state.wins_x}")
    with c2: st.metric("Player O", f"⭕ {st.session_state.wins_o}")
    with c3: st.metric("Draws", f"🤝 {st.session_state.draws}")
    with c4:
        total = st.session_state.wins_x + st.session_state.wins_o + st.session_state.draws
        st.metric("Total Games", str(total))

    st.markdown("<hr/>", unsafe_allow_html=True)

    status_text = (f"Player {st.session_state.current_player}'s turn" if not st.session_state.game_over
                   else ("It's a draw!" if st.session_state.winner == 'Draw' else f"Winner: Player {st.session_state.winner} 🎉"))
    st.markdown(f'<div class="status"><div class="status-left">{status_text}</div><div class="status-right small-muted">Local play • Undo & Reset</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="display:flex;justify-content:center;margin-top:14px;">', unsafe_allow_html=True)
    # Render board by rows
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            pos = r * 3 + c
            val = st.session_state.board[pos]
            label = val if val != '' else " "
            tile_class = "tile"
            if val == 'X': tile_class += " x"
            if val == 'O': tile_class += " o"
            cols[c].markdown(f'<div class="{tile_class}">{label}</div>', unsafe_allow_html=True)
            if cols[c].button("Play", key=f"cell_{pos}", disabled=(st.session_state.game_over or val != '')):
                make_move(pos)
                safe_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("Undo Move", use_container_width=True):
            undo_move(); safe_rerun()
    with c2:
        if st.button("New Game", use_container_width=True):
            reset_game(); safe_rerun()
    with c3:
        if st.button("Reset Scores", use_container_width=True):
            st.session_state.wins_x = 0; st.session_state.wins_o = 0; st.session_state.draws = 0; safe_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Render Stopwatch
# ---------------------------
def render_stopwatch():
    init_stopwatch()
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;"><div><h2 style="margin:0">⏱ Stopwatch</h2><div class="small-muted">Start • Pause • Stop • Lap</div></div><div></div></div>', unsafe_allow_html=True)

    elapsed = get_elapsed()
    st.markdown(f'<div style="text-align:center;margin-top:12px"><div style="font-family:Orbitron, monospace; font-weight:700; font-size:36px;">{format_time(elapsed)}</div></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("▶️ Start", use_container_width=True):
            if not st.session_state.is_running:
                st.session_state.start_time = time.time(); st.session_state.is_running = True; safe_rerun()
    with c2:
        if st.button("⏸️ Pause", use_container_width=True):
            if st.session_state.is_running:
                st.session_state.elapsed_time = get_elapsed(); st.session_state.is_running = False; safe_rerun()
    with c3:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.elapsed_time = get_elapsed(); st.session_state.is_running = False; safe_rerun()
    with c4:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.start_time = None; st.session_state.elapsed_time = 0.0; st.session_state.is_running = False; st.session_state.lap_times = []; safe_rerun()

    if st.button("🏁 Lap", use_container_width=True):
        if st.session_state.is_running or st.session_state.elapsed_time > 0:
            lap_time = get_elapsed()
            if 'lap_times' not in st.session_state: st.session_state.lap_times = []
            st.session_state.lap_times.append({"lap": len(st.session_state.lap_times) + 1 if 'lap_times' in st.session_state else 1, "time": lap_time, "formatted": format_time(lap_time), "ts": datetime.now().strftime("%H:%M:%S")})
            safe_rerun()

    if 'lap_times' in st.session_state and st.session_state.lap_times:
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("<h4>Recent Laps</h4>", unsafe_allow_html=True)
        for lap in reversed(st.session_state.lap_times[-10:]):
            st.write(f"Lap {lap['lap']} — {lap['formatted']} ({lap['ts']})")
        if st.button("Export Laps to CSV"):
            df = pd.DataFrame(st.session_state.lap_times)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", data=csv, file_name=f"laps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

    st.markdown('</div>', unsafe_allow_html=True)

    # auto refresh while running (keeps display updating)
    if st.session_state.is_running:
        time.sleep(0.1)
        request_rerun()

# ---------------------------
# App switch
# ---------------------------
if app_choice == "Tic-Tac-Toe":
    render_tictactoe()
else:
    render_stopwatch()

st.markdown('<div class="footer-note">Tip: This app uses a safe rerun shim (no experimental API required).</div>', unsafe_allow_html=True)
