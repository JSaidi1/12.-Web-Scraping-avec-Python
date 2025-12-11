import scrapy

from bookstore.items import BookstoreItem


class BooksPaginationSpider(scrapy.Spider):
    name = "books_pagination_spider"
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

        next_page = response.css("li.next a::attr(href)").get()

        # Pagination limitée à 3 pages
        page_num = response.meta.get("page_num", 1)  # page actuelle
        if page_num < 3:  # limite à 3 pages
            if next_page:
                yield response.follow(next_page, callback=self.parse, meta={"page_num": page_num + 1})
