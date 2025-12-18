# Guide de déploiement sur Railway

## Prérequis

- Un compte GitHub avec le dépôt https://github.com/Gas1212/scraping-spacenet.git
- Un compte Railway (gratuit) sur https://railway.app

## Étapes de déploiement

### 1. Connexion à Railway

1. Allez sur https://railway.app
2. Cliquez sur "Login" et connectez-vous avec votre compte GitHub
3. Autorisez Railway à accéder à vos dépôts GitHub

### 2. Créer un nouveau projet

1. Cliquez sur "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Choisissez le dépôt `Gas1212/scraping-spacenet`
4. Railway détectera automatiquement le Dockerfile

### 3. Configuration du projet

Railway va automatiquement :
- Détecter le `Dockerfile`
- Construire l'image Docker
- Déployer le conteneur

### 4. Configuration des variables d'environnement (optionnel)

Si vous souhaitez ajouter des variables d'environnement :

1. Allez dans l'onglet "Variables"
2. Ajoutez vos variables si nécessaire (pour l'instant, aucune n'est requise)

### 5. Déploiement

Le déploiement se fait automatiquement. Railway va :
1. Cloner le dépôt
2. Construire l'image Docker avec le Dockerfile
3. Exécuter le conteneur
4. Lancer le spider automatiquement

### 6. Vérifier les logs

1. Allez dans l'onglet "Deployments"
2. Cliquez sur le déploiement actif
3. Consultez les logs pour voir la progression du scraping

### 7. Récupérer les données

Les données seront exportées dans `/app/data/products.json` à l'intérieur du conteneur.

Pour récupérer les données, vous pouvez :

**Option 1 : Modifier le spider pour envoyer les données ailleurs**
- Ajoutez un pipeline pour envoyer les données vers une base de données
- Utilisez une API pour stocker les données
- Envoyez les données vers un service de stockage cloud (S3, etc.)

**Option 2 : Utiliser Railway avec un volume persistant**
1. Dans Railway, allez dans "Settings"
2. Ajoutez un volume pour persister `/app/data`

## Configuration pour exécution programmée (Cron)

Railway ne supporte pas nativement les cron jobs, mais vous pouvez :

### Option 1 : Utiliser un service externe
- Utilisez https://cron-job.org
- Configurez un webhook qui déclenche le déploiement

### Option 2 : Modifier le Dockerfile pour une exécution continue

Créez un script qui boucle avec un délai :

```dockerfile
# Ajouter dans le Dockerfile
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]
```

Et créez `run.sh` :

```bash
#!/bin/bash
while true; do
    scrapy crawl scraper -o /app/data/products_$(date +%Y%m%d_%H%M%S).json
    sleep 86400  # Attendre 24 heures
done
```

## Stockage des données recommandé

Pour un scraper en production, il est recommandé d'utiliser :

### Option 1 : Base de données PostgreSQL
1. Ajoutez un service PostgreSQL dans Railway
2. Créez un pipeline Scrapy pour stocker dans PostgreSQL
3. Railway fournit automatiquement les variables d'environnement de connexion

### Option 2 : MongoDB
1. Ajoutez MongoDB via Railway ou utilisez MongoDB Atlas
2. Configurez le pipeline Scrapy pour MongoDB

### Option 3 : API externe
1. Créez une API qui reçoit les données
2. Utilisez un pipeline pour envoyer les données via HTTP

## Surveillance et monitoring

1. Consultez les logs dans Railway pour le debugging
2. Configurez des alertes en cas d'échec
3. Utilisez les métriques Railway pour surveiller l'utilisation des ressources

## Coûts

- Railway offre un plan gratuit avec $5 de crédits par mois
- Le scraping peut consommer des ressources, surveillez votre utilisation
- Optimisez les paramètres `DOWNLOAD_DELAY` et `CONCURRENT_REQUESTS` si nécessaire

## Troubleshooting

### Le déploiement échoue
- Vérifiez les logs de build
- Assurez-vous que le Dockerfile est correct
- Vérifiez que requirements.txt contient toutes les dépendances

### Le spider ne trouve pas de produits
- Vérifiez que les URLs des sitemaps sont accessibles
- Consultez les logs pour voir les erreurs de scraping
- Testez localement d'abord

### Problèmes de mémoire
- Réduisez `CONCURRENT_REQUESTS_PER_DOMAIN`
- Augmentez `DOWNLOAD_DELAY`
- Passez à un plan Railway avec plus de ressources

## Support

Pour toute question, consultez :
- Documentation Railway : https://docs.railway.app
- Documentation Scrapy : https://docs.scrapy.org
