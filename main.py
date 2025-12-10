import random
import time
from wsgiref import headers

import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def get_nbr_of_pages(url: str) -> int:
    nbr_page = 1

    while True:
        end_point = f"/page/{nbr_page}"

        soup = BeautifulSoup(fetch_page(url + end_point), "lxml")
        time_to_sleep = random.uniform(1, 3)
        # time.sleep(time_to_sleep)
        # print("time.sleep = ", time_to_sleep)
        li_next_page = soup.find("li", class_="next")
        # print(li_next_page)

        if li_next_page is None:
            break

        nbr_page += 1

    return nbr_page

def scrape_pages(url: str, path_page: str, nbr_page: int) -> list:
    scraped_pages = []

    for i in range(1, nbr_page + 1):
        url_full = url + path_page + str(i)
        scraped_pages.append(BeautifulSoup(fetch_page(url_full), "lxml"))

    return scraped_pages

def main():
    base_url = "http://quotes.toscrape.com"
    home_page = fetch_page(base_url)
    # print(f"=========== home_page =========== \n{home_page}")

    # ===== 1.Détecte automatiquement le nombre de pages
    nbr_of_pages = get_nbr_of_pages(base_url)
    print(nbr_of_pages)
    #&
    # ===== 2. Scrape toutes les pages (jusqu'à 10 max)
    pages_scraped = scrape_pages(base_url, "/page/", nbr_of_pages) # list
    # print(pages_scraped)

    # ===== 3. Pour chaque citation, extrait :
    texts = []
    authors = []
    tags_global = []
    tags_page = []

    # Texte
    # Auteur
    # Tags
    # URL de l'auteur
    for page in pages_scraped:

        # Texte
        span_citation = page.find("span", class_="text")
        texts.append(span_citation.text)
        # Auteur
        small_author = page.find("small", class_="author")
        authors.append(small_author.text)
        # Tags
        # a_tags = page.findAll("a", class_="tag")
        # for a_tag in a_tags:
        #     tags.append(a_tag.text)
        # tags_global.append(tags)
        div_quotes = page.findAll("div", class_="quote")
        tags_quote = []
        for quote in div_quotes:
            tags_quote = []

            a_tags = quote.findAll("a", class_="tag")
            for a_tag in a_tags:
                tags_quote.append(a_tag.text)

            tags_quote = tags_quote.append(tags_quote)
            # print(tags_quote)
            # break
        # break
        tags_page.append(tags_quote)

    print(tags_page)
















if __name__ == "__main__":
    main()