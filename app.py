"""Antarmuka Streamlit sistem pakar diagnosis hama dan penyakit padi."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from expert_system.engine import infer, validate_rule
from expert_system.storage import append_history, load_json, read_history, save_json
from ui import landing, nav, theme

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
LOG = BASE / "logs" / "consultation_history.csv"

OPTIONS = [0.0, 0.4, 0.7, 1.0]
LABELS = {0.0: "Tidak terlihat", 0.4: "Kurang yakin", 0.7: "Cukup yakin", 1.0: "Sangat yakin"}
LEVEL_TEXT = {
    0.0: "gejala tidak ada atau tidak sempat diperiksa",
    0.4: "sepertinya ada, tetapi belum jelas",
    0.7: "terlihat cukup jelas",
    1.0: "terlihat jelas dan Anda yakin",
}
CATEGORY_HINT = {
    "Daun": "Bercak, warna, dan bentuk luka pada helai daun",
    "Pelepah dan batang": "Pelepah, pangkal batang, dan kondisi batang",
    "Malai dan bulir": "Leher malai, malai, dan bulir padi",
    "Warna dan pertumbuhan": "Perubahan warna dan pertumbuhan seluruh tanaman",
    "Tanda hama di lapangan": "Serangga, telur, ulat, dan jejak hama di sawah",
}
PAGES = ["Diagnosis", "Kamus penyakit dan hama", "Kelola aturan", "Riwayat konsultasi"]
MIN_SYMPTOMS = 1
TIE_MARGIN = 5.0  # selisih skor (poin persen) yang dianggap setara


# ---------------------------------------------------------------- data
def get_data():
    return load_json(DATA / "symptoms.json"), load_json(DATA / "diseases.json"), load_json(DATA / "rules.json")


def load_examples():
    path = DATA / "test_cases.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {r["case_name"]: [x for x in r["symptoms"].split(";") if x] for r in csv.DictReader(f)}


# ---------------------------------------------------------------- state & callbacks
def _facts() -> dict:
    return st.session_state.setdefault("facts", {})


def _set_widget_values(values: dict):
    """Samakan nilai semua pilihan gejala dengan `values` (dipakai oleh callback)."""
    for s in load_json(DATA / "symptoms.json"):
        st.session_state[f"sym_{s['id']}"] = values.get(s["id"], 0.0)


def on_symptom_change(sid: str):
    value = st.session_state.get(f"sym_{sid}", 0.0)
    facts = _facts()
    if value > 0:
        facts[sid] = value
    else:
        facts.pop(sid, None)


def reset_all():
    st.session_state["facts"] = {}
    st.session_state.pop("last_result", None)
    st.session_state["stage"] = "input"
    _set_widget_values({})


def edit_symptoms():
    st.session_state["stage"] = "input"


def load_example():
    name = st.session_state.get("example_pick")
    examples = load_examples()
    if name in examples:
        st.session_state["facts"] = {sid: 1.0 for sid in examples[name]}
        _set_widget_values(st.session_state["facts"])
        st.session_state["stage"] = "input"
        st.session_state.pop("last_result", None)
    st.session_state["example_pick"] = None


def run_analysis():
    _, diseases, rules = get_data()
    facts = dict(_facts())
    result = infer(facts, rules, diseases)
    st.session_state["last_facts"] = facts
    st.session_state["last_result"] = result
    st.session_state["stage"] = "result"
    append_history(LOG, facts, result)


def go_to(page: str):
    nav.go(page)


# ---------------------------------------------------------------- halaman Diagnosis
def symptom_row(s: dict, facts: dict):
    sid = s["id"]
    current = facts.get(sid, 0.0)
    prefix = "on_row_" if current > 0 else "off_row_"
    with st.container(key=prefix + sid):
        left, right = st.columns([1.1, 1.3], vertical_alignment="center")
        with left:
            st.markdown(
                f'<div class="sym-label">{escape(s["label"])}</div><div class="sym-why">{escape(s["why"])}</div>',
                unsafe_allow_html=True,
            )
        with right:
            key = f"sym_{sid}"
            if key not in st.session_state:
                st.session_state[key] = current if current in OPTIONS else 0.0
            st.radio(
                s["label"],
                OPTIONS,
                format_func=LABELS.get,
                horizontal=True,
                key=key,
                label_visibility="collapsed",
                on_change=on_symptom_change,
                args=(sid,),
            )


def summary_panel(symptoms: list, facts: dict):
    label = {s["id"]: s["label"] for s in symptoms}
    n = len(facts)
    with st.container(key="summary_panel"):
        st.markdown("### Gejala yang Anda pilih")
        st.markdown(f'<div class="sum-count">{n} dari {len(symptoms)} gejala ditandai</div>', unsafe_allow_html=True)
        if n == 0:
            st.markdown(
                '<div class="sum-empty">Belum ada gejala. Mulai dari bagian <b>Daun</b>, lalu geser tombol keyakinan '
                "pada gejala yang Anda lihat. Atau coba contoh kasus di atas.</div>",
                unsafe_allow_html=True,
            )
        else:
            items = "".join(
                f"<li><span>{escape(label.get(k, k))}</span><i>{escape(LABELS[v])}</i></li>" for k, v in facts.items()
            )
            st.markdown(f'<ul class="sum-list">{items}</ul>', unsafe_allow_html=True)
        st.button(
            "Analisis gejala",
            type="primary",
            use_container_width=True,
            disabled=n < MIN_SYMPTOMS,
            on_click=run_analysis,
        )
        if n < MIN_SYMPTOMS:
            st.caption(f"Pilih minimal {MIN_SYMPTOMS} gejala. Makin banyak gejala yang cocok, makin kuat dugaannya.")
        if n:
            st.button("Kosongkan pilihan", use_container_width=True, on_click=reset_all)


def input_stage(symptoms: list):
    facts = _facts()
    st.markdown(theme.stepper(1 if len(facts) >= MIN_SYMPTOMS else 0), unsafe_allow_html=True)
    main, side = st.columns([2.15, 1], gap="large")
    with main:
        examples = load_examples()
        if examples:
            st.selectbox(
                "Baru pertama kali? Coba contoh kasus",
                list(examples),
                index=None,
                placeholder="Pilih contoh, gejalanya terisi otomatis",
                key="example_pick",
                on_change=load_example,
            )
        st.markdown(
            '<div class="legend"><b>Cara memilih tingkat keyakinan</b><ul>'
            + "".join(f"<li><em>{LABELS[v]}</em>: {LEVEL_TEXT[v]}</li>" for v in OPTIONS)
            + "</ul></div>",
            unsafe_allow_html=True,
        )
        categories = list(dict.fromkeys(s["category"] for s in symptoms))
        for cat in categories:
            items = [s for s in symptoms if s["category"] == cat]
            chosen = sum(1 for s in items if s["id"] in facts)
            badge = f'<span class="cnt">{chosen} dipilih</span>' if chosen else ""
            st.markdown(
                f'<div class="cat-head"><h3>{escape(cat)}</h3>{badge}<small>{escape(CATEGORY_HINT.get(cat, ""))}</small></div>',
                unsafe_allow_html=True,
            )
            for s in items:
                symptom_row(s, facts)
    with side:
        summary_panel(symptoms, facts)


# ---------------------------------------------------------------- hasil
def build_summary_text(result: dict, symptoms: list) -> str:
    label = {s["id"]: s["label"] for s in symptoms}
    lines = ["RINGKASAN KONSULTASI SISTEM PAKAR PADI", datetime.now().strftime("Waktu: %d-%m-%Y %H:%M"), "", "Gejala yang dipilih:"]
    for sid, cf in st.session_state.get("last_facts", {}).items():
        lines.append(f"- {label.get(sid, sid)}: {LABELS.get(cf, cf)} (CF {cf:.2f})")
    lines += ["", "Dugaan diagnosis:"]
    if result["diagnoses"]:
        for d in result["diagnoses"]:
            lines.append(f"- {d['name']}: {theme.level(d['confidence_percent'])['name']}, skor dukungan {d['confidence_percent']:.1f}% (CF {d['cf']:.2f})")
    else:
        lines.append("- Bukti belum cukup.")
    lines += ["", "Aturan yang aktif: " + (", ".join(result["working_memory"]["fired_rule_ids"]) or "tidak ada"), ""]
    lines.append("Catatan: hasil ini dugaan awal, bukan pengganti diagnosis penyuluh atau petugas perlindungan tanaman.")
    return "\n".join(lines)


def winner_card(d: dict, trace: list, smap: dict, rank_text: str = "paling mungkin"):
    pct = d["confidence_percent"]
    support = []
    for t in trace:
        if t["disease_id"] == d["id"]:
            support += [smap.get(s, s) for s in t["antecedents"]]
    support = list(dict.fromkeys(support))
    st.markdown(
        '<div class="result-main">'
        f'<span class="tag">{escape(d["type"])} {escape(rank_text)}</span>'
        f'<h2>{escape(d["name"])}</h2>'
        f'<p class="sci">{escape(d["scientific_name"])}</p>'
        f'<div class="score-row"><b>{pct:.0f}%</b>{theme.level_badge(pct)}</div>'
        f"{theme.meter(pct)}"
        f'<p class="lvl-advice">{escape(theme.level(pct)["advice"])}</p>'
        f'<p class="sum">{escape(d["summary"])}</p>'
        "</div>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1, 1], gap="medium")
    with left:
        recs = "".join(f"<li>{escape(r)}</li>" for r in d["recommendations"])
        st.markdown(f'<div class="box"><h4>Langkah awal yang disarankan</h4><ol>{recs}</ol></div>', unsafe_allow_html=True)
    with right:
        why = []
        for t in trace:
            if t["disease_id"] == d["id"]:
                names = " dan ".join(f"<b>{escape(smap.get(s, s))}</b>" for s in t["antecedents"])
                why.append(f'<div class="why-line">Anda memilih {names}.<small>{escape(t["description"])}</small></div>')
        st.markdown(f'<div class="box"><h4>Mengapa sistem menduga ini?</h4>{"".join(why)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="note"><b>Perhatian.</b> {escape(d["caution"])}</div>', unsafe_allow_html=True)


def technical_details(result: dict, symptoms: list):
    smap = {s["id"]: s["label"] for s in symptoms}
    with st.expander("Lihat cara kerja sistem (untuk pakar dan dosen)"):
        t1, t2, t3, t4 = st.tabs(["Aturan aktif", "Alur penalaran (HOW)", "Working memory", "Alasan pertanyaan (WHY)"])
        with t1:
            if not result["trace"]:
                st.info("Belum ada aturan yang aktif.")
            else:
                rows = [
                    {
                        "Aturan": t["rule_id"],
                        "Gejala yang cocok": " + ".join(smap.get(s, s) for s in t["antecedents"]),
                        "CF input terendah": t["evidence_cf"],
                        "CF aturan": t["rule_cf"],
                        "Kontribusi": t["contribution_cf"],
                        "CF gabungan": t["combined_cf"],
                    }
                    for t in result["trace"]
                ]
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                st.caption("Kontribusi = CF input terendah x CF aturan. Beberapa aturan untuk hipotesis yang sama digabung: CF1 + CF2 x (1 - CF1).")
        with t2:
            if not result["trace"]:
                st.info("Belum ada alur penalaran karena belum ada aturan aktif.")
            for t in result["trace"]:
                names = [smap.get(s, s) for s in t["antecedents"]]
                st.markdown(f"**{t['rule_id']}**: JIKA {' DAN '.join(names)} MAKA {t['disease_id']}.")
                st.write(t["description"])
                st.caption(
                    f"CF input terendah {t['evidence_cf']:.2f} x CF aturan {t['rule_cf']:.2f} = kontribusi {t['contribution_cf']:.2f}; "
                    f"CF gabungan {t['combined_cf']:.2f}. Sumber: {', '.join(t['source_ids'])}"
                )
        with t3:
            st.write("Fakta input:", st.session_state.get("last_facts", {}))
            st.write("Aturan aktif:", result["working_memory"]["fired_rule_ids"])
            st.write("Fakta hasil inferensi:", result["working_memory"]["inferred_facts"])
        with t4:
            st.caption("Setiap gejala ditanyakan karena membantu membedakan satu penyakit atau hama dari yang lain.")
            for s in symptoms:
                st.markdown(f"**{s['label']}**")
                st.caption(s["why"])


def result_stage(symptoms: list, diseases: list):
    result = st.session_state.get("last_result")
    if result is None:
        edit_symptoms()
        st.rerun()
    st.markdown(theme.stepper(2), unsafe_allow_html=True)
    smap = {s["id"]: s["label"] for s in symptoms}
    n = len(st.session_state.get("last_facts", {}))
    top = st.columns([2.4, 1, 1.1], vertical_alignment="center")
    top[0].markdown(f"### Hasil dari {n} gejala yang Anda pilih")
    top[1].button("Ubah gejala", on_click=edit_symptoms, use_container_width=True)
    top[2].button("Konsultasi baru", on_click=reset_all, use_container_width=True)

    diagnoses = result["diagnoses"]
    if not diagnoses:
        st.markdown(
            '<div class="box"><h4>Bukti belum cukup untuk menyimpulkan</h4>'
            "<p>Sistem sengaja tidak memaksakan jawaban. Coba lagi dengan:</p>"
            "<ul><li>Menambah gejala lain yang Anda lihat, terutama dari bagian tanaman yang berbeda.</li>"
            "<li>Memperbaiki tingkat keyakinan jika ada gejala yang sebenarnya terlihat jelas.</li>"
            "<li>Menghubungi penyuluh atau petugas perlindungan tanaman bila gejala meluas.</li></ul></div>",
            unsafe_allow_html=True,
        )
    else:
        top_pct = diagnoses[0]["confidence_percent"]
        ties = [d for d in diagnoses[1:] if top_pct - d["confidence_percent"] < TIE_MARGIN]
        winner_card(diagnoses[0], result["trace"], smap, "setara dengan kandidat lain" if ties else "paling mungkin")
        if ties:
            st.warning(
                f"Ada {len(ties)} kandidat lain dengan skor hampir sama (selisih kurang dari {TIE_MARGIN:.0f} poin). "
                "Jangan hanya mengandalkan urutan; periksa semuanya dan tambahkan gejala pembeda."
            )
        if len(diagnoses) > 1:
            st.markdown("### Kandidat lain")
            st.caption("Tingkat dihitung dari skor yang sama untuk semua kandidat, bukan dari urutan.")
            for d in diagnoses[1:]:
                p2 = d["confidence_percent"]
                with st.expander(f"{d['name']}: {p2:.0f}% ({theme.level(p2)['name']})"):
                    st.markdown(theme.level_badge(p2) + f'<p class="lvl-advice">{escape(theme.level(p2)["advice"])}</p>' + theme.meter(p2), unsafe_allow_html=True)
                    st.write(d["summary"])
                    st.markdown("**Langkah awal**")
                    for rec in d["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.caption(d["caution"])
        st.caption(
            "Tingkat Kritis, Gawat, Waspada, dan Dugaan awal dihitung dari skor dukungan (85%, 70%, 45%) dan menunjukkan seberapa mendesak tindak lanjutnya, "
            "bukan tingkat kerusakan tanaman. Skor dukungan menunjukkan seberapa kuat aturan pakar dan gejala Anda mendukung dugaan ini (Certainty Factor). "
            "Ini bukan peluang pasti. Aplikasi tidak memberikan dosis pestisida; ikuti label produk dan anjuran resmi setempat."
        )
    st.download_button(
        "Unduh ringkasan (TXT)",
        data=build_summary_text(result, symptoms),
        file_name="hasil_konsultasi_padi.txt",
        mime="text/plain",
    )
    technical_details(result, symptoms)


def consult(symptoms, diseases, rules):
    if st.session_state.get("stage", "input") == "result":
        result_stage(symptoms, diseases)
    else:
        st.markdown(theme.hero(), unsafe_allow_html=True)
        input_stage(symptoms)


# ---------------------------------------------------------------- Kamus
def rule_sentence(rule: dict, smap: dict, dmap: dict) -> str:
    cond = " dan ".join(f"<b>{escape(smap.get(s, s))}</b>" for s in rule["antecedents"])
    return f'<div class="rule-sentence">Jika {cond}, maka kemungkinan <b>{escape(dmap.get(rule["disease_id"], rule["disease_id"]))}</b> (bobot aturan {float(rule["cf"]):.2f}).</div>'


def knowledge(symptoms, diseases, rules):
    st.markdown(
        theme.page_head("Kamus penyakit dan hama", "Pelajari ciri, gejala khas, dan langkah awal untuk setiap penyakit atau hama yang dikenali sistem."),
        unsafe_allow_html=True,
    )
    smap = {s["id"]: s["label"] for s in symptoms}
    dmap = {d["id"]: d["name"] for d in diseases}
    t1, t2, t3 = st.tabs(["Penyakit dan hama", "Daftar gejala", "Aturan JIKA-MAKA"])
    with t1:
        c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
        query = c1.text_input("Cari", placeholder="Ketik nama atau ciri, misalnya wereng")
        kind = c2.radio("Tampilkan", ["Semua", "Penyakit", "Hama"], horizontal=True)
        shown = [
            d for d in diseases
            if (kind == "Semua" or d["type"] == kind)
            and query.lower() in (d["name"] + " " + d["summary"] + " " + d["scientific_name"]).lower()
        ]
        st.caption(f"Menampilkan {len(shown)} dari {len(diseases)}")
        if not shown:
            st.info("Tidak ada yang cocok. Coba kata kunci lain atau pilih Semua.")
        cols = st.columns(2, gap="medium")
        for i, d in enumerate(shown):
            with cols[i % 2]:
                sym = [smap[x] for x in d.get("symptom_ids", []) if x in smap]
                st.markdown(
                    f'<div class="dz"><span class="badge {d["type"].lower()}">{escape(d["type"])}</span>'
                    f'<h4>{escape(d["name"])}</h4><p class="sci">{escape(d["scientific_name"])}</p>'
                    f'<p class="sum">{escape(d["summary"])}</p>'
                    f'<div class="lbl">Gejala khas</div>{theme.chips(sym)}</div>',
                    unsafe_allow_html=True,
                )
                with st.expander("Penanganan awal"):
                    for rec in d["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.caption(d["caution"])
    with t2:
        st.caption("Cari gejala berdasarkan nama, bagian tanaman, atau alasan pertanyaan. Gejala dapat berkaitan dengan lebih dari satu diagnosis.")
        q_symptom = st.text_input("Cari gejala", placeholder="Contoh: bercak, malai, wereng", key="knowledge_symptom_query")
        categories = ["Semua"] + sorted({s.get("category", "Lainnya") for s in symptoms})
        selected_category = st.selectbox("Filter bagian tanaman", categories, key="knowledge_symptom_category")
        q = q_symptom.strip().casefold()
        symptom_rows = [
            {"Gejala": s["label"], "Bagian tanaman": s.get("category", "Lainnya"), "Mengapa ditanyakan": s.get("why", ""), "Deskripsi": s.get("description", ""), "ID": s["id"]}
            for s in symptoms
            if (selected_category == "Semua" or s.get("category", "Lainnya") == selected_category)
            and q in " ".join([s.get("label", ""), s.get("category", ""), s.get("why", ""), s.get("description", ""), s.get("id", "")]).casefold()
        ]
        st.caption(f"Menampilkan {len(symptom_rows)} dari {len(symptoms)} gejala")
        if symptom_rows:
            st.dataframe(pd.DataFrame(symptom_rows), use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada gejala yang cocok. Coba kata kunci atau filter lain.")
    with t3:
        st.caption("Setiap aturan berbunyi: jika beberapa gejala terlihat bersamaan, maka suatu diagnosis mungkin. Bobot aturan (CF) dari 0 sampai 1.")
        rows = [
            {
                "Aturan": r["id"],
                "Jika (gejala)": " + ".join(smap.get(x, x) for x in r["antecedents"]),
                "Maka (diagnosis)": dmap.get(r["disease_id"], r["disease_id"]),
                "Bobot": float(r["cf"]),
                "Sumber": ", ".join(r["source_ids"]),
            }
            for r in rules
        ]
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True, hide_index=True,
            column_config={"Bobot": st.column_config.ProgressColumn("Bobot aturan", min_value=0.0, max_value=1.0, format="%.2f")},
        )


# ---------------------------------------------------------------- Kelola aturan
def next_rule_id(rules: list) -> str:
    nums = [int(r["id"][1:]) for r in rules if str(r["id"]).startswith("R") and str(r["id"])[1:].isdigit()]
    return f"R{(max(nums) + 1) if nums else 1:02d}"


def manage_rules(symptoms, diseases, rules):
    st.markdown(
        theme.page_head("Kelola aturan", "Halaman untuk pakar. Tambah, ubah, atau hapus aturan JIKA-MAKA yang dipakai sistem saat mendiagnosis."),
        unsafe_allow_html=True,
    )
    flash = st.session_state.pop("flash", None)
    if flash:
        st.success(flash)
    if rules:
        st.markdown("**Contoh aturan yang sudah ada**")
        smap0 = {s["id"]: s["label"] for s in symptoms}
        dmap0 = {d["id"]: d["name"] for d in diseases}
        st.markdown(rule_sentence(rules[0], smap0, dmap0), unsafe_allow_html=True)
    st.markdown('<div class="note"><b>Periksa sumber dahulu.</b> Perubahan langsung tersimpan ke data/rules.json dan memengaruhi hasil diagnosis berikutnya.</div>', unsafe_allow_html=True)

    mode = st.radio("Pilih tindakan", ["Tambah aturan", "Ubah aturan", "Hapus aturan"], horizontal=True)
    symptom_ids = {s["id"] for s in symptoms}
    disease_ids = {d["id"] for d in diseases}
    source_ids = [s["source_id"] for s in load_json(DATA / "sources.json")]
    symptom_label = {s["id"]: s["label"] for s in symptoms}
    disease_label = {d["id"]: d["name"] for d in diseases}

    if mode == "Tambah aturan":
        with st.form("add_rule"):
            rid = st.text_input("ID aturan", value=next_rule_id(rules), help="Harus unik. Saran: nomor berikutnya.").strip()
            did = st.selectbox("Diagnosis (bagian MAKA)", list(disease_label), format_func=disease_label.get)
            ants = st.multiselect("Gejala (bagian JIKA), pilih minimal satu", list(symptom_label), format_func=symptom_label.get, placeholder="Pilih gejala")
            cf = st.slider("Bobot aturan (CF)", 0.0, 1.0, 0.8, 0.05, help="Makin dekat 1, makin kuat gejala itu menunjuk ke diagnosis.")
            desc = st.text_area("Penjelasan singkat", placeholder="Mengapa kombinasi gejala ini mendukung diagnosis?")
            src = st.multiselect("Sumber rujukan", source_ids, placeholder="Pilih sumber")
            submit = st.form_submit_button("Simpan aturan", type="primary")
        if submit:
            candidate = {"id": rid, "antecedents": ants, "disease_id": did, "cf": cf, "description": desc, "source_ids": src}
            errors = validate_rule(candidate, symptom_ids, disease_ids, set(source_ids))
            if any(r["id"] == rid for r in rules):
                errors.append("ID aturan sudah digunakan.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                rules.append(candidate)
                save_json(DATA / "rules.json", rules)
                st.session_state["flash"] = f"Aturan {rid} tersimpan."
                st.rerun()
    elif mode == "Ubah aturan":
        rid = st.selectbox("Pilih aturan", [r["id"] for r in rules])
        old = next(r for r in rules if r["id"] == rid)
        st.markdown(rule_sentence(old, symptom_label, disease_label), unsafe_allow_html=True)
        with st.form("edit_rule"):
            did = st.selectbox("Diagnosis (bagian MAKA)", list(disease_label), index=list(disease_label).index(old["disease_id"]), format_func=disease_label.get)
            ants = st.multiselect("Gejala (bagian JIKA)", list(symptom_label), default=old["antecedents"], format_func=symptom_label.get, placeholder="Pilih gejala")
            cf = st.slider("Bobot aturan (CF)", 0.0, 1.0, float(old["cf"]), 0.05)
            desc = st.text_area("Penjelasan singkat", old.get("description", ""))
            src = st.multiselect("Sumber rujukan", source_ids, default=old.get("source_ids", []), placeholder="Pilih sumber")
            submit = st.form_submit_button("Simpan perubahan", type="primary")
        if submit:
            candidate = {**old, "disease_id": did, "antecedents": ants, "cf": cf, "description": desc, "source_ids": src}
            errors = validate_rule(candidate, symptom_ids, disease_ids, set(source_ids))
            if errors:
                for e in errors:
                    st.error(e)
            else:
                save_json(DATA / "rules.json", [candidate if r["id"] == rid else r for r in rules])
                st.session_state["flash"] = f"Perubahan pada {rid} tersimpan."
                st.rerun()
    else:
        rid = st.selectbox("Pilih aturan yang akan dihapus", [r["id"] for r in rules])
        old = next(r for r in rules if r["id"] == rid)
        st.markdown(rule_sentence(old, symptom_label, disease_label), unsafe_allow_html=True)
        with st.form("delete_rule"):
            confirm = st.checkbox(f"Saya yakin ingin menghapus {rid}")
            submit = st.form_submit_button("Hapus aturan")
        if submit:
            if not confirm:
                st.error("Centang kotak konfirmasi dahulu.")
            else:
                save_json(DATA / "rules.json", [r for r in rules if r["id"] != rid])
                st.session_state["flash"] = f"Aturan {rid} dihapus."
                st.rerun()


# ---------------------------------------------------------------- Riwayat
def _safe_json(raw, default):
    try:
        return json.loads(raw)
    except Exception:
        return default


MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def _format_time(raw: str) -> str:
    try:
        dt = datetime.fromisoformat(raw)
        return f"{dt.day} {MONTHS[dt.month - 1]} {dt.year}, {dt:%H:%M}"
    except Exception:
        return raw


def history_page():
    st.markdown(
        theme.page_head("Riwayat konsultasi", "Catatan setiap analisis yang pernah dijalankan di aplikasi ini, beserta aturan yang paling sering dipakai."),
        unsafe_allow_html=True,
    )
    rows = read_history(LOG)
    if not rows:
        st.markdown(
            '<div class="box"><h4>Belum ada konsultasi</h4><p>Riwayat akan muncul di sini setelah Anda menjalankan analisis gejala pertama.</p></div>',
            unsafe_allow_html=True,
        )
        st.button("Mulai konsultasi", type="primary", on_click=go_to, args=("Diagnosis",))
        return
    raw = pd.DataFrame(rows)
    view = []
    for r in rows:
        facts = _safe_json(r.get("known_facts", "{}"), {})
        diag = _safe_json(r.get("diagnoses", "[]"), [])
        top = diag[0] if diag else None
        view.append(
            {
                "Waktu": _format_time(r.get("timestamp", "")),
                "Jumlah gejala": len(facts),
                "Diagnosis utama": top["name"] if top else "Bukti belum cukup",
                "Skor dukungan": round(top["cf"] * 100, 1) if top else 0.0,
                "Aturan aktif": ", ".join(_safe_json(r.get("rules_used", "[]"), [])) or "-",
            }
        )
    df = pd.DataFrame(view).iloc[::-1].reset_index(drop=True)
    m1, m2, m3 = st.columns(3)
    answered = df[df["Diagnosis utama"] != "Bukti belum cukup"]
    m1.markdown(theme.stat("Jumlah konsultasi", len(df)), unsafe_allow_html=True)
    m2.markdown(theme.stat("Diagnosis tersering", answered["Diagnosis utama"].mode().iat[0] if len(answered) else "-"), unsafe_allow_html=True)
    m3.markdown(theme.stat("Rata-rata gejala dipilih", f"{df['Jumlah gejala'].mean():.1f}"), unsafe_allow_html=True)
    st.write("")
    st.dataframe(
        df, use_container_width=True, hide_index=True,
        column_config={"Skor dukungan": st.column_config.ProgressColumn("Skor dukungan (%)", min_value=0, max_value=100, format="%.0f")},
    )
    counts: dict = {}
    for text in raw["rules_used"].fillna("[]"):
        for rid in _safe_json(text, []):
            counts[rid] = counts.get(rid, 0) + 1
    if counts:
        st.markdown("### Aturan yang paling sering dipakai")
        chart = pd.DataFrame(sorted(counts.items(), key=lambda x: x[1], reverse=True), columns=["Aturan", "Jumlah"]).set_index("Aturan")
        st.bar_chart(chart, color="#1F3B2E", horizontal=True, height=max(160, 46 * len(chart)))
    st.download_button("Unduh riwayat (CSV)", raw.to_csv(index=False).encode("utf-8-sig"), "riwayat_konsultasi.csv", "text/csv")


# ---------------------------------------------------------------- main
def main():
    st.set_page_config(page_title="OryzAI", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")
    theme.inject_css()
    nav.inject_css()
    page = nav.current()
    nav.navbar()
    nav.overlay()
    symptoms, diseases, rules = get_data()
    with st.container(key=nav.page_key()):
        if page == nav.HOME:
            n_src = len(load_json(DATA / "sources.json"))
            landing.render([(len(diseases), "penyakit dan hama"), (len(symptoms), "gejala dikenali"), (len(rules), "aturan pakar"), (n_src, "sumber rujukan")])
        else:
            if page == "Diagnosis":
                consult(symptoms, diseases, rules)
            elif page == "Kamus penyakit dan hama":
                knowledge(symptoms, diseases, rules)
            elif page == "Kelola aturan":
                manage_rules(symptoms, diseases, rules)
            else:
                history_page()
            st.markdown(
                '<div class="app-foot">OryzAI adalah alat bantu skrining awal. Bukan pengganti diagnosis ahli atau rekomendasi resmi pestisida.</div>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
