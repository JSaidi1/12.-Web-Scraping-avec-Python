import requests
from bs4 import BeautifulSoup
import json

# ======= 1. Récupérer la page d'accueil
url = "http://quotes.toscrape.com"
response = requests.get(url)

# Vérification
if response.status_code != 200:
    print("Erreur de chargement :", response.status_code)
else:
    print("Page récupérée avec succès !")

# ======= 2. Parser avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# ======= 3. Trouver toutes les citations (class="quote")
quotes = soup.find_all("div", class_="quote")

# ======= 7. Créer une liste pour stocker les données
data = []

# ======= 4. Extraire les informations pour chaque citation
for q in quotes:
    text = q.find("span", class_="text").get_text(strip=True)
    author = q.find("small", class_="author").get_text(strip=True)
    tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]
    data.append({
        "texte": text,
        "auteur": author,
        "tags": tags
    })

# ======= 5. Afficher les 5 premières citations
print("\n--- 5 premières citations ---")
for item in data[:5]:
    print(f"\nCitation : {item['texte']}")
    print(f"Auteur : {item['auteur']}")
    print(f"Tags : {item['tags']}")

# ======= 6. Compter le nombre total de citations
print("\nNombre total de citations trouvées :", len(data))

# ======= 8. Bonus : sauvegarder dans un fichier JSON
with open("./save_files/citations.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)