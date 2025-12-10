import os

import pandas as pd
import requests
from bs4 import BeautifulSoup



def word_to_nbr(word) -> float | None:
    match word.lower():
        case "zero":
            return 0
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case _:
            print(f"\nError: no equivalent number to {word}")
            return None

def download_image(image_url, save_path):
    response = requests.get(image_url)
    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)


def main():
    base_url = "http://books.toscrape.com"

    # ======= 1. Récupérer la page d'accueil
    print("# ======= 1. Récupérer la page d'accueil")
    response = requests.get(base_url)
    # print(response.text)

    # ======= 2. Pour chaque livre sur la page, extraire :
    # Titre
    # Prix (convertir en float)
    # Note (étoiles → nombre)
    # Disponibilité (In stock / Out of stock)
    # URL de l'image
    print("\n# ======= 2. Pour chaque livre sur la page, extraire")

    titles = []
    prices = []
    ratings = []
    availabilities = []
    img_urls = []

    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("article", class_="product_pod")
    # print(articles)
    for article in articles:
        # title
        h3 = article.find("h3")
        titles.append(h3.find("a").get("title"))
        # price
        div_price = article.find("div", class_="product_price")
        prices.append(float(div_price.find("p").text.strip('Â £')))
        # ratings (étoiles → nombre)
        p_rating = article.find("p", class_="star-rating")
        class_rating = p_rating.get("class")[1]
        ratings.append(word_to_nbr(class_rating))
        # availability (In stock / Out of stock)
        p_availability = div_price.find("p", class_="availability")
        availabilities.append(p_availability.text.strip())
        # URL of the image
        div_img = article.find("div", class_="image_container")
        img_urls.append(div_img.find("img").get("src").strip())

    # ======= 3. Créer un DataFrame Pandas
    print("\n# ======= 3. Créer un DataFrame Pandas")
    data = {
        "title": titles,
        "price": prices,
        "rating": ratings,
        "availability": availabilities,
        "img_url": img_urls
    }
    df = pd.DataFrame(data)
    print(df)

    # ======= 4. Calculer :
    print("\n# ======= 4. Calculer :")
    # Prix moyen
    average_price = df["price"].mean()
    print("average_price = ", average_price)
    # Livre le plus cher
    high_price = df["price"].max()
    print("high_price = ", high_price)
    # Livre le moins cher
    less_price = df["price"].min()
    print("less_price = ", less_price)
    # Répartition par note
    titles_by_rating = df.groupby("rating")["title"].apply(list)
    print(titles_by_rating)

    # ======= 5. Sauvegarder dans books.csv
    df.to_csv("./data/output/books.csv", index=False)

    # ======= 6. Bonus : Télécharger l'image du livre le plus cher
    # get url of the most expensive book
    # url_expensive_book = df
    most_expensive = df[df["price"] == high_price]
    print(most_expensive)
    url_expensive_book = base_url + "/" + most_expensive["img_url"].iloc[0]
    # print("url_expensive_book = ", url_expensive_book)

    if url_expensive_book:
        save_path = "./data/output/image_expensive_book.jpg"
        print("[INFO] Téléchargement de la première image :")
        print(" URL :", url_expensive_book)
        print(" Chemin local :", save_path)
        download_image(url_expensive_book, save_path)
        print("[OK] Téléchargement terminé.")
    else:
        print("[3] Aucune image à télécharger.")







if __name__ == "__main__":
    main()