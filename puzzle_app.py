import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

IMAGE_FOLDER = Path("images")

def encode(path):
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)

    return {
        "name": path.stem,
        "url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
        "w": w,
        "h": h
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
  background:#0f172a;
  color:white;
}}

.app {{
  display:flex;
  height:100vh;
}}

.sidebar {{
  width:280px;
  background:#111827;
  padding:20px;
}}

.main {{
  flex:1;
  display:flex;
  justify-content:center;
  align-items:center;
}}

#board {{
  display:grid;
  gap:2px;
  background:#020617;
  padding:4px;
  border-radius:16px;
}}

.tile {{
  background-repeat:no-repeat;
  cursor:pointer;
  border-radius:4px;
  transition: transform .1s;
}}

.tile:hover {{
  transform: scale(1.02);
}}

select, input, button {{
  width:100%;
  margin-top:10px;
  padding:10px;
  border-radius:8px;
  border:none;
}}

button {{
  background:#7c3aed;
  color:white;
  font-weight:bold;
}}

.preview {{
  width:100%;
  margin-top:20px;
  border-radius:10px;
}}

</style>
</head>

<body>

<div class="app">

<div class="sidebar">
  <h2>Puzzle</h2>

  <select id="imgSelect"></select>
  <input type="range" id="diff" min="2" max="8" value="4">
  <button onclick="newGame()">Shuffle</button>

  <img id="preview" class="preview">
</div>

<div class="main">
  <div id="board"></div>
</div>

</div>

<script>

const images = {json.dumps(images)}

const board = document.getElementById("board")
const select = document.getElementById("imgSelect")
const diff = document.getElementById("diff")
const preview = document.getElementById("preview")

let grid = 4
let arr = []
let selected = null
let current = images[0]

function init() {{
  images.forEach((img,i)=>{{
    let o=document.createElement("option")
    o.value=i
    o.textContent=img.name
    select.appendChild(o)
  }})
  updateImage()
  newGame()
}}

function updateImage(){{
  current = images[select.value]
  preview.src = current.url
}}

select.onchange = ()=>{{ updateImage(); newGame() }}
diff.onchange = ()=>{{ grid = Number(diff.value); newGame() }}

function shuffle(a){{
  return a.sort(()=>Math.random()-0.5)
}}

function newGame(){{
  arr = shuffle([...Array(grid*grid).keys()])
  render()
}}

function render(){{
  board.innerHTML=""
  board.style.gridTemplateColumns = `repeat(${grid},1fr)`

  // 🔥 PROPORZIONE REALE DELL’IMMAGINE
  const ratio = current.h / current.w

  const maxW = Math.min(window.innerWidth*0.8, 900)
  const width = maxW
  const height = width * ratio

  board.style.width = width + "px"
  board.style.height = height + "px"

  arr.forEach((p,i)=>{{
    const t = document.createElement("div")
    t.className="tile"

    const row = Math.floor(p/grid)
    const col = p % grid

    t.style.width = "100%"
    t.style.height = "100%"

    // 🔥 SCALING PERFETTO
    t.style.backgroundImage = `url(${current.url})`
    t.style.backgroundSize = `${grid*100}% ${grid*100}%`
    t.style.backgroundPosition = `${col/(grid-1)*100}% ${row/(grid-1)*100}%`

    t.onclick = ()=>swap(i)

    board.appendChild(t)
  }})
}}

function swap(i){{
  if(selected===null){{ selected=i; return }}

  [arr[selected], arr[i]] = [arr[i], arr[selected]]
  selected=null
  render()
}}

init()

</script>

</body>
</html>
"""

st.components.v1.html(html, height=900)
