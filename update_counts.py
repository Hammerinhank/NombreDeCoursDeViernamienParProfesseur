import json
from playwright.sync_api import sync_playwright

tutors = [
    {"name": "QUYNH", "url": "https://preply.com/fr/tuteur/3555405"},
    {"name": "CHI",   "url": "https://preply.com/fr/tuteur/3788757"},
    {"name": "MAI",   "url": "https://preply.com/fr/tuteur/5826353"},
    {"name": "HUONG", "url": "https://preply.com/fr/tuteur/5590437"},
    {"name": "THU",   "url": "https://preply.com/fr/tuteur/6100757"},
    {"name": "XUAN",  "url": "https://preply.com/fr/tuteur/6471628"},
    {"name": "LINH",  "url": "https://preply.com/fr/tuteur/3621179"},
    {"name": "TRAN",  "url": "https://preply.com/fr/tuteur/5501608"},
    {"name": "TRANG", "url": "https://preply.com/fr/tuteur/6246579"},
    {"name": "YEN",   "url": "https://preply.com/fr/tuteur/7303777"},
]

def get_counts():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0")
        for tutor in tutors:
            try:
                page = context.new_page()
                page.goto(tutor["url"], timeout=60000)
                page.wait_for_load_state("networkidle")
                # On cherche le chiffre dans le texte de la page
                content = page.content()
                import re
                match = re.search(r'"totalLessons":\s*(\d+)', content)
                count = match.group(1) if match else "Non trouvé"
                results.append({"name": tutor["name"], "count": count})
                page.close()
            except Exception as e:
                results.append({"name": tutor["name"], "count": "Erreur"})
        browser.close()
    return results

if __name__ == "__main__":
    data = get_counts()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
