"""Penyimpanan data JSON dan riwayat konsultasi CSV."""
import csv, json
from datetime import datetime
from pathlib import Path

def load_json(path):
    with Path(path).open(encoding="utf-8") as f: return json.load(f)

def save_json(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def append_history(path, facts, result):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    fields = ["timestamp","known_facts","diagnoses","rules_used"]
    with path.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists: w.writeheader()
        w.writerow({"timestamp":datetime.now().isoformat(timespec="seconds"),
          "known_facts":json.dumps(facts,ensure_ascii=False),
          "diagnoses":json.dumps([{"id":d["id"],"name":d["name"],"cf":d["cf"]} for d in result.get("diagnoses",[])],ensure_ascii=False),
          "rules_used":json.dumps(result.get("working_memory",{}).get("fired_rule_ids",[]),ensure_ascii=False)})

def read_history(path):
    path=Path(path)
    if not path.exists(): return []
    with path.open("r",newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
