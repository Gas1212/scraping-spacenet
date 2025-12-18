# Spacenet Scraper

Spider Scrapy pour extraire les données des produits du site spacenet.tn

## Description

Ce projet utilise Scrapy pour scraper les produits du site spacenet.tn à partir des sitemaps XML. Il extrait les informations suivantes pour chaque produit en stock :

- URL du produit
- Titre
- Marque
- Prix actuel et ancien prix
- Remise
- Référence
- Image du produit
- Fiche technique
- État du stock
- Catégorie et chemin de catégorie
- Date d'identification

## Installation locale

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
scrapy crawl scraper -o products.json
```

## Docker

### Construire l'image

```bash
docker build -t spacenet-scraper .
```

### Exécuter le conteneur

```bash
docker run -v $(pwd)/data:/app/data spacenet-scraper
```

## Déploiement sur Railway

### 🚀 Guide rapide
Consultez [QUICK_START.md](QUICK_START.md) pour un déploiement en 3 étapes simples.

### 📚 Documentation complète
Pour plus de détails sur le déploiement, les options de stockage et le monitoring, consultez [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md).

### Résumé des étapes :
1. Connectez-vous à [Railway](https://railway.app)
2. Créez un nouveau projet
3. Connectez votre dépôt GitHub
4. Railway détectera automatiquement le Dockerfile
5. Le spider s'exécutera automatiquement lors du déploiement

## Configuration

Les sitemaps utilisés sont configurés dans le fichier `spacenet/spiders/scraper.py` :

- http://spacenet.tn/sitemap/sitemap-products-1.xml
- http://spacenet.tn/sitemap/sitemap-products-2.xml
- http://spacenet.tn/sitemap/sitemap-products-3.xml

## Paramètres personnalisés

- **DOWNLOAD_DELAY**: 0.5 seconde entre chaque requête
- **CONCURRENT_REQUESTS_PER_DOMAIN**: 4 requêtes simultanées maximum
- **FEED_EXPORT_ENCODING**: UTF-8

## Filtre

Le spider ne garde que les produits **en stock** et ignore ceux qui sont "Sur commande".
