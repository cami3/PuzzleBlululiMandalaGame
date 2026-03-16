import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Blululi Puzzle Studio", page_icon="🧩", layout="wide")

st.markdown("""
<style>
header, footer {visibility:hidden;}
[data-testid="stToolbar"],
[data-testid="stHeader"],
[data-testid="stStatusWidget"],
[data-testid="stDecoration"]{
display:none;
}

[data-testid="stAppViewContainer"],
.main .block-container{
padding:0 !important;
margin:0 !important;
max-width:100% !important;
}

iframe{
border:none !important;
}
</style>
""", unsafe_allow_html=True)

IMAGE_FOLDER = Path("images")

def encode_image(path):

    with Image.open(path) as src:

        img = src.convert("RGB")
        img.thumbnail((1600,1600))

        buffer = io.BytesIO()
        img.save(buffer,"JPEG",quality=90,optimize=True)

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return {
        "name": path.stem.replace("_"," ").replace("-"," ").title(),
        "url": f"data:image/jpeg;base64,{encoded}"
    }

images = sorted(
    p for p in IMAGE_FOLDER.iterdir()
    if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}
)

assets = [encode_image(p) for p in images]

products = [
"https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-art-1",
"https://blululi.com/collections/t-shirts/products/colorful-mandala-geometric-t-shirt",
"https://blululi.com/collections/t-shirts/products/vibrant-mandala-tee-intricate-art-design",
"https://blululi.com/products/vibrant-mandala-tee-colorful-intricate-2",
"https://blululi.com/products/spun-polyester-square-pillowcase-mandala-art-original-fine-art-hand-drawn-dark-charcoal-blue-1",
"https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-art",
"https://blululi.com/products/rainbow-mandala-womens-short-sleeve-t-shirt-2",
"https://blululi.com/collections/t-shirts/products/intricate-mandala-t-shirt-colorful-geometric-design",
"https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-intricate-1",
"https://blululi.com/products/one-shoulder-dress-with-hand-drawn-mandala-design-black-with-orange-red-and-gold-accents",
"https://blululi.com/collections/kitchen-decor/products/mandala-art-15oz-ceramic-mug-perfect-for-coffee-tea-lovers-2",
"https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
"https://blululi.com/products/colorful-mandala-tote-bag-boho-psychedelic-all-over-print"
]

html = Path("puzzle_app.html").read_text()

html = html.replace("__ASSETS__", json.dumps(assets))
html = html.replace("__PRODUCTS__", json.dumps(products))

st.components.v1.html(html, height=1300, scrolling=True)
