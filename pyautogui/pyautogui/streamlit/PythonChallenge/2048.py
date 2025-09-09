# 2048.py
import streamlit as st
import random
import copy
from typing import List, Tuple
import streamlit.components.v1 as components
st.set_page_config(page_title="2048 (Streamlit)", layout="centered")

Board = List[List[int]]

# ---------- Game logic (classic 2048) ----------
def new_board(size: int = 4) -> Board:
    return [[0] * size for _ in range(size)]

def add_random_tile(board: Board, probs=(0.9, 0.1)):
    empty = [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == 0]
    if not empty:
        return False
    r, c = random.choice(empty)
    board[r][c] = 2 if random.random() < probs[0] else 4
    return True

def compact_and_merge_line(line: List[int]) -> Tuple[List[int], int]:
    new_line = [x for x in line if x != 0]
    score = 0
    i = 0
    out = []
    while i < len(new_line):
        if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
            merged = new_line[i] * 2
            out.append(merged)
            score += merged
            i += 2
        else:
            out.append(new_line[i])
            i += 1
    out.extend([0] * (len(line) - len(out)))
    return out, score

def transpose(board: Board) -> Board:
    size = len(board)
    return [[board[r][c] for r in range(size)] for c in range(size)]

def reverse_rows(board: Board) -> Board:
    return [list(reversed(row)) for row in board]

def move_left(board: Board) -> Tuple[Board, int, bool]:
    size = len(board)
    new = new_board(size)
    total_score = 0
    moved = False
    for r in range(size):
        out, score = compact_and_merge_line(board[r])
        new[r] = out
        total_score += score
        if out != board[r]:
            moved = True
    return new, total_score, moved

def move_right(board: Board) -> Tuple[Board, int, bool]:
    rev = reverse_rows(board)
    new_rev, score, moved = move_left(rev)
    new = reverse_rows(new_rev)
    return new, score, moved

def move_up(board: Board) -> Tuple[Board, int, bool]:
    tr = transpose(board)
    new_tr, score, moved = move_left(tr)
    new = transpose(new_tr)
    return new, score, moved

def move_down(board: Board) -> Tuple[Board, int, bool]:
    tr = transpose(board)
    new_tr, score, moved = move_right(tr)
    new = transpose(new_tr)
    return new, score, moved

def can_move(board: Board) -> bool:
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == 0:
                return True
    for r in range(size):
        for c in range(size - 1):
            if board[r][c] == board[r][c + 1]:
                return True
    for c in range(size):
        for r in range(size - 1):
            if board[r][c] == board[r + 1][c]:
                return True
    return False

def board_max(board: Board) -> int:
    return max(max(row) for row in board)

# ---------- Session state helpers ----------
def init_session(size: int = 4):
    if "board" not in st.session_state:
        board = new_board(size)
        add_random_tile(board)
        add_random_tile(board)
        st.session_state.board = board
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "history" not in st.session_state:
        st.session_state.history = []  # list of (board, score)
    if "won" not in st.session_state:
        st.session_state.won = False
    if "best_score" not in st.session_state:
        st.session_state.best_score = 0
    if "size" not in st.session_state:
        st.session_state.size = size

def restart_game():
    size = st.session_state.get("size", 4)
    board = new_board(size)
    add_random_tile(board)
    add_random_tile(board)
    st.session_state.board = board
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.won = False

def do_move(direction: str):
    board = st.session_state.board
    score = st.session_state.score
    if not can_move(board):
        return
    if direction == "left":
        new_board_state, gained, moved = move_left(board)
    elif direction == "right":
        new_board_state, gained, moved = move_right(board)
    elif direction == "up":
        new_board_state, gained, moved = move_up(board)
    elif direction == "down":
        new_board_state, gained, moved = move_down(board)
    else:
        return

    if moved:
        st.session_state.history.append((copy.deepcopy(board), score))
        st.session_state.board = new_board_state
        st.session_state.score += gained
        if st.session_state.score > st.session_state.best_score:
            st.session_state.best_score = st.session_state.score
        add_random_tile(st.session_state.board)
        if board_max(st.session_state.board) >= 2048:
            st.session_state.won = True

def undo_move():
    if st.session_state.history:
        board, score = st.session_state.history.pop()
        st.session_state.board = board
        st.session_state.score = score

# ---------- HTML/CSS renderer for the board ----------
def render_board_html():
    board = st.session_state.board
    size = st.session_state.size
    # CSS styling - compact and similar to screenshot
    css = f"""
    <style>
      .game-wrapper {{
        display:flex;
        justify-content:center;
        margin-top: 12px;
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat({size}, 110px);
        grid-gap: 14px;
        background: rgba(0,0,0,0.05);
        padding: 18px;
        border-radius: 12px;
      }}
      .tile {{
        height: 88px;
        width: 110px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-family: "Arial", sans-serif;
        font-size: 26px;
        box-shadow: inset 0 -4px 0 rgba(0,0,0,0.08);
      }}
      .tile-empty {{
        background: rgba(255,255,255,0.03);
        color: #ddd;
      }}
      /* color mapping, fallback dark look */
      .t2 {{ background:#eee4da; color:#776e65; }}
      .t4 {{ background:#ede0c8; color:#776e65; }}
      .t8 {{ background:#f2b179; color:#f9f6f2; }}
      .t16 {{ background:#f59563; color:#f9f6f2; }}
      .t32 {{ background:#f67c5f; color:#f9f6f2; }}
      .t64 {{ background:#f65e3b; color:#f9f6f2; }}
      .t128 {{ background:#edcf72; color:#f9f6f2; font-size:20px; }}
      .t256 {{ background:#edcc61; color:#f9f6f2; font-size:20px; }}
      .t512 {{ background:#edc850; color:#f9f6f2; font-size:18px; }}
      .t1024 {{ background:#edc53f; color:#f9f6f2; font-size:16px; }}
      .t2048 {{ background:#edc22e; color:#f9f6f2; font-size:16px; }}
      .controls {{
        display:flex;
        gap:8px;
        justify-content:center;
        margin-top:12px;
      }}
      .btn {{
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.1));
        border-radius:8px;
        padding:8px 12px;
        color: #f1f1f1;
        border: none;
        cursor: pointer;
        font-weight:600;
      }}
    </style>
    """

    # Build grid HTML
    tile_html = ""
    for r in range(size):
        for c in range(size):
            v = board[r][c]
            if v == 0:
                tile_html += f'<div class="tile tile-empty"></div>'
            else:
                cls = f"t{v}" if v <= 2048 else "t2048"
                tile_html += f'<div class="tile {cls}">{v}</div>'

    html = f"""
    {css}
    <div class="game-wrapper">
      <div class="grid">
        {tile_html}
      </div>
    </div>
    """

    # render with components.html so HTML/CSS render exactly
    # height must be enough to show grid; compute roughly:
    height = 140 + size * 106
    components.html(html, height=height, scrolling=False)

# ---------- App UI ----------
st.title("2048 — Streamlit Edition ✨")
st.write("Use the arrow buttons (or click) to move tiles. Reach 2048 to win. Undo and Restart supported.")

init_session(size=4)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    st.metric("Best", st.session_state.best_score)
with col3:
    if st.button("Restart 🔁"):
        restart_game()
    st.markdown("")  # spacing
    if st.button("Undo ↶"):
        undo_move()

# status messages
if st.session_state.won:
    st.success("🎉 You reached 2048! Keep playing or Restart.")
if not can_move(st.session_state.board):
    st.error("Game Over — no more moves. Press Restart to play again.")

# render the board using HTML/CSS
render_board_html()

# movement controls
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⬆️ Up"):
        do_move("up")
left, middle, right = st.columns([1, 1, 1])
with left:
    if st.button("⬅️ Left"):
        do_move("left")
with right:
    if st.button("➡️ Right"):
        do_move("right")
with c2:
    if st.button("⬇️ Down"):
        do_move("down")

st.markdown("---")
st.caption("Tip: to enable keyboard controls, I can add a small JS component; want that?")

# optional deploy instructions
with st.expander("How to deploy"):
    st.write("""
    1. Save as `2048.py`.
    2. `pip install streamlit`
    3. `streamlit run 2048.py`
    4. To deploy: push to GitHub and use Streamlit Community Cloud (share.streamlit.io).
    """)

