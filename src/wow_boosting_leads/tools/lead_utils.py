import json
import os
from typing import List, Dict

# Dynamically resolve PROJECT_ROOT to the wow_boosting_leads project directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LEADS_FILE = os.path.join(PROJECT_ROOT, "wow_leads.json")

def load_existing_leads() -> List[Dict]:
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_leads(leads: List[Dict]):
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

def is_duplicate(new_lead: Dict, existing: List[Dict]) -> bool:
    """Deduplicate by URL or username"""
    new_url = new_lead.get("url") or new_lead.get("jump_url")
    new_user = new_lead.get("author") or new_lead.get("username")
    
    for old in existing:
        old_url = old.get("url") or old.get("jump_url")
        old_user = old.get("author") or old.get("username")
        if (new_url and new_url == old_url) or (new_user and new_user.lower() == old_user.lower()):
            return True
    return False
