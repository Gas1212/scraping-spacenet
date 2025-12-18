#!/bin/bash

# Script pour exécuter le scraper de manière programmée
# Peut être utilisé avec Railway pour des exécutions répétées

echo "=== Démarrage du scraper Spacenet ==="
echo "Date: $(date)"

# Créer le nom de fichier avec timestamp
OUTPUT_FILE="/app/data/products_$(date +%Y%m%d_%H%M%S).json"

# Exécuter le spider
scrapy crawl scraper -o "$OUTPUT_FILE"

# Vérifier si le scraping a réussi
if [ $? -eq 0 ]; then
    echo "=== Scraping terminé avec succès ==="
    echo "Fichier généré: $OUTPUT_FILE"
else
    echo "=== Erreur lors du scraping ==="
    exit 1
fi

# Si vous voulez exécuter en boucle (décommentez ci-dessous)
# while true; do
#     echo "=== Démarrage du scraper Spacenet ==="
#     echo "Date: $(date)"
#     OUTPUT_FILE="/app/data/products_$(date +%Y%m%d_%H%M%S).json"
#     scrapy crawl scraper -o "$OUTPUT_FILE"
#     echo "=== Attente de 24 heures avant la prochaine exécution ==="
#     sleep 86400  # 24 heures
# done
