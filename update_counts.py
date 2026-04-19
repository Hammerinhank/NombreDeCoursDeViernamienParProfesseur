import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

tutors_list = ["QUYNH", "CHI", "MAI", "HUONG", "THU", "XUAN", "LINH", "TRAN", "TRANG", "YEN"]
urls = {
    "QUYNH": "https://preply.com/fr/tuteur/3555405",
    "CHI": "https://preply.com/fr/tuteur/3788757",
    "MAI": "https://preply.com/fr/tuteur/5826353",
    "HUONG": "https://preply.com/fr/tuteur/5590437",
    "THU": "https://preply.com/fr/tuteur/6100757",
    "XUAN": "https://preply.com/fr/tuteur/6471628",
    "LINH": "https://preply.com/fr/tuteur/3621179",
    "TRAN": "https://preply.com/fr/tuteur/5501608",
    "TRANG": "https://preply.com/fr/tuteur/6246579",
    "YEN": "https://preply.com/fr/tuteur/7303777"
}

def fetch_data():
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = {"date": today, "counts": {}}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0")
        for name in tutors_list:
            try:
                page = context.new_page()
                page.goto(urls[name], timeout=60000)
                content = page.content()
                import re
                match = re.search(r'"totalLessons":\s*(\d+)', content)
                new_entry["counts"][name] = int(match.group(1)) if match else None
                page.close()
            except:
                new_entry["counts"][name] = None
        browser.close()
    return new_entry

if __name__ == "__main__":
    history_file = "history.json"
    
    # Charger l'historique existant ou créer une liste vide
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    # Ajouter les données du jour
    new_data = fetch_data()

    # Ajoutez ces 3 lignes ici :
    print("--- DIAGNOSTIC DATA ---")
    print(new_data)
    print("-----------------------")
    
    # Éviter les doublons si le script tourne deux fois le même jour
    history = [entry for entry in history if entry['date'] != new_data['date']]
    history.append(new_data)
    
    # Garder seulement les 40 derniers mois pour ne pas alourdir (environ 1200 entrées)
    history = history[-1200:]

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
