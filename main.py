# Exercice : Récupérer et analyser une page web
# Site : http://quotes.toscrape.com (site d'entraînement)
#
# Tâches
#








import requests


def main():
    BASE_URL = "http://quotes.toscrape.com"
    ROBOTS_URL = f"{BASE_URL}/robots.txt"

    # 1. Récupérer la page d'accueil avec Requests
    response = requests.get(BASE_URL)
    html = response.text
    print(html)

    # 2. Afficher le code de statut
    print("Code HTTP :", response.status_code)  # 200 = OK

    # 3. Afficher les 500 premiers caractères du HTML
    print("\n=== Aperçu du HTML (500 premiers caractères) ===")
    print(html[:500])

    # 4. Vérifier l'encodage de la page
    print("\nEncodage détecté :", response.encoding)

    # 5. Afficher les headers de la réponse
    # Headers de la réponse (métadonnées HTTP)
    print("\n=== Headers de la réponse ===")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    # 6. Récupérer le robots.txt du site
    def afficher_robots_txt():
        """Télécharge et affiche le contenu de robots.txt."""
        print(f"Récupération de {ROBOTS_URL} ...")
        response = requests.get(ROBOTS_URL)

        # Status HTTP (200 = OK, 404 = non trouvé, etc.)
        print("Code HTTP :", response.status_code)

        # Affichage brut du fichier robots.txt
        print("\n=== Contenu de robots.txt ===")
        print(response.text)

    afficher_robots_txt()

    # 7. Bonus : Utiliser une session pour faire 3 requêtes successives
    # Créer une session
    session = requests.Session()

    # Les cookies et headers sont persistés d'une requête à l'autre
    session.headers.update({'User-Agent': 'My Scraper 1.0'})

    # Première requête (authentification par exemple)
    # Les paramètres username/password sont purement fictifs ici.
    response1 = session.post(
        # 'https://httpbin.org/post',
        f'{BASE_URL}/post',
        data={'username': 'user', 'password': 'pass'}
    )

    print("Code HTTP de la tentative de login :", response1.status_code)

    # Requêtes suivantes gardent les cookies de la session
    # response2 = session.get('https://httpbin.org/cookies/set?session_id=12345')
    # response3 = session.get('https://httpbin.org/cookies')

    response2 = session.get(f'{BASE_URL}/cookies/set?session_id=12345')
    response3 = session.get(f'{BASE_URL}/cookies')

    print("\nCode HTTP /session_id :", response2.status_code)
    print("Code HTTP /cookies  :", response3.status_code)

    # Voir les cookies stockés dans la session
    print("\n=== Cookies de la session ===")
    print(session.cookies.get_dict())

    # Fermer la session proprement (bonne pratique)
    session.close()


if __name__ == "__main__":
    main()