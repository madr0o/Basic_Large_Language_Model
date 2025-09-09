import csv
from typing import Optional, Tuple
from rapidfuzz import process, fuzz

def load_animal_catalog(path: str):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                "name": row["name"].strip(),
                "scientific_name": row["scientific_name"].strip(),
            })
        return items
    
def resolve_animal_name(user_text: str, catalog) -> Optional[Tuple[str, str, float]]:
    choices = [c["name"] for c in catalog]
    match, score, idx = process.extractOne(
        user_text.strip().lower(),
        choices,
        scorer=fuzz.WRatio
    ) or (None, 0, None)

    if match is None or idx is None:
        return None
    
    rec = catalog[idx]
    return rec["name"], rec["scientific_name"], score

def is_valid_animal(user_text: str, catalog, treshold: int=70):
    found = resolve_animal_name(user_text, catalog)
    if not found:
        return None
    common, sci, score = found
    if score >= treshold:
        return {"name": common, "scientific_name": sci, "score": score}
    return None