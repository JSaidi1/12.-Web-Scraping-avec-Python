import scrapy
from ecommerce_scraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """Extraire toutes les catégories depuis la page d'accueil"""
        categories = response.css('div.side_categories ul.nav li ul li a::attr(href)').getall()
        for cat in categories:
            yield response.follow(cat, callback=self.parse_category)

    def parse_category(self, response):
        """Extraire les livres d'une page de catégorie et gérer la pagination"""
        books = response.css('article.product_pod h3 a::attr(href)').getall()
        for book in books:
            yield response.follow(book, callback=self.parse_book)

        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)

    def parse_book(self, response):
        """Extraire les détails d'un livre"""
        item = BookItem()
        item['title'] = response.css('div.product_main h1::text').get()
        item['price'] = response.css('p.price_color::text').get()
        item['rating'] = response.css('p.star-rating').attrib['class'].split()[1]
        item['description'] = response.css('#product_description ~ p::text').get(default='').strip()
        # La catégorie est la 3ème dans le fil d'ariane (Home > Books > Category)
        item['category'] = response.css('ul.breadcrumb li a::text').getall()[2].strip()
        # Nombre d'avis
        item['review_count'] = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').get()
        item['image_url'] = response.urljoin(response.css('div.carousel img::attr(src)').get())
        yield item
