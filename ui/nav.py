"""Navbar dinamis (sticky) + transisi antarhalaman untuk OryzAI.

Satu navbar dipakai di semua halaman, termasuk Beranda. Menu yang aktif ditandai pil hijau
dengan animasi pop + cincin lilac, dan setiap pindah halaman memicu tirai/sapuan transisi
serta animasi masuk konten.
"""
from __future__ import annotations

import streamlit as st

HOME = "Beranda"
SCREEN = "Diagnosis"  # halaman skrining (nama internal)
ITEMS = [
    ("Beranda", HOME),
    ("Skrining", SCREEN),
    ("Kamus", "Kamus penyakit dan hama"),
    ("Aturan", "Kelola aturan"),
    ("Riwayat", "Riwayat konsultasi"),
]

CSS = """
<style>
/* ---------- buang elemen bawaan Streamlit yang bikin ruang kosong ---------- */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"], [data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 5.6rem !important; }
.stApp { overflow-x: hidden; }
/* blok <style> tidak boleh menyisakan celah kosong di atas navbar */
[data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] > style:only-child) { display: none !important; }
/* wadah overlay transisi tidak ikut memakan ruang */
[data-testid="stVerticalBlock"] > *:has(> [class*="st-key-ov_"]), [class*="st-key-ov_"] { position: absolute !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }

/* ---------- navbar menempel di atas, selebar layar penuh ---------- */
.st-key-topnav {
  position: fixed !important; top: 0; left: 0; right: 0; width: 100% !important; z-index: 1000; margin: 0 !important; padding: .65rem var(--padx); box-sizing: border-box;
  background: rgba(232, 220, 198, .9); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border-bottom: 1.5px solid var(--line); animation: navDrop .8s cubic-bezier(.2,.8,.2,1) both;
}
.st-key-topnav [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .25rem !important; align-items: center; }
.st-key-topnav [data-testid="stColumn"] { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }
.st-key-topnav [data-testid="stColumn"]:nth-child(2) { flex: 1 1 auto !important; }

.stApp .st-key-topnav [data-testid^="stBaseButton"] {
  background: transparent !important; border: 1.5px solid transparent !important; border-radius: 999px !important;
  padding: .35rem 1.05rem !important; min-height: 2.4rem; box-shadow: none !important;
  transition: background .25s, transform .25s cubic-bezier(.3,1.6,.5,1), border-color .25s, box-shadow .25s;
}
.stApp .st-key-topnav [data-testid^="stBaseButton"] p {
  font-size: .8rem !important; font-weight: 700 !important; letter-spacing: .1em; text-transform: uppercase; white-space: nowrap;
  color: var(--leaf) !important; transition: color .25s;
}
.stApp .st-key-topnav [data-testid^="stBaseButton"]:hover { background: var(--lav) !important; transform: translateY(-2px); }
.stApp .st-key-topnav [data-testid^="stBaseButton"]:active { transform: translateY(1px) scale(.97); }

/* menu aktif */
.stApp [class*="st-key-navon_"] [data-testid^="stBaseButton"] {
  background: var(--leaf) !important; border-color: var(--leaf) !important;
  animation: navPop .55s cubic-bezier(.3,1.6,.5,1) both, navRing .9s ease-out both;
}
.stApp [class*="st-key-navon_"] [data-testid^="stBaseButton"] p { color: var(--cream) !important; }
.stApp [class*="st-key-navon_"] [data-testid^="stBaseButton"]:hover { background: var(--moss) !important; }

/* logo */
.stApp .st-key-navlogo [data-testid^="stBaseButton"] { padding-left: .2rem !important; }
.stApp .st-key-navlogo [data-testid^="stBaseButton"] p { font-family: var(--display) !important; font-size: 1.35rem !important; letter-spacing: -.01em; text-transform: none; font-weight: 800 !important; display: flex; align-items: center; }
.stApp .st-key-navlogo [data-testid^="stBaseButton"] p::before {
  content: ""; width: 15px; height: 15px; margin-right: .6rem; background: var(--lav); border: 2px solid var(--leaf);
  border-radius: 50% 0 50% 50%; transform: rotate(45deg); transition: transform .6s cubic-bezier(.3,1.6,.5,1), background .3s;
}
.stApp .st-key-navlogo [data-testid^="stBaseButton"]:hover { background: transparent !important; }
.stApp .st-key-navlogo [data-testid^="stBaseButton"]:hover p::before { transform: rotate(225deg) scale(1.15); background: var(--leaf); }

/* tombol CTA & penghitung gejala di kanan */
.stApp .st-key-navcta [data-testid^="stBaseButton"] { background: var(--leaf) !important; border-color: var(--leaf) !important; box-shadow: 4px 4px 0 var(--lav) !important; }
.stApp .st-key-navcta [data-testid^="stBaseButton"] p { color: var(--cream) !important; }
.stApp .st-key-navcta [data-testid^="stBaseButton"]:hover { background: var(--lav-deep) !important; border-color: var(--lav-deep) !important; box-shadow: 6px 6px 0 var(--lav) !important; transform: translate(-2px, -2px); }
.nav-count { display: inline-flex; align-items: center; gap: .55rem; border: 1.5px dashed var(--leaf); border-radius: 999px; padding: .4rem 1rem; font-size: .78rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; white-space: nowrap; transition: all .3s; }
.nav-count::before { content: ""; width: 9px; height: 9px; border-radius: 50%; background: var(--muted); opacity: .5; }
.nav-count.on { background: var(--lav); border-style: solid; animation: navPop .5s cubic-bezier(.3,1.6,.5,1) both; }
.nav-count.on::before { background: var(--leaf); opacity: 1; animation: navPulse 1.6s ease-in-out infinite; }

@media (max-width: 900px) {
  .st-key-topnav [data-testid="stHorizontalBlock"] { overflow-x: auto; scrollbar-width: none; }
  .st-key-topnav [data-testid="stColumn"]:nth-child(2) { display: none !important; }
  .st-key-topnav [data-testid="stColumn"]:last-child { display: none !important; }
  .stApp .st-key-topnav [data-testid^="stBaseButton"] { padding: .3rem .7rem !important; }
  .stApp .st-key-topnav [data-testid^="stBaseButton"] p { font-size: .7rem !important; letter-spacing: .06em; }
}

/* ---------- animasi masuk konten setiap pindah halaman ---------- */
[class*="st-key-pg_"] { animation: pgIn .75s .2s cubic-bezier(.2,.8,.2,1) both; }

/* ---------- tirai (Beranda <-> fitur) dan sapuan (antar fitur) ---------- */
.curtain { position: fixed; inset: 0; z-index: 99999; pointer-events: none; display: grid; place-items: center; background: var(--leaf); animation: curtainUp 1.15s .35s cubic-bezier(.77,0,.18,1) forwards; }
.curtain::after { content: ""; position: absolute; left: 0; right: 0; bottom: -14px; height: 14px; background: var(--lav); }
.curtain b { font-family: var(--display); font-weight: 800; font-size: clamp(2.6rem, 9vw, 6rem); color: var(--cream); letter-spacing: -.04em; animation: curtainText .9s .05s ease both; }
.curtain b span { color: var(--lav); }
.sweep { position: fixed; inset: 0; z-index: 99999; pointer-events: none; background: var(--leaf); border-right: 14px solid var(--lav); animation: sweepOut .8s .12s cubic-bezier(.77,0,.18,1) forwards; }

@keyframes navDrop { from { opacity: 0; transform: translateY(-100%); } to { opacity: 1; transform: none; } }
@keyframes navPop { 0% { transform: scale(.82); } 100% { transform: scale(1); } }
@keyframes navRing { 0% { box-shadow: 0 0 0 0 rgba(203, 179, 232, .95); } 100% { box-shadow: 0 0 0 14px rgba(203, 179, 232, 0); } }
@keyframes navPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.5); } }
@keyframes pgIn { from { opacity: 0; transform: translateY(26px); } to { opacity: 1; transform: none; } }
@keyframes curtainUp { 0% { transform: translateY(0); } 100% { transform: translateY(-112%); visibility: hidden; } }
@keyframes curtainText { from { opacity: 0; transform: translateY(24px) scale(.94); } to { opacity: 1; transform: none; } }
@keyframes sweepOut { 0% { transform: translateX(0); } 100% { transform: translateX(104%); visibility: hidden; } }
@keyframes heroFloat { from { transform: translateY(0); } to { transform: translateY(-10px); } }

@media (prefers-reduced-motion: reduce) {
  .st-key-topnav, [class*="st-key-pg_"], .curtain, .curtain *, .sweep, [class*="st-key-navon_"] * { animation-duration: .01ms !important; animation-delay: 0s !important; }
}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def current() -> str:
    return st.session_state.setdefault("page", HOME)


def go(page: str) -> None:
    """Pindah halaman: dipakai sebagai callback tombol di mana pun."""
    prev = st.session_state.get("page", HOME)
    if page == prev:
        return
    st.session_state["page"] = page
    st.session_state["nav_n"] = st.session_state.get("nav_n", 0) + 1
    st.session_state["transition"] = "curtain" if HOME in (page, prev) else "sweep"


def page_key() -> str:
    return f"pg_{st.session_state.get('nav_n', 0)}"


def navbar() -> None:
    page = current()
    n = len(st.session_state.get("facts", {}))
    with st.container(key="topnav"):
        cols = st.columns([1.2, 3, 1, 1, 1, 1, 1, 1.6], vertical_alignment="center")
        with cols[0].container(key="navlogo"):
            st.button("OryzAI", key="navlogo_btn", on_click=go, args=(HOME,))
        for i, (col, (label, target)) in enumerate(zip(cols[2:7], ITEMS)):
            prefix = "navon_" if target == page else "nav_"
            with col.container(key=f"{prefix}{i}"):
                st.button(label, key=f"navbtn_{i}", on_click=go, args=(target,))
        with cols[7]:
            if page == SCREEN:
                text = f"{n} gejala dipilih" if n else "Belum ada gejala"
                st.markdown(f'<span class="nav-count{" on" if n else ""}">{text}</span>', unsafe_allow_html=True)
            else:
                with st.container(key="navcta"):
                    st.button("Mulai skrining", key="navcta_btn", on_click=go, args=(SCREEN,))


def overlay() -> None:
    """Tirai/sapuan yang menutupi pergantian halaman, lalu terangkat."""
    kind = st.session_state.pop("transition", None)
    n = st.session_state.get("nav_n", 0)
    if kind == "curtain":
        with st.container(key=f"ov_{n}"):
            st.markdown('<div class="curtain"><b>Oryz<span>AI</span></b></div>', unsafe_allow_html=True)
    elif kind == "sweep":
        with st.container(key=f"ov_{n}"):
            st.markdown('<div class="sweep"></div>', unsafe_allow_html=True)
