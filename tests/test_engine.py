"""Pengujian mesin inferensi, CF, validasi rule, dan skenario dataset."""
import csv
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from expert_system.engine import combine_cf, infer, validate_rule  # noqa: E402


class TestExpertSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads((ROOT / "data/rules.json").read_text(encoding="utf-8"))
        cls.diseases = json.loads((ROOT / "data/diseases.json").read_text(encoding="utf-8"))
        cls.symptoms = json.loads((ROOT / "data/symptoms.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))

    def test_cf_formula(self):
        self.assertAlmostEqual(combine_cf(0.5, 0.4), 0.7, places=3)
        self.assertEqual(combine_cf(0, 0.4), 0.4)
        self.assertEqual(combine_cf(1, 0.4), 1.0)

    def test_cf_is_bounded(self):
        self.assertEqual(combine_cf(-0.5, 0.4), 0.4)
        self.assertEqual(combine_cf(1.5, 0.4), 1.0)

    def test_scenarios(self):
        failures = []
        with (ROOT / "data/test_cases.csv").open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                facts = {x: 1.0 for x in row["symptoms"].split(";") if x}
                out = infer(facts, self.rules, self.diseases)
                actual = out["diagnoses"][0]["id"] if out["diagnoses"] else "NO_DIAGNOSIS"
                if actual != row["expected_diagnosis"]:
                    failures.append(f"{row['case_id']}: expected {row['expected_diagnosis']}, got {actual}")
        self.assertEqual(failures, [])

    def test_reasoning_trace_and_working_memory(self):
        out = infer({"G01": 0.7}, self.rules, self.diseases)
        self.assertEqual(out["trace"][0]["rule_id"], "R01")
        self.assertEqual(out["working_memory"]["fired_rule_ids"], ["R01"])
        self.assertIn("candidate:P01", out["working_memory"]["inferred_facts"])
        self.assertAlmostEqual(out["diagnoses"][0]["cf"], 0.7 * 0.85, places=3)

    def test_multiple_rules_combine_same_diagnosis(self):
        out = infer({"G01": 1.0, "G14": 1.0}, self.rules, self.diseases)
        self.assertEqual([t["rule_id"] for t in out["trace"]], ["R01", "R02"])
        self.assertAlmostEqual(out["diagnoses"][0]["cf"], combine_cf(0.85, 0.9), places=3)

    def test_unknown_or_weak_facts_give_no_diagnosis(self):
        self.assertEqual(infer({"G99": 1.0}, self.rules, self.diseases)["diagnoses"], [])
        # 0.4 x CF 0.5 = 0.2, di bawah ambang 0.25
        self.assertEqual(infer({"G07": 0.4}, [r for r in self.rules if r["id"] == "R05"], self.diseases)["diagnoses"], [])

    def test_dataset_v2_is_complete(self):
        self.assertEqual((len(self.diseases), len(self.symptoms), len(self.rules)), (12, 23, 29))
        used = {s for r in self.rules for s in r["antecedents"]}
        self.assertEqual(used, {s["id"] for s in self.symptoms}, "setiap gejala dipakai minimal satu aturan")

    def test_rule_validation_rejects_invalid_data(self):
        symptom_ids = {s["id"] for s in self.symptoms}
        disease_ids = {d["id"] for d in self.diseases}
        source_ids = {s["source_id"] for s in self.sources}
        bad = {"id": "", "antecedents": ["missing", "missing"], "disease_id": "unknown", "cf": 1.4,
               "description": "", "source_ids": ["unknown-source"]}
        errors = validate_rule(bad, symptom_ids, disease_ids, source_ids)
        self.assertGreaterEqual(len(errors), 5)

    def test_all_existing_rules_have_valid_references(self):
        symptom_ids = {s["id"] for s in self.symptoms}
        disease_ids = {d["id"] for d in self.diseases}
        source_ids = {s["source_id"] for s in self.sources}
        ids = [rule["id"] for rule in self.rules]
        self.assertEqual(len(ids), len(set(ids)), "ID rule harus unik")
        for rule in self.rules:
            self.assertEqual(validate_rule(rule, symptom_ids, disease_ids, source_ids), [], rule["id"])


if __name__ == "__main__":
    unittest.main()
