import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Puzzle Studio", layout="wide")

IMAGE_FOLDER = Path("images")

if not IMAGE_FOLDER.exists():
    st.error("Missing ./images folder")
    st.stop()

image_paths = [p for p in IMAGE_FOLDER.iterdir() if p.suffix.lower() in [".jpg", ".png", ".jpeg", ".webp"]]

def encode_image(path):
    with Image.open(path) as img:
        img = img.convert("RGB")

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        encoded = base64.b64encode(buf.getvalue()).decode()

    return {
        "name": path.stem,
        "url": f"data:image/jpeg;base64,{encoded}"
    }

assets = [encode_image(p) for p in image_paths]

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>

body {{
  margin:0;
  font-family: sans-serif;
  background: #f5f5f5;
}}

.container {{
  display:flex;
  gap:20px;
  padding:20px;
}}

.sidebar {{
  width:260px;
}}

.board-container {{
  flex:1;
  display:flex;
  justify-content:center;
  align-items:center;
}}

#board {{
  display:grid;
  gap:2px;
  background:white;
  padding:4px;
  border-radius:12px;

  /* 🔥 FIX: non più quadrato forzato */
  width: min(90vw, 900px);
  height: auto;
  aspect-ratio: auto;
}}

.tile {{
  background-repeat:no-repeat;
  background-size: contain; /* 🔥 FIX PRINCIPALE */
  background-position:center;
  cursor:pointer;
  border-radius:4px;
}}

img.preview {{
  width:100%;
  border-radius:12px;
}}

button {{
  width:100%;
  padding:10px;
  margin-top:10px;
  border:none;
  border-radius:8px;
  cursor:pointer;
}}

.primary {{
  background:#6d28d9;
  color:white;
}}

</style>
</head>

<body>

<div class="container">

<div class="sidebar">
  <h3>Choose Image</h3>
  <select id="imageSelect"></select>

  <h3>Difficulty</h3>
  <input type="range" min="2" max="8" value="4" id="difficulty">

  <button class="primary" onclick="newGame()">Shuffle</button>

  <img id="preview" class="preview">
</div>

<div class="board-container">
  <div id="board"></div>
</div>

</div>

<script>

const images = {json.dumps(assets)}

const board = document.getElementById("board")
const select = document.getElementById("imageSelect")
const difficulty = document.getElementById("difficulty")
const preview = document.getElementById("preview")

let grid = 4
let arrangement = []
let currentImage = ""

function init() {{
  images.forEach((img, i) => {{
    const opt = document.createElement("option")
    opt.value = i
    opt.textContent = img.name
    select.appendChild(opt)
  }})

  select.value = 0
  updateImage()
  newGame()
}}

function updateImage() {{
  const img = images[select.value]
  currentImage = img.url
  preview.src = currentImage
}}

select.addEventListener("change", () => {{
  updateImage()
  newGame()
}})

difficulty.addEventListener("change", () => {{
  grid = Number(difficulty.value)
  newGame()
}})

function makeArrangement() {{
  let arr = Array.from({{length:grid*grid}}, (_,i)=>i)
  return arr.sort(()=>Math.random()-0.5)
}}

function render() {{
  board.innerHTML = ""
  board.style.gridTemplateColumns = `repeat(${grid},1fr)`

  arrangement.forEach((piece, i) => {{
    const tile = document.createElement("div")
    tile.className = "tile"

    tile.style.backgroundImage = `url(${currentImage})`

    const row = Math.floor(piece / grid)
    const col = piece % grid

    tile.style.backgroundSize = `${grid*100}% ${grid*100}%`
    tile.style.backgroundPosition = `${col/(grid-1)*100}% ${row/(grid-1)*100}%`

    tile.onclick = () => swap(i)

    board.appendChild(tile)
  }})
}}

let selected = null

function swap(i) {{
  if(selected === null){{
    selected = i
    return
  }}

  [arrangement[selected], arrangement[i]] = [arrangement[i], arrangement[selected]]
  selected = null
  render()
}}

function newGame() {{
  arrangement = makeArrangement()
  render()
}}

init()

</script>

</body>
</html>
"""

st.components.v1.html(html, height=900, scrolling=True)
