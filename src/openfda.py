from typing import Optional, Dict, Any, List
import requests

BASE = "https://api.fda.gov/drug/label.json"

def _fetch_label(drug_query: str) -> Optional[Dict[str, Any]]:
    """
    Fetch one representative label for a drug (by generic or brand name).
    Tries generic name, then brand name.
    """
    for field in ("openfda.generic_name", "openfda.brand_name"):
        params = {"search": f'{field}:"{drug_query}"', "limit": 1}
        resp = requests.get(BASE, params=params, timeout=20)
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results") or []
        if results:
            return results[0]
    return None

def get_interaction_text(drug_name: str) -> Dict[str, str]:
    """
    Return label sections relevant to interactions/warnings, if present.
    Keys: drug_interactions, warnings_and_cautions, warnings, precautions
    """
    label = _fetch_label(drug_name)
    sections: Dict[str, str] = {}
    if not label:
        return sections

    for key in ["drug_interactions", "warnings_and_cautions", "warnings", "precautions"]:
        val = label.get(key)
        if isinstance(val, list):
            sections[key] = "\n\n".join(val[:2])
        elif isinstance(val, str):
            sections[key] = val
    return sections

def simple_crosscheck(drug_a: str, drug_b: str) -> List[str]:
    """
    Heuristic: check if drug B is mentioned in drug A's 'drug_interactions' text, and vice versa.
    """
    a_text = get_interaction_text(drug_a).get("drug_interactions", "").lower()
    b_text = get_interaction_text(drug_b).get("drug_interactions", "").lower()
    notes: List[str] = []
    if a_text and drug_b.lower() in a_text:
        notes.append(f"Label for {drug_a} mentions {drug_b} in 'Drug Interactions'.")
    if b_text and drug_a.lower() in b_text:
        notes.append(f"Label for {drug_b} mentions {drug_a} in 'Drug Interactions'.")
    return notes
