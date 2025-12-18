import scrapy
from scrapy.http import XmlResponse
import re
from datetime import datetime
import unicodedata

class SpacenetSitemapSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["spacenet.tn"]

    # URLs des sitemaps de produits
    sitemap_urls = [
        "http://spacenet.tn/sitemap/sitemap-products-1.xml",
        "http://spacenet.tn/sitemap/sitemap-products-2.xml",
        "http://spacenet.tn/sitemap/sitemap-products-3.xml",
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_found_urls = 0
        self.products_in_stock = 0

    def normalize_category(self, text):
        """Normalise les noms de catégorie : supprime accents, caractères spéciaux, espaces -> tirets"""
        if not text:
            return ""
        # Normalise les caractères Unicode (décompose les accents)
        text = unicodedata.normalize('NFKD', text)
        # Garde seulement les caractères alphanumériques et espaces, convertit en minuscules
        text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
        # Remplace les espaces par des tirets
        return text.replace(' ', '-')

    def start_requests(self):
        for sitemap_url in self.sitemap_urls:
            yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response: XmlResponse):
        urls = response.xpath(
            '//x:urlset/x:url/x:loc/text()',
            namespaces={'x': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        ).getall()

        self.logger.info(f"🗺️ {len(urls)} URLs trouvées dans : {response.url}")
        self.total_found_urls += len(urls)

        for product_url in urls:
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        self.logger.info(f"🔍 Scraping produit : {response.url}")

        title = response.css("h1.h1::text").get()

        # Extraction de la marque depuis l'attribut alt
        brand = response.css('div.product-manufacturer img::attr(alt)').get()
        brand = brand.strip() if brand else "Non définie"

        def clean_price(text):
            if not text:
                return 0.0
            cleaned = re.sub(r'[^\d.,]', '', text)
            if '.' in cleaned:
                cleaned = cleaned.replace(',', '')
            elif ',' in cleaned:
                cleaned = cleaned.replace(',', '.')
            try:
                return float(cleaned)
            except ValueError:
                return 0.0

        # Prix actuel
        price_text = response.css("div.current-price span::attr(content)").get()
        if not price_text:
            self.logger.info(f"❌ Pas de prix trouvé — produit ignoré : {response.url}")
            return
        price = clean_price(price_text)

        # Ancien prix
        old_price_texts = response.css("div.product-discount span.regular-price::text").getall()
        old_price = clean_price(old_price_texts[0]) if old_price_texts else price

        # Remise
        discount = old_price - price

        # Fiche technique
        fiche_technique = ' '.join(response.css('div.product-des p *::text').getall()).strip()

        # État global du stock
        etat_global = "Sur commande"
        for bloc in response.css("div.magasin-table div.table-bloc"):
            dispo = bloc.css("div.right-side span::text").get()
            if dispo and "Disponible" in dispo:
                etat_global = "En stock"
                break
        etat_stock = etat_global

        # FILTRE : Ignorer les produits qui ne sont pas en stock
        if etat_stock != "En stock":
            self.logger.info(f"❌ Produit non en stock ({etat_stock}) — ignoré : {response.url}")
            return

        # Breadcrumb pour catégorie
        breadcrumb_items = response.css('div.breadcrumb-no-images nav.breadcrumb ol li')
        categories_with_name = [
            (li.css('a span::text').get() or li.css('span::text').get() or '').strip()
            for li in breadcrumb_items
        ]
        categories_with_name = [c for c in categories_with_name if c]  # filtrer les vides

        # Catégorie principale = avant-dernier élément
        category_main = categories_with_name[-2] if len(categories_with_name) >= 2 else "Non définie"
        
        # Normalisation SEULEMENT de la catégorie
        normalized_category = self.normalize_category(category_main)

        # Chemin complet
        category_path = " > ".join(categories_with_name[:-1]) if categories_with_name else "Non définie"

        # Date
        identification_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")

        item = {
            "url": response.url,
            "title": title.strip() if title else "",
            "brand": brand,
            "price": price,
            "old_price": old_price,
            "discount": discount,
            "reference": response.css("div.product-reference span::text").get() or "",
            "product_image": response.urljoin(response.css('div.product-cover img::attr(src)').get() or ""),
            "fiche_technique": fiche_technique,
            "etat_stock": etat_stock,
            "category": normalized_category,  # Seulement ce champ est normalisé
            "category_path": category_path,
            "identification_date": identification_date
        }

        self.products_in_stock += 1
        yield item

    def closed(self, reason):
        self.logger.info(f"✅ Spider terminé. Total URLs trouvées : {self.total_found_urls}, Produits en stock : {self.products_in_stock}")