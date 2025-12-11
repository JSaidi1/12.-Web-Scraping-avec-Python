import scrapy

from bookstore.items import BookstoreItem


class BooksSpider(scrapy.Spider):
    name = "books_items_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com"]

    def parse(self, response):
        # title, price, rating, availability
        articles = response.css("article.product_pod")

        for article in articles:
            item = BookstoreItem()
            item['title'] = article.css("a::text").get()
            item['price'] = article.css("p.price_color::text").get()
            item['rating'] = article.css('p::attr(class)').get(default='').split()[1]
            item['availability'] = article.xpath(
                'normalize-space(.//p[@class="instock availability"]/text()[2])'
            ).get()

            yield item


