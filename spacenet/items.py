import scrapy

class SpacenetItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    reference = scrapy.Field()  # Laisser tel quel pour éviter erreurs de type
    product_image = scrapy.Field()
    fiche_technique = scrapy.Field()

    # Champs dynamiques à mettre à jour régulièrement
    price = scrapy.Field()
    old_price = scrapy.Field()
    discount = scrapy.Field()
    identification_date = scrapy.Field()
    etat_stock = scrapy.Field()

    # Nouveaux champs
    brand = scrapy.Field()       # Marque du produit
    category = scrapy.Field()    # Catégorie principale
    category_path = scrapy.Field()  # Chemin complet des catégories (optionnel)
