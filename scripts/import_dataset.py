"""Impor Dataset_Sistem_Pakar_Padi_versi2.xlsx ke basis pengetahuan aplikasi.

Jalankan dari akar proyek:  python scripts/import_dataset.py
Butuh openpyxl (hanya untuk impor, tidak untuk menjalankan aplikasi): pip install openpyxl
Menimpa: data/symptoms.json, diseases.json, rules.json, sources.json,
         data/dataset_gejala_diagnosis.csv, data/knowledge_sources.csv, data/test_cases.csv
"""
from __future__ import annotations

import csv
import itertools
import json
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
XLSX = DATA / "Dataset_Sistem_Pakar_Padi_versi2.xlsx"
sys.path.insert(0, str(ROOT))
from expert_system.engine import infer  # noqa: E402

# Kategori organ di dataset -> kelompok tampilan di aplikasi
GROUP = {
    "Daun": "Daun",
    "Daun / Pelepah": "Pelepah dan batang",
    "Batang": "Pelepah dan batang",
    "Batang / Pelepah": "Pelepah dan batang",
    "Malai": "Malai dan bulir",
    "Malai / Bulir": "Malai dan bulir",
    "Daun / Pertumbuhan": "Warna dan pertumbuhan",
    "Daun / Tanaman": "Warna dan pertumbuhan",
    "Tanda Lapangan": "Tanda hama di lapangan",
}
GROUP_ORDER = ["Daun", "Pelepah dan batang", "Malai dan bulir", "Warna dan pertumbuhan", "Tanda hama di lapangan"]
KIND = {"Jamur": "jamur", "Bakteri": "bakteri", "Virus": "virus", "Serangga": "serangga", "Mollusca": "moluska", "Mamalia": "mamalia"}

SOURCES = [
    {"source_id": "DATASET_V2", "reference": "Dataset_Sistem_Pakar_Padi_versi2.xlsx (sheet Master Hama & Penyakit, Master Gejala, Aturan & CF Pakar, Rekomendasi Penanganan).", "url": "", "role": "Basis pengetahuan utama aplikasi: gejala, aturan, bobot CF pakar, dan rekomendasi penanganan."},
    {"source_id": "IRRI_RKB", "reference": "IRRI Rice Knowledge Bank (International Rice Research Institute).", "url": "https://www.knowledgebank.irri.org/", "role": "Rujukan yang disebut pada dataset untuk gejala dan penanganan."},
    {"source_id": "BSIP_PADI", "reference": "BSIP Padi, Kementerian Pertanian Republik Indonesia.", "url": "", "role": "Rujukan yang disebut pada dataset untuk gejala dan penanganan."},
    {"source_id": "JUKNIS_OPT", "reference": "Petunjuk teknis OPT, Direktorat Perlindungan Tanaman Pangan, Kementerian Pertanian RI.", "url": "", "role": "Rujukan yang disebut pada dataset untuk pengendalian organisme pengganggu tanaman."},
]


def rows(ws, header_row=4):
    it = ws.iter_rows(min_row=header_row, values_only=True)
    head = [h for h in next(it)]
    for r in it:
        if r and r[0]:
            yield dict(zip(head, r))


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    master = list(rows(wb["Master Hama & Penyakit"]))
    gejala = list(rows(wb["Master Gejala"]))
    aturan = list(rows(wb["Aturan & CF Pakar"]))
    rekom = {r["Kode HP"]: r for r in rows(wb["Rekomendasi Penanganan"])}

    # --- aturan
    rules = []
    for r in aturan:
        rules.append({
            "id": r["Kode Rule"], "antecedents": [r["Kode Gejala"]], "disease_id": r["Kode HP"],
            "cf": float(r["CF Pakar (MB)"]), "description": r["Deskripsi Gejala"],
            "role": r["Tingkat Peran Gejala"], "source_ids": ["DATASET_V2"],
        })
    dname = {m["Kode HP"]: m["Nama Hama / Penyakit"] for m in master}

    # --- gejala
    first_label, links = {}, {}
    for r in rules:
        g = r["antecedents"][0]
        first_label.setdefault(g, r["description"])
        links.setdefault(g, []).append(dname[r["disease_id"]])
    symptoms = []
    for g in gejala:
        gid = g["Kode Gejala"]
        organ = g["Kategori Organ"]
        names = links.get(gid, [])
        why = "Gejala ini mendukung: " + ", ".join(names) + "." if names else "Gejala pendukung."
        symptoms.append({
            "id": gid, "label": first_label.get(gid, g["Deskripsi Gejala Visual"]), "category": GROUP[organ],
            "organ": organ, "why": why, "description": g["Deskripsi Gejala Visual"], "source_ids": ["DATASET_V2"],
        })
    symptoms.sort(key=lambda s: (GROUP_ORDER.index(s["category"]), s["id"]))

    # --- penyakit dan hama
    diseases = []
    for m in master:
        code = m["Kode HP"]
        kat = m["Kategori"]  # contoh: "Penyakit (Jamur)"
        tipe, _, agen = kat.partition(" (")
        agen = agen.rstrip(")")
        kind = "Penyakit" if tipe.startswith("Penyakit") else "Hama"
        rk = rekom[code]
        diseases.append({
            "id": code, "name": m["Nama Hama / Penyakit"], "type": kind, "scientific_name": m["Nama Latin / Agen Pengganggu"],
            "category": kat, "organ": m["Organ Utama Terdiserang"],
            "summary": f"{kind} golongan {KIND.get(agen, agen.lower())}. Bagian tanaman yang diserang: {m['Organ Utama Terdiserang']}.",
            "symptom_ids": [r["antecedents"][0] for r in rules if r["disease_id"] == code],
            "recommendations": [
                "Hayati/kultural: " + rk["Penanganan Hayati / Kultural"],
                "Kimiawi (rujukan bahan aktif): " + rk["Penanganan Kimiawi (Bahan Aktif & Aplikasi)"],
            ],
            "caution": "Diagnosis visual hanya dugaan awal. Bahan aktif di atas adalah rujukan; ikuti label produk dan anjuran penyuluh atau petugas perlindungan tanaman setempat.",
        })

    def dump(name, obj):
        (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

    dump("symptoms.json", symptoms)
    dump("diseases.json", diseases)
    dump("rules.json", rules)
    dump("sources.json", SOURCES)

    slabel = {s["id"]: s["label"] for s in symptoms}
    with (DATA / "dataset_gejala_diagnosis.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rule_id", "gejala_ids", "gejala_teramati", "diagnosis_id", "diagnosis", "cf_rule", "peran_gejala", "deskripsi_aturan", "source_ids"])
        for r in rules:
            w.writerow([r["id"], ";".join(r["antecedents"]), " + ".join(slabel[a] for a in r["antecedents"]), r["disease_id"], dname[r["disease_id"]], r["cf"], r["role"], r["description"], ";".join(r["source_ids"])])
    with (DATA / "knowledge_sources.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_id", "reference", "url", "role"])
        w.writeheader()
        w.writerows(SOURCES)

    # --- skenario uji: himpunan gejala terkecil milik tiap diagnosis yang membuatnya peringkat pertama tanpa seri
    cases = []
    for i, d in enumerate(diseases, 1):
        syms = d["symptom_ids"]
        chosen = None
        for size in range(2, len(syms) + 1):
            best = None
            for combo in itertools.combinations(syms, size):
                out = infer({s: 1.0 for s in combo}, rules, diseases)["diagnoses"]
                if out and out[0]["id"] == d["id"]:
                    margin = out[0]["cf"] - (out[1]["cf"] if len(out) > 1 else 0)
                    if best is None or margin > best[0]:
                        best = (margin, combo)
            if best:
                chosen = best[1]
                break
        if chosen is None:
            raise SystemExit(f"Tidak ada skenario unik untuk {d['id']}")
        cases.append([f"T{i:02d}", d["name"], ";".join(chosen), d["id"], "Gejala khas: " + ", ".join(rules_r["id"] for rules_r in rules if rules_r["disease_id"] == d["id"] and rules_r["antecedents"][0] in chosen)])
    with (DATA / "test_cases.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "case_name", "symptoms", "expected_diagnosis", "purpose"])
        w.writerows(cases)
    print(f"{len(diseases)} penyakit/hama, {len(symptoms)} gejala, {len(rules)} aturan, {len(cases)} skenario uji")


if __name__ == "__main__":
    main()
