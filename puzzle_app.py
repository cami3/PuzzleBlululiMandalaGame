import streamlit as st
from PIL import Image
import random
import time

st.set_page_config(layout="wide")

GRID = 4  # molto meglio 4x4

IMAGE_PATH = "images/web_purple.jpg"


# =====================
# LOAD
# =====================
def load():
    img = Image.open(IMAGE_PATH).resize((800, 800))
    return img

def split(img):
    size = 800 // GRID
    tiles = []

    for r in range(GRID):
        for c in range(GRID):
            tiles.append(img.crop((c*size, r*size, (c+1)*size, (r+1)*size)))

    return tiles


# =====================
# STATE
# =====================
if "board" not in st.session_state:
    st.session_state.board = list(range(GRID*GRID))
    random.shuffle(st.session_state.board)
    st.session_state.moves = 0
    st.session_state.start = None


# =====================
# MOVE LOGIC
# =====================
def get_neighbors(i):
    r, c = divmod(i, GRID)
    moves = []

    if r > 0: moves.append(i-GRID)
    if r < GRID-1: moves.append(i+GRID)
    if c > 0: moves.append(i-1)
    if c < GRID-1: moves.append(i+1)

    return moves


def move(i):
    empty = st.session_state.board.index(GRID*GRID-1)

    if i in get_neighbors(empty):
        st.session_state.board[empty], st.session_state.board[i] = (
            st.session_state.board[i],
            st.session_state.board[empty],
        )
        st.session_state.moves += 1

        if st.session_state.start is None:
            st.session_state.start = time.time()


# =====================
# UI
# =====================
img = load()
tiles = split(img)

st.title("🧩 Mandala Puzzle")

for r in range(GRID):
    cols = st.columns(GRID)

    for c in range(GRID):
        i = r*GRID + c
        tile_id = st.session_state.board[i]

        with cols[c]:
            if tile_id == GRID*GRID-1:
                st.empty()
            else:
                st.image(tiles[tile_id], use_container_width=True)
                if st.button("", key=i):
                    move(i)
                    st.rerun()


# =====================
# STATUS
# =====================
if st.session_state.start:
    t = int(time.time() - st.session_state.start)
else:
    t = 0

st.write(f"⏱ {t}s | 🔁 {st.session_state.moves} mosse")


# =====================
# COMPLETION
# =====================
if st.session_state.board == list(range(GRID*GRID)):
    st.success("🔥 Design sbloccato!")

    st.markdown("## 👉 Ottieni questo design")
    st.markdown("[Compra ora](https://blululi.com)")
