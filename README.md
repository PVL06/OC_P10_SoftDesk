# OC Projet 10: SoftDesk API Rest

## :v:Présentation du projet

Ce projet s’inscrit dans le cadre du parcours "Développeur d’application Python" sur OpenClassrooms.\
Il consiste à développer une API REST avec Django, en utilisant notamment les librairies Django Rest Framework pour l’API et SimpleJWT pour l’authentification.  
\
Le but de cette API est de permettre la gestion de projets de développement en équipe. Les fonctionnalités implémentées sont :  
* Inscription des utilisateurs et authentification via un token JWT.
* Création de nouveaux projets avec un type défini (backend, frontend, iOS, Android).
* Ajout ou suppression de contributeurs pour participer aux différents projets.
* Pour les contributeurs d’un projet, possibilité d’ajouter des issues avec différents champs pour la gestion du projet (utilisateur assigné, priorité, tag, statut).
* Enfin, pour chaque issue, la possibilité d’ajouter des commentaires afin que les contributeurs puissent échanger.
  
## :lock: Permissions  
Les permissions d'accès aux différentes données ont nécessité une attention particulière, comme le montre le tableau récapitulatif suivant :  
  
| Permissions | No authenticated | Authenticated | Contributor | Author |
|---          |:-:               |:-:            |:-:          |:-:     |
| Registration                      | O |
| Login or refresh                  | O | 
| Users list                        |   | O |
| Contributor project list          |   |   | O |
| Create new project                |   | O |
| Access to Project/Issue/Comment   |   |   | O |
| Add or remove project contributor |   |   |   | O |
| Update Project/Issue/Comment      |   |   |   | O |
| Delete Project/Issue/Comment      |   |   |   | O |
    
L'authentification s'effectue grâce au token JWT, qui est placé dans le champ Authorization de l'en-tête (header) de la requête HTTP.  
Un contributeur est un utilisateur authentifié contribuant à au moins un projet ou étant l'auteur d'un projet.  
Un auteur est un utilisateur authentifié, créateur d'une ressource particulière (projet, issue ou commentaire).  

## :blue_book:Documentation
Pour faciliter l'utilisation et l'intégration de l'API, une documentation détaillée est disponible sur Postman. Elle inclut :

* Les descriptions des endpoints.
* Les paramètres nécessaires.
* Les exemples de requêtes et de réponses.

:link: Accédez à la documentation Postman ici : [Lien vers la documentation](https://documenter.getpostman.com/view/38947734/2sAYQfEpxQ)
## :computer:Installation
Dans ce projet, j'ai choisi d'utiliser UV, un gestionnaire Python, pour sa simplicité et son efficacité dans la gestion des environnements et des dépendances. UV offre une approche moderne et intuitive, permettant de :

* Maintenir un environnement de développement isolé et propre.
* Simplifier l'installation et la mise à jour des dépendances.
* Gagner du temps grâce à une interface utilisateur conviviale et des commandes rapides.

Ce choix s'inscrit dans une volonté de rendre le projet accessible et facile à maintenir, tout en adoptant des outils performants adaptés aux besoins des développeurs Python modernes.\
\
Récupération du dépôt avec Git.
```
git clone https://github.com/PVL06/OC_P10_SoftDesk.git
```

Lancement du serveur avec UV.
```
cd src
uv run manage.py runserver
```
Si UV n'est pas installé, le fichier requirements.txt contient les dépendances requises.  
```
python -m venv env
# Windows
env/Script/activate
# Linux
source env/bin/activate
```
```
pip install -r requirements.txt
python manage.py runserver
```
Ce dépôt contient une base de données SQLite d'exemple incluse pour faciliter les tests et la compréhension du projet
## :white_check_mark:Utilisation
Une fois le serveur lancé en local, utilisez cURL pour envoyer des requêtes HTTP directement depuis votre terminal, ou Postman en vous basant sur la documentation fournie.\
Testez les fonctionnalités.