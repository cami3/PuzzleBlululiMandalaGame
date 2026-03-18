import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Blululi Experience", layout="wide")

IMAGE_FOLDER = Path("images")

if not IMAGE_FOLDER.exists():
    st.error("Missing ./images folder")
    st.stop()

def encode(path):
    with Image.open(path) as img:
        img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return {
            "name": path.stem.replace("_", " ").title(),
            "url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        }

images = [encode(p) for p in IMAGE_FOLDER.iterdir() if p.suffix.lower() in [".jpg",".png",".jpeg",".webp"]]

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body {{
  margin:0;
  font-family: Inter, sans-serif;
  background: radial-gradient(circle at top, #1a1a2e, #0f0f1a);
  color:white;
}}

.app {{
  display:flex;
  height:100vh;
}}

.sidebar {{
  width:300px;
  padding:24px;
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(20px);
}}

h1 {{
  font-size:22px;
  margin-bottom:10px;
}}

select, input {{
  width:100%;
  margin-top:10px;
  margin-bottom:20px;
}}

button {{
  width:100%;
  padding:12px;
  border:none;
  border-radius:10px;
  background: linear-gradient(135deg,#7c3aed,#a78bfa);
  color:white;
  font-weight:bold;
  cursor:pointer;
}}

.board-wrap {{
  flex:1;
  display:flex;
  justify-content:center;
  align-items:center;
}}

#board {{
  display:grid;
  gap:2px;
  padding:6px;
  border-radius:20px;
  background: rgba(255,255,255,0.06);
  box-shadow: 0 0 40px rgba(124,58,237,0.4);
}}

.tile {{
  position:relative;
  background-repeat:no-repeat;
  cursor:pointer;
  border-radius:4px;
  overflow:hidden;
}}

.tile::after {{
  content:"";
  position:absolute;
  inset:0;
  border:1px solid rgba(255,255,255,0.08);
}}

.tile.glow {{
  box-shadow: 0 0 12px rgba(167,139,250,0.6);
}}

.overlay {{
  position:fixed;
  inset:0;
  background: rgba(0,0,0,0.7);
  display:none;
  justify-content:center;
  align-items:center;
}}

.overlay.show {{
  display:flex;
}}

.modal {{
  background:#111827;
  padding:30px;
  border-radius:20px;
  text-align:center;
  max-width:400px;
}}

.modal img {{
  width:100%;
  border-radius:12px;
  margin-bottom:15px;
}}

</style>
</head>

<body>

<div class="app">

<div class="sidebar">
  <h1>Blululi Puzzle</h1>

  <label>Choose design</label>
  <select id="imgSelect"></select>

  <label>Difficulty</label>
  <input type="range" min="3" max="7" value="4" id="diff">

  <button onclick="start()">Start Puzzle</button>

  <p style="opacity:.6;font-size:14px;">
    Complete the mandala to unlock the product.
  </p>
</div>

<div class="board-wrap">
  <div id="board"></div>
</div>

</div>

<div id="overlay" class="overlay">
  <div class="modal">
    <h2>Completed ✨</h2>
    <img id="finalImg">
    <p>This mandala design is available in our shop.</p>
    <button onclick="location.href='https://blululi.com'">Shop Now</button>
  </div>
</div>

<script>

const images = {json.dumps(images)}

const board = document.getElementById("board")
const select = document.getElementById("imgSelect")
const diff = document.getElementById("diff")
const overlay = document.getElementById("overlay")
const finalImg = document.getElementById("finalImg")

let grid = 4
let arr = []
let img = ""
let selected = null

images.forEach((i,idx)=>{{
  const o=document.createElement("option")
  o.value=idx
  o.textContent=i.name
  select.appendChild(o)
}})

function start(){{
  grid = Number(diff.value)
  img = images[select.value].url

  arr = Array.from({{length:grid*grid}},(_,i)=>i)
  arr.sort(()=>Math.random()-0.5)

  render()
}}

function render(){{
  board.innerHTML=""
  board.style.gridTemplateColumns=`repeat(${grid},1fr)`

  const size = 600

  arr.forEach((p,i)=>{{
    const t=document.createElement("div")
    t.className="tile glow"

    const r=Math.floor(p/grid)
    const c=p%grid

    t.style.width = size/grid + "px"
    t.style.height = size/grid + "px"

    t.style.backgroundImage=`url(${img})`
    t.style.backgroundSize=`${size}px ${size}px`
    t.style.backgroundPosition=`-${c*(size/grid)}px -${r*(size/grid)}px`

    t.onclick=()=>click(i)

    board.appendChild(t)
  }})
}}

function click(i){{
  if(selected===null){{
    selected=i
    return
  }}

  [arr[selected],arr[i]]=[arr[i],arr[selected]]
  selected=null

  render()
  check()
}}

function check(){{
  if(arr.every((v,i)=>v===i)){{
    finalImg.src = img
    overlay.classList.add("show")
  }}
}}

start()

</script>

</body>
</html>
"""

st.components.v1.html(html, height=900)
