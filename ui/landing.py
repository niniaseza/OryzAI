"""Landing page OryzAI: hero animasi, marquee, kartu fitur, dan tirai transisi masuk.

Palet: Oatmeal #E8DCC6, Pine Green #1F3B2E, Soft Lilac #CBB3E8.
Semua animasi murni CSS (tanpa JavaScript) dan menghormati prefers-reduced-motion.
"""
from __future__ import annotations

import streamlit as st

from ui import nav

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Fraunces:ital,opsz,wght@1,9..144,400&display=swap');

.lp { position: relative; color: var(--leaf); }
.lp * { box-sizing: border-box; }


/* ---------- hero ---------- */
.lp-title {
  position: relative; z-index: 1; margin: .6rem 0 0; padding: 0;
  font-family: var(--display) !important; font-weight: 800; color: var(--leaf);
  font-size: clamp(4.4rem, 24.5vw, 30rem); line-height: .86; letter-spacing: -.055em;
  display: flex; flex-wrap: nowrap; user-select: none; overflow: visible;
}
.lp-title span { display: inline-block; opacity: 0; transform: translateY(70%) rotate(4deg); animation: lpLetter 1s cubic-bezier(.2,.9,.2,1) forwards; }
.lp-title span:nth-child(1) { animation-delay: .15s; } .lp-title span:nth-child(2) { animation-delay: .25s; }
.lp-title span:nth-child(3) { animation-delay: .35s; } .lp-title span:nth-child(4) { animation-delay: .45s; }
.lp-title span:nth-child(5) { animation-delay: .55s; } .lp-title span:nth-child(6) { animation-delay: .65s; color: var(--lav-deep); }

.st-key-lp_hero [data-testid="stHorizontalBlock"] { align-items: flex-start; gap: 1.5rem; }
.lp-chip { display: inline-block; background: var(--lav); border: 1.5px solid var(--leaf); border-radius: 999px; padding: .4rem 1rem; font-size: .74rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin: 1rem 0 .9rem; animation: lpFloat 5s ease-in-out infinite alternate; }
.lp-copy { animation: lpUp 1s .9s cubic-bezier(.2,.8,.2,1) both; }
.lp-copy .lp-h2 { margin: 0 0 .8rem; font-family: var(--display) !important; font-weight: 500; font-size: clamp(1.9rem, 3.4vw, 3rem); line-height: 1.05; }
.lp-copy .lp-h2 em { font-family: 'Fraunces', Georgia, serif; font-style: italic; font-weight: 400; color: var(--lav-deep); display: block; font-size: 1.12em; }
.lp-copy p { margin: 0 0 .4rem; font-size: .95rem; line-height: 1.6; color: var(--muted); max-width: 42ch; }

.lp-art { position: relative; z-index: 2; margin-top: calc(-1 * clamp(2rem, 12vw, 12rem)); pointer-events: none; }
.lp-art svg { width: 100%; height: auto; overflow: visible; }
.sway { transform-box: fill-box; transform-origin: 50% 100%; animation: lpSway 6s ease-in-out infinite alternate; }
.sway.s2 { animation-duration: 7.5s; animation-delay: -2s; } .sway.s3 { animation-duration: 5s; animation-delay: -1s; }
.grain { transform-box: fill-box; transform-origin: center; opacity: 0; animation: lpPop .6s cubic-bezier(.2,1.4,.4,1) forwards; }
.drift { animation: lpFloat 9s ease-in-out infinite alternate; }
.rise { animation: lpRise 1.4s cubic-bezier(.2,.8,.2,1) both; }
@media (max-width: 900px) { .lp-art { margin-top: 0; } }

/* ---------- tombol masuk ---------- */
.st-key-cta_wrap { margin-top: .8rem; animation: lpUp 1s 1.1s cubic-bezier(.2,.8,.2,1) both; }
.st-key-cta_wrap button { background: var(--leaf) !important; border: 2px solid var(--leaf) !important; border-radius: 999px !important; padding: .55rem 1.7rem !important; min-height: 3.1rem; transition: transform .25s, background .25s, box-shadow .25s; box-shadow: 6px 6px 0 var(--lav); }
.st-key-cta_wrap button p { color: var(--cream) !important; font-weight: 700 !important; font-size: 1rem !important; letter-spacing: .02em; }
.st-key-cta_wrap button:hover { background: var(--lav-deep) !important; border-color: var(--lav-deep) !important; transform: translate(-2px, -2px); box-shadow: 9px 9px 0 var(--lav); }
.st-key-cta_wrap button:active { transform: translate(3px, 3px); box-shadow: 2px 2px 0 var(--lav); }

/* ---------- marquee ---------- */
.lp-marquee { overflow: hidden; margin: 3rem 0 0; background: var(--leaf); color: var(--cream); padding: .9rem 0; border-block: 3px solid var(--lav); }
.lp-track { display: flex; width: max-content; animation: lpMarq 28s linear infinite; font-family: var(--display); font-weight: 600; font-size: 1.35rem; letter-spacing: .02em; white-space: nowrap; }
.lp-track span { padding: 0 1.4rem; } .lp-track span:nth-child(even) { color: var(--lav); }
.lp-marquee:hover .lp-track { animation-play-state: paused; }


/* ---------- angka ---------- */
.lp-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; margin-top: 3.2rem; }
@media (max-width: 800px) { .lp-stats { grid-template-columns: repeat(2, 1fr); } }
.lp-stat { border-top: 3px solid var(--leaf); padding-top: .9rem; animation: lpUp .9s both; transition: transform .35s cubic-bezier(.2,.8,.2,1); }
.lp-stat:nth-child(2) { animation-delay: .1s; } .lp-stat:nth-child(3) { animation-delay: .2s; } .lp-stat:nth-child(4) { animation-delay: .3s; }
.lp-stat b { display: block; font-family: var(--display); font-weight: 800; font-size: clamp(2.8rem, 6.5vw, 5.4rem); line-height: 1; letter-spacing: -.04em; transition: color .3s, transform .35s cubic-bezier(.3,1.6,.5,1); }
.lp-stat span { display: block; margin-top: .4rem; font-size: .95rem; font-weight: 600; }
.lp-stat:hover { border-top-color: var(--lav-deep); }
.lp-stat:hover b { color: var(--lav-deep); transform: translateY(-5px) scale(1.04); transform-origin: left bottom; }
.lp-step { transition: transform .3s cubic-bezier(.2,.8,.2,1), border-color .3s; }
.lp-step:hover { transform: translateY(-5px); border-top-color: var(--lav-deep); }

/* ---------- fitur ---------- */
.lp-sec { margin-top: 4.5rem; }
.lp-sec-h { display: flex; align-items: end; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.lp-sec-h .lp-h3 { margin: 0; font-size: clamp(1.8rem, 4vw, 3rem); line-height: 1; font-family: var(--display) !important; font-weight: 800; letter-spacing: -.03em; }
.lp-sec-h .lp-h3 em { font-family: 'Fraunces', Georgia, serif; font-weight: 400; color: var(--lav-deep); }
.lp-sec-h p { margin: 0; max-width: 36ch; color: var(--muted); font-size: .92rem; }
[class*="st-key-fc_"] { position: relative; }
[class*="st-key-fc_"] [data-testid="stButton"] { position: absolute; inset: 0; z-index: 5; }
[class*="st-key-fc_"] [data-testid="stButton"] > div, [class*="st-key-fc_"] button { width: 100%; height: 100%; }
[class*="st-key-fc_"] button { opacity: 0; cursor: pointer; border-radius: 22px; }
[class*="st-key-fc_"] button:focus-visible { opacity: 1; background: transparent !important; outline: 3px solid var(--lav-deep); }
.lp-card .go { position: absolute; left: 1.3rem; bottom: 1.2rem; font-weight: 700; font-size: .85rem; color: var(--leaf); z-index: 2; transition: color .35s, transform .35s; }
[class*="st-key-fc_"]:hover .lp-card .go { transform: translateX(6px); }
.lp-card { position: relative; display: block; overflow: hidden; background: var(--paper); border: 1.5px solid var(--leaf); border-radius: 22px 22px 22px 6px; padding: 1.4rem 1.3rem 1.6rem; min-height: 230px; height: 100%; transition: transform .35s cubic-bezier(.2,.8,.2,1), background .35s, color .35s; animation: lpUp .9s both; }
.lp-card::before { content: ""; position: absolute; width: 190px; height: 190px; right: -70px; bottom: -80px; border-radius: 50%; background: var(--lav); transition: transform .5s cubic-bezier(.2,.8,.2,1); }
[class*="st-key-fc_"]:hover .lp-card { transform: translateY(-8px) rotate(-.6deg); background: var(--leaf); color: var(--cream); }
[class*="st-key-fc_"]:hover .lp-card::before { transform: scale(2.6); }
[class*="st-key-fc_"]:hover .lp-card :is(.ct, p, .no) { color: var(--cream) !important; }
.lp-card > * { position: relative; z-index: 1; }
.lp-card .no { font-family: var(--display); font-weight: 800; font-size: .95rem; color: var(--lav-deep); letter-spacing: .1em; }
.lp-card .ct { margin: 2.2rem 0 .5rem; font-size: 1.4rem; line-height: 1.1; transition: color .35s; }
.lp-card p { margin: 0; font-size: .92rem; line-height: 1.5; color: var(--leaf); transition: color .35s; max-width: 34ch; }

/* ---------- langkah ---------- */
.lp-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem; }
@media (max-width: 800px) { .lp-steps { grid-template-columns: 1fr; } }
.lp-step { border-top: 3px solid var(--leaf); padding-top: .9rem; }
.lp-step b { font-family: var(--display); font-size: 3.2rem; font-weight: 800; line-height: 1; color: var(--lav-deep); display: block; }
.lp-step .lp-st { margin: .3rem 0 .3rem; font-size: 1.1rem; font-family: var(--display) !important; }
.lp-step p { margin: 0; color: var(--muted); font-size: .9rem; }
.lp-foot { margin-top: 3rem; text-align: center; font-size: .8rem; color: var(--muted); }


@keyframes lpLetter { to { opacity: 1; transform: none; } }
@keyframes lpUp { from { opacity: 0; transform: translateY(28px); } to { opacity: 1; transform: none; } }
@keyframes lpDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: none; } }
@keyframes lpSway { from { transform: rotate(-2.2deg); } to { transform: rotate(2.6deg); } }
@keyframes lpFloat { from { transform: translateY(0); } to { transform: translateY(-14px); } }
@keyframes lpPop { from { opacity: 0; transform: scale(.2); } to { opacity: 1; transform: scale(1); } }
@keyframes lpRise { from { opacity: 0; transform: translateY(60px) scale(.96); } to { opacity: 1; transform: none; } }
@keyframes lpMarq { to { transform: translateX(-50%); } }

@media (prefers-reduced-motion: reduce) {
  .lp *, }
</style>
"""

CSS_ONLY_LANDING = """
<style>
.lp-marquee { transform: none !important; width: 100vw !important; margin-left: calc(50% - 50vw) !important; margin-right: 0 !important; }
.lp-foot { padding-bottom: 1rem; }
</style>
"""


def _art() -> str:
    """Ilustrasi rumpun padi: daun hijau tua, malai dengan bulir lavender."""
    leaves = [
        # (path, kelas goyang, warna)
        ("M300 520 C 250 400, 120 330, 40 300 C 120 360, 190 420, 300 520Z", "s2", "#1F3B2E"),
        ("M330 520 C 330 380, 260 260, 150 170 C 250 270, 300 390, 330 520Z", "s3", "#355744"),
        ("M360 520 C 420 400, 560 330, 700 320 C 600 370, 470 430, 360 520Z", "s2", "#1F3B2E"),
        ("M345 520 C 380 380, 470 270, 600 200 C 500 290, 420 400, 345 520Z", "s3", "#2A4B3A"),
    ]
    out = ['<svg viewBox="0 0 740 540" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    out.append('<circle class="drift" cx="560" cy="150" r="90" fill="#CBB3E8" opacity=".55"/>')
    out.append('<circle class="drift" cx="130" cy="120" r="38" fill="#CBB3E8" opacity=".4" style="animation-delay:-3s"/>')
    out.append('<g class="rise">')
    for d, cls, col in leaves:
        out.append(f'<g class="sway {cls}"><path d="{d}" fill="{col}"/></g>')
    # tiga malai: (titik pangkal x, arah kelengkungan, jumlah bulir, kelas)
    panicles = [
        (340, 520, 250, 90, 11, "s2", 0.9),
        (335, 520, 170, 150, 9, "s3", 1.3),
        (350, 520, 440, 120, 10, "sway", 1.7),
    ]
    for i, (x0, y0, x1, y1, n, cls, delay) in enumerate(panicles):
        cx, cy = (x0 + x1) / 2 - 40 + i * 40, (y0 + y1) / 2 - 80
        out.append(f'<g class="sway {cls}">')
        out.append(f'<path d="M{x0} {y0} Q {cx} {cy} {x1} {y1}" fill="none" stroke="#1F3B2E" stroke-width="5" stroke-linecap="round"/>')
        for k in range(n):
            t = 0.45 + 0.55 * k / (n - 1)
            # titik di kurva kuadratik
            bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
            by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1
            side = -1 if k % 2 else 1
            ang = 25 * side + (-20 if x1 < x0 else 20)
            gx, gy = bx + side * 13, by
            out.append(
                f'<ellipse class="grain" cx="{gx:.0f}" cy="{gy:.0f}" rx="9" ry="19" transform="rotate({ang} {gx:.0f} {gy:.0f})" '
                f'fill="#CBB3E8" stroke="#5E3F93" stroke-width="2" style="animation-delay:{delay + k * 0.09:.2f}s"/>'
            )
        out.append("</g>")
    out.append("</g></svg>")
    return "".join(out)


FEATURES = [
    ("01", "Diagnosis gejala", "Pilih gejala yang terlihat pada tanaman. Sistem menebak penyakit atau hama yang paling mungkin dan memberi langkah awal.", "Diagnosis"),
    ("02", "Kamus penyakit dan hama", "Daftar penyakit dan hama padi lengkap dengan ciri, gejala khas, dan cara penanganan awal.", "Kamus penyakit dan hama"),
    ("03", "Kelola aturan", "Untuk pakar: tambah, ubah, atau hapus aturan JIKA-MAKA yang dipakai sistem saat mendiagnosis.", "Kelola aturan"),
    ("04", "Riwayat konsultasi", "Catatan semua diagnosis yang pernah dijalankan, beserta aturan yang paling sering dipakai.", "Riwayat konsultasi"),
]


def render(stats: list | None = None) -> None:
    """Tampilkan landing page. Semua elemen yang bisa ditekan adalah tombol Streamlit."""
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(CSS_ONLY_LANDING, unsafe_allow_html=True)

    # --- judul raksasa
    letters = "".join(f"<span>{c}</span>" for c in "ORYZAI")
    st.markdown(f'<div class="lp"><div class="lp-title" role="img" aria-label="OryzAI">{letters}</div></div>', unsafe_allow_html=True)

    # --- teks + tombol (kiri), ilustrasi (kanan): tidak saling menimpa
    with st.container(key="lp_hero"):
        left, right = st.columns([1, 1.15], gap="large")
        with left:
            st.markdown(
                '<div class="lp"><div class="lp-chip">Cek padi dalam semenit</div>'
                '<div class="lp-copy"><div class="lp-h2">Diagnosis padi<em>dengan tenang.</em></div>'
                "<p>Kenali hama dan penyakit tanaman padi dari gejala yang Anda lihat, lengkap dengan langkah awal yang aman.</p></div></div>",
                unsafe_allow_html=True,
            )
            with st.container(key="cta_wrap"):
                st.button("Mulai diagnosis", key="enter_app", on_click=nav.go, args=(nav.SCREEN,))
        with right:
            st.markdown(f'<div class="lp"><div class="lp-art">{_art()}</div></div>', unsafe_allow_html=True)

    # --- marquee
    marquee = "".join(f"<span>{w}</span>" for w in ["Penyakit padi", "Hama wereng", "Blas", "Hawar daun", "Tungro", "Certainty Factor", "Sistem pakar", "Skrining awal"] * 2)
    st.markdown(f'<div class="lp"><div class="lp-marquee" aria-hidden="true"><div class="lp-track">{marquee}</div></div></div>', unsafe_allow_html=True)

    # --- angka pengetahuan sistem (diambil dari data nyata)
    if stats:
        cells = "".join(f'<div class="lp-stat"><b>{v}</b><span>{l}</span></div>' for v, l in stats)
        st.markdown(f'<div class="lp"><div class="lp-stats">{cells}</div></div>', unsafe_allow_html=True)

    # --- kartu fitur: seluruh kartu bisa ditekan
    st.markdown(
        '<div class="lp"><div class="lp-sec"><div class="lp-sec-h"><div class="lp-h3">Semua yang Anda butuhkan,<br><em>dalam satu tempat.</em></div>'
        "</div></div></div>",
        unsafe_allow_html=True,
    )
    fcols = st.columns(4, gap="medium")
    for i, (col, (n, t, d, page)) in enumerate(zip(fcols, FEATURES)):
        with col:
            with st.container(key=f"fc_{i}"):
                st.markdown(
                    f'<div class="lp"><div class="lp-card"><span class="no">{n}</span><div class="ct">{t}</div><p>{d}</p></div></div>',
                    unsafe_allow_html=True,
                )
                st.button(t, key=f"card_{i}", on_click=nav.go, args=(page,))

    # --- langkah + footer
    st.markdown(
        '<div class="lp">'
        '<div class="lp-sec"><div class="lp-sec-h"><div class="lp-h3">Tiga langkah <em>sederhana.</em></div></div>'
        '<div class="lp-steps">'
        '<div class="lp-step"><b>1</b><div class="lp-st">Pilih gejala</div><p>Tandai yang terlihat pada daun, pelepah, batang, atau hama.</p></div>'
        '<div class="lp-step"><b>2</b><div class="lp-st">Atur keyakinan</div><p>Dari “kurang yakin” sampai “sangat yakin”.</p></div>'
        '<div class="lp-step"><b>3</b><div class="lp-st">Lihat hasilnya</div><p>Dugaan diagnosis, alasan, dan langkah awal penanganan.</p></div>'
        "</div></div>"
        '<div class="lp-foot">OryzAI adalah alat bantu skrining awal, bukan pengganti penyuluh pertanian.</div>'
        "</div>",
        unsafe_allow_html=True,
    )
