import pymongo

class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Forcer la référence en string
        if 'reference' in item and item['reference'] is not None:
            item['reference'] = str(item['reference'])

        # Champs dynamiques à mettre à jour à chaque scraping
        update_fields = {
            "price": item.get("price", 0.0),
            "old_price": item.get("old_price", 0.0),
            "discount": item.get("discount", 0.0),
            "etat_stock": item.get("etat_stock", "Sur commande"),
            "identification_date": item.get("identification_date"),
            "product_image": item.get("product_image") or "",
            "category": item.get("category") or "",
            "brand": item.get("brand") or "",  # ✅ marque ajoutée
            "category_path": item.get("category_path") or "Non définie"  # ✅ MAJ chemin
        }

        # Champs statiques à conserver si nouvel item
        static_fields = {
            "title": item.get("title") or "",
            "reference": item.get("reference") or "",
            "fiche_technique": item.get("fiche_technique") or "",
        }

        # Upsert dans MongoDB
        self.collection.update_one(
            {"url": item["url"]},
            {
                "$set": update_fields,
                "$setOnInsert": static_fields
            },
            upsert=True
        )

        return item
