import pandas as pd
import requests
from requests import Timeout
import time

headers = {
    'User-Agent': 'My Scraper 1.0',
}


def fetch_page(url, timeout=10):
    """Récupère une page avec gestion d'erreurs."""
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout
        )
        # Lève une exception si le code HTTP est 4xx ou 5xx
        response.raise_for_status()
        return response.text

    except Timeout:
        print(f"Timeout pour {url}")
        return None

    except ConnectionError:
        print(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        print(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        print(f"Erreur générale: {e}")
        return None

def scrape_pages(base_url: str, page_nbr_max: int, page_nbr_min: int = 1):

    # from bs4 import BeautifulSoup


    # Liste des pages à scraper
    # pages = [f"{base_url}page-{i}" for i in range(1, 4)]
    pages = [f"{base_url}/page/{i}" for i in range(page_nbr_min, page_nbr_max)]

    # En-têtes pour simuler un navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Liste pour stocker les résultats
    results = []

    for page_url in pages:
        try:
            html_page = fetch_page(page_url, timeout=10)

            results.append(html_page)
            # Délai pour éviter de surcharger le serveur
            time.sleep(2)

        except Exception as e:
            print(f"Erreur lors de la récupération de {page_url} : {e}")

    return results

def count_char(text: str):
    """Retourne les charactes d'un texte."""
    return len(text)


def save_page_to_html(page: str, filename):
    """sauvegarde une page web dans un fichier HTML."""
    try:
        # response = requests.get(url)
        # response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        #
        # soup = BeautifulSoup(response.content, "html.parser")

        # Écrire le contenu HTML dans le fichier
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page)

        print(f"Page sauvegardée avec succès dans : {filename}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {url} : {e}")

def generate_report(base_url: str, num_pages_to_scrap: int, output_filename: str):
    data = []

    for i in range(1, num_pages_to_scrap + 1):
        page_url = f"{base_url}/page/{i}"
        start_time = time.time()
        try:
            response = requests.get(page_url)
            status_code = response.status_code
            content_size = len(response.content)
            end_time = time.time()
            response_time = end_time - start_time

            data.append([page_url, status_code, content_size, response_time])

        except Exception as e:
            data.append([page_url, "Erreur", 0, 0])

    df = pd.DataFrame(data, columns=["URL", "Statut HTTP", "Taille (octets)", "Temps de réponse (s)"])

    df.to_csv(output_filename, encoding="utf-8", index=False)

    print(f"Rapport généré avec succès : {output_filename}")


def main():
    BASE_URL = "http://quotes.toscrape.com"
    # === 1. Créer une fonction fetch_page(url) avec gestion d'erreurs
    print(fetch_page(BASE_URL))

    # === 2. Scraper les 3 premières pages du site
    # &
    # === 3. Pour chaque page, extraire le HTML brut
    pages = scrape_pages(BASE_URL, 4, 1)
    for page in pages:
        print("# ============= Page =============")
        print(page)

    # === 4. Compter le nombre de caractères de chaque page
    print(f"\nnbre de char de la page 1 : {count_char(pages[0])}") #
    print(f"\nnbre de char de la page 2 : {count_char(pages[1])}") #
    print(f"\nnbre de char de la page 3 : {count_char(pages[2])}") #

    # === 5. Sauvegarder chaque page dans un fichier HTML
    html_file_1 = "./save_files/page1.html"
    html_file_2 = "./save_files/page2.html"
    html_file_3 = "./save_files/page3.html"
    save_page_to_html(pages[0], html_file_1)
    save_page_to_html(pages[1], html_file_2)
    save_page_to_html(pages[2], html_file_3)

    # === 6. Créer un rapport CSV avec :
    # URL de la page
    # Statut HTTP
    # Taille en octets
    # Temps de réponse

    generate_report(BASE_URL,3, "./save_files/report.csv")



if __name__ == "__main__":
    main()