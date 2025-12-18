# Quick Start - Déploiement Railway

## 🚀 Déploiement en 3 étapes

### Étape 1 : Accéder à Railway
1. Allez sur https://railway.app
2. Connectez-vous avec votre compte GitHub

### Étape 2 : Créer le projet
1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez le dépôt : `Gas1212/scraping-spacenet`

### Étape 3 : Déployer
Railway va automatiquement :
- ✅ Détecter le Dockerfile
- ✅ Construire l'image
- ✅ Déployer le conteneur
- ✅ Lancer le scraper

## 📊 Vérifier le déploiement

1. Dans Railway, allez dans **"Deployments"**
2. Cliquez sur le déploiement actif
3. Consultez les **logs** pour voir :
   - Le nombre d'URLs trouvées dans les sitemaps
   - La progression du scraping
   - Le nombre de produits en stock extraits

## 📦 Récupérer les données

Les données sont exportées en JSON dans `/app/data/products.json`

### Pour persister les données (recommandé) :

**Option A : Ajouter une base de données PostgreSQL**
1. Dans Railway, cliquez sur **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway connectera automatiquement la base
3. Modifiez le spider pour utiliser un pipeline PostgreSQL

**Option B : Ajouter un volume**
1. Dans Settings → Add Volume
2. Mount path : `/app/data`

## ⚙️ Configuration actuelle

- **Sitemaps scrapés** : 3 fichiers XML
  - sitemap-products-1.xml
  - sitemap-products-2.xml
  - sitemap-products-3.xml

- **Données extraites** :
  - URL, titre, marque
  - Prix actuel et ancien prix
  - Référence, image
  - Fiche technique
  - État du stock
  - Catégories

- **Filtre** : Uniquement les produits **en stock**

## 🔄 Automatiser l'exécution

Pour exécuter le scraper régulièrement, consultez le fichier [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) pour les options avancées.

## 📚 Documentation complète

- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Guide complet de déploiement
- [README.md](README.md) - Documentation du projet

## 🆘 Besoin d'aide ?

Consultez les logs dans Railway pour voir les détails de l'exécution et les éventuelles erreurs.
