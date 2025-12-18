# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Créer le répertoire pour les données exportées
RUN mkdir -p /app/data

# Commande par défaut pour exécuter le spider
CMD ["scrapy", "crawl", "scraper", "-o", "/app/data/products.json"]
