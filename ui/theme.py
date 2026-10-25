"""Tema visual dan potongan HTML kecil untuk antarmuka sistem pakar padi.

Palet tetap mengikuti README: krem #E8DCC6, hijau tua #1F3B2E, lavender #CBB3E8.
"""
from __future__ import annotations

from html import escape

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,800&family=Fraunces:ital,opsz,wght@1,9..144,400&family=Public+Sans:wght@400;500;600;700&display=swap');

:root {
  --padx: clamp(1.2rem, 4vw, 4.5rem);
  --cream: #E8DCC6;
  --paper: #F7F2E9;
  --leaf: #1F3B2E;
  --moss: #355744;
  --lav: #CBB3E8;
  --lav-soft: #EADFF5;
  --lav-deep: #4A2C80;
  --muted: #2F4A3B;
  --line: rgba(31, 59, 46, .16);
  --note-bg: #F1E2B5;
  --note-ink: #4F3800;
  --display: 'Bricolage Grotesque', 'Trebuchet MS', system-ui, sans-serif;
  --body: 'Public Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

/* ---------- Dasar ---------- */
.stApp { background: var(--cream); color: var(--leaf); }
.stApp :is(p, span, label, div, li, td, th, input, textarea, button, summary):not([data-testid="stIconMaterial"]) {
  font-family: var(--body);
}
.stApp :is(h1, h2, h3, h4) { font-family: var(--display); color: var(--leaf); letter-spacing: -.015em; }
.stApp h1 { font-weight: 800; }
.stApp :is(h2, h3, h4) { font-weight: 600; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 100% !important; padding: 2.2rem var(--padx) 4rem !important; }
[data-testid="stHeaderActionElements"], .stApp :is(h1,h2,h3,h4,h5,h6) a[href^="#"] { display: none !important; }
.stApp p, .stApp li { line-height: 1.6; }
.stApp a { color: var(--lav-deep) !important; text-underline-offset: 3px; }
.stApp :focus-visible { outline: 3px solid var(--lav-deep) !important; outline-offset: 2px; }
.stApp hr { border-color: var(--line); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--leaf); }
[data-testid="stSidebar"] * { color: var(--cream); }
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] { padding-bottom: 0; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { display: none; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] { gap: .3rem; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div { width: 100%; }
[data-testid="stSidebar"] label[data-testid="stRadioOption"] {
  width: 100%; padding: .65rem .85rem; border-radius: 12px; margin: 0;
  border: 1px solid transparent; background: transparent; cursor: pointer;
}
[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child { display: none; }
[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover { background: rgba(232, 220, 198, .1); }
[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] { background: var(--lav); }
[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] * { color: var(--leaf); font-weight: 700; }
[data-testid="stSidebar"] label[data-testid="stRadioOption"] p { font-size: .98rem; }
.side-brand { display: flex; gap: .7rem; align-items: center; padding: .4rem .2rem 1rem; }
.side-brand b { font-family: var(--display); font-size: 1.08rem; line-height: 1.15; display: block; color: var(--cream); }
.side-brand small { color: var(--lav); font-size: .76rem; line-height: 1.25; display: block; margin-top: .15rem; }
.side-note { background: rgba(232, 220, 198, .09); border-radius: 12px; padding: .8rem .9rem; font-size: .84rem; line-height: 1.5; margin-top: 1rem; }

/* ---------- Hero ---------- */
.hero { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; background: var(--leaf); border-radius: 26px 26px 26px 6px; padding: 2rem 2.2rem; margin-bottom: 1.2rem; }
.hero::before { content: ""; position: absolute; width: 260px; height: 260px; border-radius: 50%; background: var(--lav); opacity: .16; right: -70px; top: -90px; }
.hero-text { position: relative; z-index: 1; flex: 1 1 auto; max-width: 560px; }
.eyebrow { display: inline-block; background: var(--lav); color: var(--leaf); border-radius: 999px; padding: .15rem .8rem; font-size: .72rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .8rem; }
.hero h1 { color: var(--cream) !important; font-size: clamp(1.9rem, 3.4vw, 2.7rem); line-height: 1.1; margin: 0 0 .8rem; padding: 0; }
.hero h1 em, .page-head h1 em { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-weight: 400; color: var(--lav); }
.page-head h1 em { color: var(--lav-deep); }
.hero p { color: var(--cream) !important; opacity: .92; font-size: 1.02rem; margin: 0 0 .6rem; }
.hero .hero-warn { font-size: .88rem; color: var(--lav) !important; opacity: 1; margin: 0; }
.hero svg { position: relative; z-index: 1; flex: 0 0 auto; height: 220px; width: auto; max-width: 38%; pointer-events: none; }
@media (max-width: 760px) { .hero svg { display: none; } .hero { padding: 1.5rem 1.3rem; } }

.page-head { margin-bottom: 1.1rem; }
.page-head .eyebrow { margin-bottom: .5rem; }
.page-head h1 { font-size: clamp(1.6rem, 2.6vw, 2.1rem); margin: 0 0 .3rem; padding: 0; }
.page-head p { color: var(--muted); margin: 0; max-width: 62ch; }

/* ---------- Stepper ---------- */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem; margin-bottom: 1.3rem; }
.step { display: flex; gap: .7rem; align-items: flex-start; padding: .8rem .95rem; border-radius: 16px; background: rgba(247, 242, 233, .55); border: 1px solid var(--line); }
.step .n { flex: none; width: 1.9rem; height: 1.9rem; border-radius: 50%; display: grid; place-items: center; font-weight: 700; font-size: .92rem; background: var(--cream); border: 1.5px solid var(--leaf); }
.step b { display: block; font-size: .98rem; line-height: 1.25; }
.step span.d { font-size: .84rem; color: var(--muted); line-height: 1.4; display: block; margin-top: .15rem; }
.step.active { background: var(--paper); border-color: var(--leaf); box-shadow: 0 0 0 2px var(--lav); }
.step.active .n { background: var(--leaf); color: var(--cream); }
.step.done .n { background: var(--lav); border-color: var(--lav); }
.step.done { opacity: .8; }
@media (max-width: 760px) { .steps { grid-template-columns: 1fr; } }

/* ---------- Legenda tingkat keyakinan ---------- */
.legend { background: var(--lav-soft); border-radius: 16px; padding: .85rem 1.1rem; margin: .2rem 0 1rem; }
.legend > b { display: block; margin-bottom: .45rem; }
.stApp .legend ul { list-style: none; margin: 0 !important; padding: 0 !important; display: grid; grid-template-columns: repeat(2, 1fr); gap: .3rem 1.2rem; }
.stApp .legend li { font-size: .9rem; line-height: 1.4; margin: 0; padding: 0; }
.legend li em { font-style: normal; font-weight: 700; }
@media (max-width: 760px) { .legend ul { grid-template-columns: 1fr; } }

/* ---------- Bagian kategori gejala ---------- */
.cat-head { display: flex; align-items: center; flex-wrap: wrap; gap: .3rem .6rem; margin: 1.6rem 0 .55rem; }
.stApp .cat-head h3 { margin: 0; padding: 0; font-size: 1.25rem; }
.cat-head small { color: var(--muted); font-size: .86rem; margin-left: auto; }
.cat-head .cnt { background: var(--leaf); color: var(--cream); border-radius: 999px; padding: .05rem .65rem; font-size: .8rem; font-weight: 700; }

/* ---------- Baris gejala ---------- */
[class*="st-key-on_row_"], [class*="st-key-off_row_"] {
  border: 1px solid var(--line); border-radius: 14px; padding: .85rem 1rem 1.05rem; margin-bottom: .1rem; background: var(--paper);
}
[class*="st-key-on_row_"] { background: var(--lav-soft); border-color: var(--lav-deep); }
.sym-label { font-weight: 600; line-height: 1.35; }
.sym-why { color: var(--muted); font-size: .84rem; line-height: 1.4; margin-top: .15rem; }

/* Semua radio di area utama tampil sebagai tombol pil */
.stApp [data-testid="stMain"] [data-testid="stRadioGroup"] { gap: .4rem; flex-wrap: wrap; }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"] {
  margin: 0; padding: .34rem .85rem; border-radius: 999px; background: var(--paper);
  border: 1.5px solid rgba(31, 59, 46, .22); cursor: pointer; transition: background .12s, border-color .12s;
}
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"] > div > div:first-child { display: none; }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"]:hover { border-color: var(--moss); }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"] p { font-size: .9rem; font-weight: 500; white-space: nowrap; }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"][data-selected="true"] { background: var(--leaf); border-color: var(--leaf); }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"][data-selected="true"] p { color: var(--cream); font-weight: 700; }

/* Khusus baris gejala: empat pilihan tersusun 2 x 2 */
[class*="st-key-on_row_"] [data-testid="stRadioGroup"], [class*="st-key-off_row_"] [data-testid="stRadioGroup"] { display: grid; grid-template-columns: 1fr 1fr; }
[class*="st-key-on_row_"] [data-testid="stRadioGroup"] > div, [class*="st-key-off_row_"] [data-testid="stRadioGroup"] > div { width: 100%; }
[class*="st-key-on_row_"] label[data-testid="stRadioOption"], [class*="st-key-off_row_"] label[data-testid="stRadioOption"] {
  width: 100%; justify-content: center; padding: .34rem .6rem; background: var(--cream); border-color: transparent;
}
[class*="st-key-on_row_"] label[data-testid="stRadioOption"]:hover, [class*="st-key-off_row_"] label[data-testid="stRadioOption"]:hover { border-color: var(--moss); }
[class*="st-key-on_row_"] label[data-testid="stRadioOption"][data-selected="true"], [class*="st-key-off_row_"] label[data-testid="stRadioOption"][data-selected="true"] { background: var(--leaf); border-color: var(--leaf); }
[class*="st-key-on_row_"] [data-testid="stRadioGroup"] > div:first-child label[data-selected="true"],
[class*="st-key-off_row_"] [data-testid="stRadioGroup"] > div:first-child label[data-selected="true"] { background: transparent; border-color: var(--muted); }
[class*="st-key-on_row_"] [data-testid="stRadioGroup"] > div:first-child label[data-selected="true"] p,
[class*="st-key-off_row_"] [data-testid="stRadioGroup"] > div:first-child label[data-selected="true"] p { color: var(--muted); }

/* ---------- Panel ringkasan ---------- */
[data-testid="stColumn"]:has(.st-key-summary_panel) { position: sticky; top: 4.2rem; align-self: flex-start; }
.st-key-summary_panel { background: var(--paper); border: 1px solid var(--line); border-radius: 22px 22px 22px 6px; padding: 1.1rem 1.2rem 1.2rem; }
.st-key-summary_panel h3 { margin: 0 0 .2rem; font-size: 1.2rem; }
.sum-count { font-size: .9rem; color: var(--muted); margin-bottom: .7rem; }
.sum-empty { background: var(--cream); border-radius: 12px; padding: .8rem .9rem; font-size: .9rem; margin-bottom: .8rem; }
.stApp .sum-list { list-style: none; margin: 0 0 .9rem !important; padding: 0 !important; max-height: 300px; overflow-y: auto; }
.stApp .sum-list li { display: flex; flex-direction: column; align-items: flex-start; gap: .25rem; padding: .5rem 0; margin: 0; border-bottom: 1px solid var(--line); font-size: .87rem; line-height: 1.35; }
.sum-list li i { font-style: normal; font-weight: 700; font-size: .76rem; background: var(--lav); border-radius: 999px; padding: .05rem .6rem; }

/* ---------- Kartu hasil ---------- */
.result-main { background: var(--leaf); color: var(--cream); border-radius: 26px 26px 26px 6px; padding: 1.5rem 1.7rem; margin: .4rem 0 1rem; }
.result-main * { color: var(--cream); }
.result-main .tag { display: inline-block; background: var(--lav); color: var(--leaf) !important; border-radius: 999px; padding: .12rem .7rem; font-size: .8rem; font-weight: 700; margin-bottom: .6rem; }
.result-main h2 { color: var(--cream) !important; font-size: clamp(1.6rem, 3vw, 2.2rem); margin: 0 0 .4rem; padding: 0; line-height: 1.1; }
.result-main .sci { font-style: italic; opacity: .8; font-size: .9rem; margin: 0 0 .9rem; }
.result-main .score-row { display: flex; align-items: baseline; gap: .8rem; flex-wrap: wrap; margin-bottom: .4rem; }
.result-main .score-row b { font-family: var(--display); font-size: 2.4rem; line-height: 1; }
.result-main .score-row span { font-weight: 600; }
.result-main .meter { background: rgba(232, 220, 198, .22); }
.result-main .meter-fill { background: var(--lav); }
.result-main p.sum { margin: 1rem 0 0; font-size: 1.02rem; max-width: 70ch; }

.meter { height: 12px; border-radius: 999px; background: rgba(31, 59, 46, .14); overflow: hidden; }
.meter-fill { height: 100%; border-radius: 999px; background: var(--leaf); }

.chips { display: flex; flex-wrap: wrap; gap: .4rem; margin: .3rem 0 .2rem; }
.chip { background: var(--lav-soft); color: var(--leaf); border: 1px solid rgba(94, 63, 147, .35); border-radius: 999px; padding: .2rem .7rem; font-size: .84rem; line-height: 1.35; }
.result-main .chip { background: rgba(232, 220, 198, .14); border-color: rgba(232, 220, 198, .35); color: var(--cream); }

.box { background: var(--paper); border: 1px solid var(--line); border-radius: 18px; padding: 1.1rem 1.3rem; margin-bottom: .9rem; }
.stApp .box h4 { margin: 0 0 .5rem; padding: 0; font-size: 1.05rem; }
.box ul, .box ol { margin: 0; padding-left: 1.2rem; }
.box li { margin-bottom: .3rem; }
.note { background: var(--note-bg); color: var(--note-ink); border-radius: 14px; padding: .75rem 1rem; font-size: .9rem; line-height: 1.5; margin: .6rem 0 1rem; }
.note * { color: var(--note-ink); }
.why-line { padding: .55rem 0; border-bottom: 1px solid var(--line); line-height: 1.5; }
.why-line:last-child { border-bottom: 0; }
.why-line small { display: block; color: var(--muted); }

.other { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.other b { font-family: var(--display); font-size: 1.1rem; }

/* ---------- Kartu pengetahuan ---------- */
.dz { margin-bottom: .45rem; background: var(--paper); border: 1px solid var(--line); border-radius: 20px 20px 20px 6px; padding: 1.1rem 1.2rem .7rem; }
.stApp .dz h4 { margin: .2rem 0 .1rem; padding: 0; font-size: 1.15rem; }
.dz .sci { color: var(--muted); font-style: italic; font-size: .84rem; margin: 0 0 .5rem; }
.dz .badge { display: inline-block; border-radius: 999px; padding: .08rem .65rem; font-size: .76rem; font-weight: 700; }
.badge.penyakit { background: var(--lav); }
.badge.hama { background: var(--leaf); color: var(--cream); }
.dz p.sum { font-size: .93rem; margin: .2rem 0 .6rem; }
.dz .lbl { font-size: .82rem; font-weight: 700; color: var(--muted); margin-top: .5rem; }

.rule-sentence { background: var(--paper); border-left: 5px solid var(--lav-deep); border-radius: 4px 14px 14px 4px; padding: .8rem 1rem; margin: .4rem 0 1rem; line-height: 1.6; }
.rule-sentence b { color: var(--lav-deep); }

.stat { background: var(--paper); border: 1px solid var(--line); border-radius: 16px; padding: .9rem 1.1rem; min-height: 6.2rem; }
.stat small { color: var(--muted); font-size: .86rem; display: block; }
.stat b { font-family: var(--display); font-size: 1.3rem; line-height: 1.2; display: block; margin-top: .2rem; }

.lvl { display: inline-block; border-radius: 999px; padding: .1rem .8rem; font-size: .85rem; font-weight: 700; }
.lvl.kritis { background: #B3261E; color: #fff; }
.lvl.gawat { background: #D9650B; color: #fff; }
.lvl.waspada { background: #F1D27A; color: #4F3800; }
.lvl.ringan { background: var(--lav); color: var(--leaf); }
.lvl-advice { margin: .5rem 0 0; font-size: .95rem; }

/* ---------- Komponen Streamlit ---------- */
.stApp [data-testid="stCaptionContainer"] { color: var(--muted); }
[data-testid="stMetric"] { background: var(--paper); border: 1px solid var(--line); border-radius: 16px; padding: 1rem 1.1rem; }
[data-testid="stExpander"] { background: var(--paper); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
[data-testid="stExpander"] summary { background: transparent; }
[data-testid="stExpander"] summary:hover { background: var(--lav-soft); }
[data-testid="stExpander"] summary p { font-weight: 600; }
[data-testid="stForm"] { background: var(--paper); border: 1px solid var(--line); border-radius: 18px; padding: 1.1rem 1.2rem; }
[data-testid="stTabs"] [role="tab"] { font-weight: 600; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: var(--leaf); }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--leaf); }
[data-testid="stAlert"] { border-radius: 14px; }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }

[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stNumberInput"] input,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
  background: #FFFCF6; border-color: rgba(31, 59, 46, .35); border-radius: 12px; color: var(--leaf);
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] { background: var(--lav); color: var(--leaf); border-radius: 8px; }
[data-testid="stSelectbox"] input { caret-color: transparent; }

[data-testid^="stBaseButton-primary"] {
  background: var(--leaf); color: var(--cream); border: 1px solid var(--leaf); border-radius: 14px; font-weight: 700; min-height: 2.9rem;
}
[data-testid^="stBaseButton-primary"] * { color: var(--cream); }
[data-testid^="stBaseButton-primary"]:hover { background: var(--lav); border-color: var(--lav); }
[data-testid^="stBaseButton-primary"]:hover * { color: var(--leaf); }
[data-testid^="stBaseButton-primary"]:disabled { background: rgba(31, 59, 46, .25); border-color: transparent; }
[data-testid^="stBaseButton-secondary"] {
  background: transparent; color: var(--leaf); border: 1.5px solid var(--leaf); border-radius: 14px; font-weight: 600;
}
[data-testid^="stBaseButton-secondary"] * { color: var(--leaf); }
[data-testid^="stBaseButton-secondary"]:hover { background: var(--lav-soft); border-color: var(--lav-deep); }
[data-testid="stDownloadButton"] button { border-radius: 14px; font-weight: 600; }

/* ---------- Ponsel: panel ringkasan menjadi bilah bawah ---------- */
@media (max-width: 760px) {
  .block-container { padding-bottom: 9rem !important; }
  [data-testid="stColumn"]:has(.st-key-summary_panel) { position: static; }
  .st-key-summary_panel {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 999; border-radius: 20px 20px 0 0;
    padding: .7rem 1rem .9rem; box-shadow: 0 -6px 24px rgba(31, 59, 46, .25); border-width: 1px 0 0 0;
  }
  .st-key-summary_panel h3, .st-key-summary_panel .sum-list, .st-key-summary_panel .sum-empty,
  .st-key-summary_panel [data-testid="stCaptionContainer"], .st-key-summary_panel [data-testid="stBaseButton-secondary"] { display: none; }
  .sum-count { margin-bottom: .5rem; font-weight: 600; }
}

/* ---------- Interaksi dinamis ---------- */
.app-foot { margin-top: 3rem; padding-top: 1rem; border-top: 1.5px solid var(--line); font-size: .85rem; color: var(--muted); text-align: center; }
.dz, .box, .stat, .step, .legend, .note, .rule-sentence { transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s, border-color .3s, background .3s; }
.dz:hover, .box:hover, .stat:hover { transform: translateY(-5px); box-shadow: 6px 6px 0 var(--lav); border-color: var(--leaf); }
.step:hover { transform: translateY(-3px); border-color: var(--leaf); }
.rule-sentence:hover { transform: translateX(6px); }
[class*="st-key-off_row_"], [class*="st-key-on_row_"] { transition: transform .25s cubic-bezier(.2,.8,.2,1), border-color .25s, background .25s, box-shadow .25s; }
[class*="st-key-off_row_"]:hover { transform: translateX(5px); border-color: var(--leaf); box-shadow: -5px 0 0 var(--lav); }
[class*="st-key-on_row_"] { box-shadow: -5px 0 0 var(--lav-deep); }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"] { transition: transform .2s cubic-bezier(.3,1.6,.5,1), background .2s, border-color .2s; }
.stApp [data-testid="stMain"] label[data-testid="stRadioOption"]:hover { transform: translateY(-2px); }
.stApp [data-testid="stMain"] [data-testid^="stBaseButton"]:not(:disabled) { transition: transform .25s cubic-bezier(.3,1.6,.5,1), background .25s, box-shadow .25s; }
.stApp [data-testid="stMain"] [data-testid^="stBaseButton-primary"]:not(:disabled):hover { transform: translateY(-2px); box-shadow: 4px 4px 0 var(--lav); }
.result-main { animation: pgIn .8s .1s cubic-bezier(.2,.8,.2,1) both; }
.meter-fill { animation: meterGrow 1.2s .3s cubic-bezier(.2,.8,.2,1) both; transform-origin: left; }
.hero svg { animation: heroFloat 6s ease-in-out infinite alternate; }
.cat-head h3 { position: relative; padding-bottom: .25rem; }
.cat-head h3::after { content: ""; position: absolute; left: 0; bottom: 0; height: 3px; width: 100%; background: var(--lav); border-radius: 3px; transform-origin: left; animation: meterGrow .8s cubic-bezier(.2,.8,.2,1) both; }
@keyframes meterGrow { from { transform: scaleX(0); } to { transform: scaleX(1); } }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def _stalk_svg() -> str:
    """Ilustrasi tangkai padi sederhana untuk hero (garis krem, bulir lavender)."""
    parts = [
        '<svg viewBox="0 0 260 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">',
        '<path d="M60 240 C 70 170, 120 110, 190 52" fill="none" stroke="#E8DCC6" stroke-width="3.5" stroke-linecap="round"/>',
        '<path d="M80 205 C 40 190, 20 165, 12 140 C 50 150, 70 170, 80 205Z" fill="#355744"/>',
        '<path d="M98 172 C 150 170, 185 190, 215 222 C 165 222, 120 205, 98 172Z" fill="#355744"/>',
    ]
    # bulir menggantung di sepanjang ujung lengkung tangkai
    for i in range(12):
        t = 0.38 + i * 0.052
        # titik pada kurva bezier kubik
        p0, p1, p2, p3 = (60, 240), (70, 170), (120, 110), (190, 52)
        x = ((1 - t) ** 3) * p0[0] + 3 * ((1 - t) ** 2) * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0]
        y = ((1 - t) ** 3) * p0[1] + 3 * ((1 - t) ** 2) * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1]
        for side in (-1, 1):
            ang = 28 * side + 12
            parts.append(
                f'<ellipse cx="{x + side * 9:.1f}" cy="{y + 12:.1f}" rx="4.6" ry="11" '
                f'transform="rotate({ang} {x + side * 9:.1f} {y + 12:.1f})" fill="#CBB3E8"/>'
            )
    parts.append("</svg>")
    return "".join(parts)


def hero() -> str:
    return (
        '<div class="hero">'
        '<div class="hero-text">'
        '<span class="eyebrow">OryzAI · Diagnosis</span>'
        "<h1>Periksa padi Anda <em>dari gejala yang terlihat</em></h1>"
        "<p>Pilih ciri-ciri yang Anda temukan di daun, pelepah, batang, atau malai. "
        "Sistem membandingkannya dengan aturan para ahli, lalu menyarankan penyakit atau hama "
        "yang paling mungkin beserta langkah awal penanganannya.</p>"
        '<p class="hero-warn">Hasilnya dugaan awal. Untuk keputusan pengendalian, tanyakan ke penyuluh pertanian setempat.</p>'
        "</div>" + _stalk_svg() + "</div>"
    )


def page_head(title: str, sub: str) -> str:
    return f'<div class="page-head"><span class="eyebrow">OryzAI</span><h1>{escape(title)}</h1><p>{escape(sub)}</p></div>'


def stepper(active: int) -> str:
    """active: 0 = pilih gejala, 1 = siap dianalisis, 2 = baca hasil."""
    steps = [
        ("Pilih gejala", "Tandai yang Anda lihat pada tanaman"),
        ("Analisis", "Sistem mencocokkan dengan aturan pakar"),
        ("Baca hasil", "Dugaan, langkah awal, dan alasannya"),
    ]
    out = ['<div class="steps">']
    for i, (title, desc) in enumerate(steps):
        state = "done" if i < active else ("active" if i == active else "todo")
        mark = "&#10003;" if state == "done" else str(i + 1)
        out.append(
            f'<div class="step {state}"><div class="n">{mark}</div>'
            f'<div><b>{escape(title)}</b><span class="d">{escape(desc)}</span></div></div>'
        )
    out.append("</div>")
    return "".join(out)


def stat(label: str, value) -> str:
    return f'<div class="stat"><small>{escape(str(label))}</small><b>{escape(str(value))}</b></div>'


def chips(items) -> str:
    return '<div class="chips">' + "".join(f'<span class="chip">{escape(str(i))}</span>' for i in items) + "</div>"


def meter(pct: float) -> str:
    pct = max(0.0, min(100.0, pct))
    return (
        f'<div class="meter" role="img" aria-label="Skor dukungan {pct:.0f} persen">'
        f'<div class="meter-fill" style="width:{pct:.1f}%"></div></div>'
    )


# Tingkat triase berdasarkan skor dukungan (Certainty Factor), berlaku sama untuk semua kandidat.
LEVELS = [
    (85.0, "kritis", "Kritis", "Sangat kuat. Segera hubungi penyuluh atau petugas perlindungan tanaman."),
    (70.0, "gawat", "Gawat", "Kuat. Tindak lanjuti dalam 1 sampai 2 hari dan konfirmasikan ke penyuluh."),
    (45.0, "waspada", "Waspada", "Sedang. Pantau tanaman dan periksa gejala tambahan."),
    (0.0, "ringan", "Dugaan awal", "Lemah. Amati lagi dan lengkapi gejala yang terlihat."),
]


def level(pct: float) -> dict:
    for floor, key, name, advice in LEVELS:
        if pct >= floor:
            return {"key": key, "name": name, "advice": advice}
    return {"key": "ringan", "name": LEVELS[-1][2], "advice": LEVELS[-1][3]}


def strength(pct: float) -> str:
    return level(pct)["name"]


def level_badge(pct: float) -> str:
    lv = level(pct)
    return f'<span class="lvl {lv["key"]}">{escape(lv["name"])}</span>'


def brand() -> str:
    mark = (
        '<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true">'
        '<rect width="40" height="40" rx="12" fill="#CBB3E8"/>'
        '<path d="M12 33 C 14 22, 21 14, 29 8" fill="none" stroke="#1F3B2E" stroke-width="2.6" stroke-linecap="round"/>'
        '<ellipse cx="22" cy="21" rx="2.6" ry="5.2" transform="rotate(35 22 21)" fill="#1F3B2E"/>'
        '<ellipse cx="27" cy="16" rx="2.4" ry="5" transform="rotate(35 27 16)" fill="#1F3B2E"/>'
        '<ellipse cx="17" cy="26" rx="2.4" ry="5" transform="rotate(35 17 26)" fill="#1F3B2E"/>'
        "</svg>"
    )
    return f'<div class="side-brand">{mark}<div><b>OryzAI</b><small>Sistem pakar diagnosis padi</small></div></div>'


__all__ = ["inject_css", "hero", "page_head", "stepper", "chips", "stat", "meter", "strength", "level", "level_badge", "brand"]
