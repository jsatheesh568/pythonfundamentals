import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🐍 Snake Game", page_icon="🎮", layout="wide")

HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    :root{
      --cell-size:18px;
      --board-bg:#0d0d0d;
      --border:#00ff88;
      --head:#00ff88;
      --body:#00cc6a;
      --food:#ff4757;
    }
    body { margin:0; background:linear-gradient(135deg,#667eea,#764ba2); font-family:Arial, sans-serif; color:#fff; }
    .container{ padding:18px; max-width:960px; margin:18px auto; }
    h1{ margin:0 0 12px 0; font-size:24px; }
    .score{ color:var(--border); font-size:18px; margin:8px 0; }
    .hint{ color:#e6ffed; font-size:13px; margin-bottom:10px; }
    .board-wrap{ background:var(--board-bg); border:4px solid var(--border); padding:6px; border-radius:10px; display:inline-block; box-shadow:0 0 20px var(--border); }
    .row{ height:var(--cell-size); line-height:0; }
    .cell{ width:var(--cell-size); height:var(--cell-size); display:inline-block; box-sizing:border-box; border:1px solid rgba(0,255,136,0.06); margin:0; padding:0; }
    .snake-head{ background:var(--head); border-radius:50%; }
    .snake-body{ background:var(--body); border-radius:20%; }
    .food{ background:var(--food); border-radius:50%; }
    .controls{ margin-top:12px; display:flex; gap:8px; align-items:center; }
    .btn{ padding:8px 12px; border-radius:8px; border:none; cursor:pointer; background:#222; color:#fff; }
    .btn:active{ transform:translateY(1px); }
    .gameover{ margin-top:12px;padding:10px;border-radius:8px;background:linear-gradient(90deg,#ff6b6b,#ff9a66);color:#fff; }
    @media (max-width:640px){
      :root{ --cell-size:16px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🐍 SNAKE GAME</h1>
    <div class="hint">Click anywhere in the board and use Arrow keys or WASD to move. Space to start/pause. R to restart.</div>
    <div class="score" id="score">Score: 0</div>

    <div id="boardContainer" class="board-wrap" tabindex="0" aria-label="Snake game board"></div>

    <div class="controls">
      <button id="startPauseBtn" class="btn">Start</button>
      <button id="restartBtn" class="btn">Restart</button>
      <div style="margin-left:8px;color:#dfefff;font-size:13px;">Use arrow keys or WASD</div>
    </div>

    <div id="gameOver" style="display:none;" class="gameover"><strong>🎮 GAME OVER</strong><div id="finalScore"></div></div>
  </div>

<script>
(function(){
  // Configuration
  const BOARD_WIDTH = 20;
  const BOARD_HEIGHT = 15;
  const CELL = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--cell-size')) || 18;
  const SPEED = 120; // ms per tick (lower -> faster)

  // State
  let snake = [{x: Math.floor(BOARD_WIDTH/2), y: Math.floor(BOARD_HEIGHT/2)}];
  let dir = {x:1, y:0}; // RIGHT
  let food = null;
  let score = 0;
  let running = false;
  let gameOver = false;
  let tickTimer = null;

  // Elements
  const boardContainer = document.getElementById('boardContainer');
  const scoreEl = document.getElementById('score');
  const startPauseBtn = document.getElementById('startPauseBtn');
  const restartBtn = document.getElementById('restartBtn');
  const gameOverEl = document.getElementById('gameOver');
  const finalScore = document.getElementById('finalScore');

  // Build board grid once and keep references
  const cells = [];
  function buildBoard(){
    boardContainer.innerHTML = '';
    for(let y=0;y<BOARD_HEIGHT;y++){
      const row = document.createElement('div');
      row.className = 'row';
      for(let x=0;x<BOARD_WIDTH;x++){
        const c = document.createElement('div');
        c.className = 'cell';
        c.style.width = CELL + 'px';
        c.style.height = CELL + 'px';
        c.dataset.x = x; c.dataset.y = y;
        row.appendChild(c);
        cells.push(c);
      }
      boardContainer.appendChild(row);
    }
  }

  function getCell(x,y){
    if(x<0 || y<0 || x>=BOARD_WIDTH || y>=BOARD_HEIGHT) return null;
    return cells[y*BOARD_WIDTH + x];
  }

  function placeFood(){
    while(true){
      const fx = Math.floor(Math.random()*BOARD_WIDTH);
      const fy = Math.floor(Math.random()*BOARD_HEIGHT);
      if(!snake.some(s => s.x===fx && s.y===fy)){
        food = {x:fx,y:fy};
        break;
      }
    }
  }

  function draw(){
    // clear all
    for(const c of cells){
      c.className = 'cell';
    }
    // food
    if(food){
      const fcell = getCell(food.x, food.y);
      if(fcell) fcell.classList.add('food');
    }
    // snake
    for(let i=0;i<snake.length;i++){
      const s = snake[i];
      const cell = getCell(s.x, s.y);
      if(!cell) continue;
      if(i===0) cell.classList.add('snake-head');
      else cell.classList.add('snake-body');
    }
    scoreEl.textContent = 'Score: ' + score;
  }

  function resetGame(){
    snake = [{x: Math.floor(BOARD_WIDTH/2), y: Math.floor(BOARD_HEIGHT/2)}];
    dir = {x:1,y:0};
    score = 0;
    gameOver = false;
    running = false;
    gameOverEl.style.display = 'none';
    startPauseBtn.textContent = 'Start';
    placeFood();
    draw();
    if(tickTimer){ clearInterval(tickTimer); tickTimer = null; }
  }

  function step(){
    if(gameOver || !running) return;
    const head = {...snake[0]};
    const nx = head.x + dir.x;
    const ny = head.y + dir.y;
    // wall collision
    if(nx<0 || ny<0 || nx>=BOARD_WIDTH || ny>=BOARD_HEIGHT){
      endGame();
      return;
    }
    // self collision
    if(snake.some(p => p.x===nx && p.y===ny)){
      endGame();
      return;
    }
    // move
    snake.unshift({x:nx,y:ny});
    if(food && nx===food.x && ny===food.y){
      score += 10;
      placeFood();
    } else {
      snake.pop();
    }
    draw();
  }

  function endGame(){
    gameOver = true;
    running = false;
    if(tickTimer){ clearInterval(tickTimer); tickTimer = null; }
    finalScore.textContent = 'Score: ' + score;
    gameOverEl.style.display = 'block';
    startPauseBtn.textContent = 'Start';
  }

  function setDirection(name){
    const opposites = {Up:'Down',Down:'Up',Left:'Right',Right:'Left'};
    // map name to vector
    const map = {Up:{x:0,y:-1}, Down:{x:0,y:1}, Left:{x:-1,y:0}, Right:{x:1,y:0}};
    if(!map[name]) return;
    const nd = map[name];
    // prevent reversing
    if(snake.length>1 && nd.x === -dir.x && nd.y === -dir.y) return;
    dir = nd;
  }

  // Keyboard handling
  function handleKey(e){
    const k = e.key;
    if(k==='ArrowUp' || k==='w' || k==='W') { setDirection('Up'); e.preventDefault(); }
    else if(k==='ArrowDown' || k==='s' || k==='S') { setDirection('Down'); e.preventDefault(); }
    else if(k==='ArrowLeft' || k==='a' || k==='A') { setDirection('Left'); e.preventDefault(); }
    else if(k==='ArrowRight' || k==='d' || k==='D') { setDirection('Right'); e.preventDefault(); }
    else if(k===' ' || k==='Spacebar'){ // start/pause
      toggleRun();
      e.preventDefault();
    } else if(k==='r' || k==='R'){
      resetGame();
      e.preventDefault();
    }
  }

  function toggleRun(){
    if(gameOver) return;
    running = !running;
    startPauseBtn.textContent = running ? 'Pause' : 'Start';
    if(running && !tickTimer){
      tickTimer = setInterval(step, SPEED);
    } else if(!running && tickTimer){
      clearInterval(tickTimer);
      tickTimer = null;
    }
  }

  // Buttons
  startPauseBtn.addEventListener('click', function(){ toggleRun(); boardContainer.focus(); });
  restartBtn.addEventListener('click', function(){ resetGame(); boardContainer.focus(); });

  // Focus board on click so keys go to iframe
  boardContainer.addEventListener('click', function(){ boardContainer.focus(); });

  // attach keyboard on document inside iframe
  window.addEventListener('keydown', handleKey, {passive:false});

  // init
  buildBoard();
  placeFood();
  draw();
  boardContainer.focus();

})();
</script>
</body>
</html>
"""

# embed the entire game as an iframe component so the iframe owns focus and keyboard events
components.html(HTML, height=600, scrolling=True)
