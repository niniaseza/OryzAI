"""Mesin inferensi forward chaining dan Certainty Factor.

CF yang didukung aplikasi berada pada rentang 0..1 (dukungan positif).
Ini adalah skor dukungan berbasis aturan, bukan probabilitas statistik.
"""
from __future__ import annotations


def _bounded_cf(value: float) -> float:
    """Konversi CF ke float dan batasi pada rentang dukungan 0..1."""
    number = float(value)
    if number != number:  # NaN
        raise ValueError("CF tidak boleh NaN.")
    return max(0.0, min(1.0, number))


def combine_cf(cf1: float, cf2: float) -> float:
    """Gabungkan dua bukti positif untuk hipotesis yang sama.

    Formula: CF(H,E1 AND E2) = CF1 + CF2 * (1 - CF1).
    Fungsi ini untuk CF non-negatif; bukti negatif tidak dimodelkan aplikasi.
    """
    a = _bounded_cf(cf1)
    b = _bounded_cf(cf2)
    return round(a + b * (1.0 - a), 4)


def infer(facts: dict, rules: list, diseases: list, threshold: float = 0.25) -> dict:
    """Jalankan forward chaining dari fakta input ke kandidat diagnosis.

    Antecedent dalam satu rule diperlakukan sebagai konjungsi (AND). Untuk
    konservatisme, kekuatan bukti rule adalah CF input terendah dikali CF rule.
    Rule yang aktif dicatat berurutan sebagai reasoning trace.
    """
    threshold = _bounded_cf(threshold)
    known = {}
    for key, value in facts.items():
        cf = _bounded_cf(value)
        if cf > 0:
            known[str(key)] = cf

    scores: dict[str, float] = {}
    trace: list[dict] = []
    for rule in rules:
        antecedents = rule.get("antecedents", [])
        if not antecedents or not all(known.get(s, 0.0) > 0 for s in antecedents):
            continue
        evidence_cf = min(known[s] for s in antecedents)
        rule_cf = _bounded_cf(rule.get("cf", 0.0))
        contribution = round(evidence_cf * rule_cf, 4)
        disease_id = rule.get("disease_id")
        previous = scores.get(disease_id, 0.0)
        combined = contribution if previous <= 0 else combine_cf(previous, contribution)
        scores[disease_id] = combined
        trace.append({
            "rule_id": rule.get("id", "(tanpa ID)"),
            "disease_id": disease_id,
            "antecedents": list(antecedents),
            "input_confidences": {s: known[s] for s in antecedents},
            "evidence_cf": round(evidence_cf, 4),
            "rule_cf": round(rule_cf, 4),
            "contribution_cf": contribution,
            "previous_cf": round(previous, 4),
            "combined_cf": round(combined, 4),
            "description": rule.get("description", ""),
            "source_ids": rule.get("source_ids", []),
        })

    dmap = {d["id"]: d for d in diseases}
    diagnoses = []
    for disease_id, score in scores.items():
        if score >= threshold and disease_id in dmap:
            diagnoses.append({
                **dmap[disease_id],
                "cf": round(score, 4),
                "confidence_percent": round(score * 100, 1),
            })
    diagnoses.sort(key=lambda diagnosis: diagnosis["cf"], reverse=True)
    return {
        "diagnoses": diagnoses,
        "trace": trace,
        "working_memory": {
            "known_facts": known,
            "fired_rule_ids": [item["rule_id"] for item in trace],
            "inferred_facts": [f"candidate:{item['id']}" for item in diagnoses],
            "candidate_scores": {key: round(value, 4) for key, value in scores.items()},
        },
    }


def validate_rule(rule: dict, symptom_ids: set, disease_ids: set, source_ids: set | None = None) -> list[str]:
    """Validasi struktur rule sebelum disimpan ke basis pengetahuan."""
    errors: list[str] = []
    rule_id = str(rule.get("id", "")).strip()
    if not rule_id:
        errors.append("ID aturan wajib diisi.")
    if not isinstance(rule.get("antecedents", []), list):
        errors.append("Gejala pada bagian JIKA harus berupa daftar.")
        antecedents = []
    else:
        antecedents = rule.get("antecedents", [])
    if len(antecedents) < 1:
        errors.append("Aturan harus memiliki minimal satu gejala.")
    if len(set(antecedents)) != len(antecedents):
        errors.append("Gejala yang sama tidak boleh dipilih lebih dari sekali.")
    if any(s not in symptom_ids for s in antecedents):
        errors.append("Ada ID gejala yang tidak dikenal.")
    if rule.get("disease_id") not in disease_ids:
        errors.append("Diagnosis tujuan tidak dikenal.")
    try:
        cf = float(rule.get("cf", -1))
        if not 0 <= cf <= 1:
            errors.append("CF harus berada pada rentang 0 sampai 1.")
    except (TypeError, ValueError):
        errors.append("CF harus berupa angka.")
    if not str(rule.get("description", "")).strip():
        errors.append("Deskripsi/alasan aturan wajib diisi.")
    sources = rule.get("source_ids", [])
    if not isinstance(sources, list):
        errors.append("Sumber rujukan harus berupa daftar.")
    elif source_ids is not None:
        if not sources:
            errors.append("Pilih minimal satu sumber rujukan.")
        if any(source not in source_ids for source in sources):
            errors.append("Ada ID sumber rujukan yang tidak dikenal.")
    return errors
