import base64
import io
import json
from pathlib import Path
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Mandala Puzzle Shop", layout="wide")

IMAGE_FOLDER = Path("images")

IMAGE_TITLES = {
    "01_web_rectangula_frame2": "Mandala Frame Pattern I",
    "02_web_IMG_2815": "Colorful Mandala on Pure Purple Background",
    "web_beige_green_plain_colors": "Beige & Green Mandala Balance",
    "web_blue_green_pink_plain_colors": "Blue Green Pink Mandala Harmony",
    "web_green_yellow_purple": "Green Yellow Purple Mandala Energy",
    "web_intricate_rectangular": "Intricate Mandala Geometry",
    "web_multicolor": "Multicolor Mandala Radiance",
    "web_orange_yellow": "Orange Yellow Mandala Sunrise",
    "web_purple": "Purple Mandala Serenity",
}

# 🔥 mapping diretto → fondamentale
IMAGE_TO_PRODUCT = {
    "01_web_rectangula_frame2": "https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
    "02_web_IMG_2815": "https://blululi.com/collections/wall-art/products/mandala-art-drawn-by-hand-vertical-framed-poster-mindfulness-yoga-purple-mandala",
    "web_beige_green_plain_colors": "https://blululi.com/collections/t-shirts/products/colorful-mandala-geometric-t-shirt",
    "web_blue_green_pink_plain_colors": "https://blululi.com/collections/t-shirts/products/vibrant-mandala-tee-intricate-art-design",
    "web_green_yellow_purple": "https://blululi.com/products/vibrant-mandala-tee-colorful-intricate-2",
    "web_intricate_rectangular": "https://blululi.com/collections/t-shirts/products/intricate-mandala-t-shirt-colorful-geometric-design",
    "web_multicolor": "https://blululi.com/products/rainbow-mandala-womens-short-sleeve-t-shirt-2",
    "web_orange_yellow": "https://blululi.com/products/one-shoulder-dress-with-hand-drawn-mandala-design-black-with-orange-red-and-gold-accents",
    "web_purple": "https://blululi.com/collections/kitchen-decor/products/mandala-art-15oz-ceramic-mug-perfect-for-coffee-tea-lovers-2",
}


def to_base64(path):
    with Image.open(path) as img:
        img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()


assets = []
for p in IMAGE_FOLDER.iterdir():
    if p.suffix.lower() in [".jpg", ".png", ".jpeg", ".webp"]:
        key = p.stem
        assets.append({
            "name": IMAGE_TITLES.get(key, key),
            "url": f"data:image/jpeg;base64,{to_base64(p)}",
            "product": IMAGE_TO_PRODUCT.get(key, "https://blululi.com")
        })

assets_json = json.dumps(assets)

# ================= HTML APP =================

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
  margin:0;
  font-family:Arial;
  background:#0f1226;
  color:white;
}}

.container {{
  max-width:1000px;
  margin:auto;
  padding:20px;
}}

h1 {{
  text-align:center;
}}

#board {{
  display:grid;
  gap:2px;
  margin-top:20px;
}}

.tile {{
  background-size:cover;
  cursor:pointer;
}}

button {{
  padding:10px;
  border:none;
  background:#6d28d9;
  color:white;
  border-radius:10px;
  cursor:pointer;
}}

.overlay {{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.8);
  display:none;
  justify-content:center;
  align-items:center;
}}

.box {{
  background:white;
  color:black;
  padding:20px;
  border-radius:20px;
  text-align:center;
}}
</style>
</head>

<body>

<div class="container">
<h1>🧩 Solve the Mandala → Unlock the Product</h1>

<select id="imageSelect"></select>
<button onclick="newGame()">Start</button>

<div id="board"></div>
</div>

<div id="overlay" class="overlay">
  <div class="box">
    <h2>✨ Completed</h2>
    <p id="resultText"></p>
    <a id="shopBtn" target="_blank">
      <button>🛍️ Shop This Design</button>
    </a>
    <br><br>
    <button onclick="closeOverlay()">Play Again</button>
  </div>
</div>

<script>

const images = {assets_json};

const board = document.getElementById("board");
const select = document.getElementById("imageSelect");
const overlay = document.getElementById("overlay");
const resultText = document.getElementById("resultText");
const shopBtn = document.getElementById("shopBtn");

let grid = 3;
let arr = [];
let moves = 0;
let current = 0;

// populate select
images.forEach((img,i)=>{{
  let opt=document.createElement("option");
  opt.value=i;
  opt.textContent=img.name;
  select.appendChild(opt);
}});

function shuffle(a){{
  for(let i=a.length-1;i>0;i--){{
    let j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }}
  return a;
}}

function newGame(){{
  current = select.value;
  arr = shuffle([...Array(grid*grid).keys()]);
  moves=0;
  render();
}}

function render(){{
  board.innerHTML="";
  board.style.gridTemplateColumns = `repeat(${{grid}},1fr)`;

  arr.forEach((val,i)=>{{
    let d=document.createElement("div");
    d.className="tile";

    let row=Math.floor(val/grid);
    let col=val%grid;

    d.style.backgroundImage=`url(${{images[current].url}})`;
    d.style.backgroundPosition=`${{-col*100}}% ${{-row*100}}%`;
    d.style.height="100px";

    d.onclick=()=>swap(i);
    board.appendChild(d);
  }});
}}

let selected=null;

function swap(i){{
  if(selected===null){{
    selected=i;
    return;
  }}
  [arr[selected],arr[i]]=[arr[i],arr[selected]];
  selected=null;
  moves++;
  render();
  check();
}}

function check(){{
  if(arr.every((v,i)=>v===i)){{
    overlay.style.display="flex";
    resultText.innerText=`Solved in ${{moves}} moves`;

    shopBtn.href = images[current].product + "?utm_source=puzzle";
  }}
}}

function closeOverlay(){{
  overlay.style.display="none";
}}

</script>

</body>
</html>
"""

st.components.v1.html(html, height=900, scrolling=True)
