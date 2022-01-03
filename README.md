# Rapport de projet - Python
## Projet portant sur les communes défavorisées en France
Cloé BERTHELIN et Valentin BAILLEUL  
ESIEE PARIS - E3FI 1I  
Janvier 2022  
## Installation
- Cloner le dépôt :
    - git clone *https://github.com/Clo3pro/bailleul-berthelin_python.git*
- Ouvrir une Invite de commandes
- Pour installer les libraires, entrer :
    - **python -m pip install Dash Pandas Folium plotly.express branca dash_bootstrap_components requests**
- Entrer :
    - **cd {*CheminVersLeDossierCloné*}**
    - **python main.py**

Pour relancer les calculs, entrer *python functions.py*
    
## Developer Guide

La structure de l’application Dashboard est principalement organisée dans 2 fichiers:
- functions.py
- main.py

Dans le fichier functions se trouvent toutes les fonctions de récupération et de traitement de données.  
Dans le fichier main se trouvent les fonctions de formatage et d’affichage de ces données en une application web.  
Les librairies sont utilisées:  
- Dash
- Panda
- Folium
- plotly express
- branca
- dash bootstrap components
- requests
- csv
- Json

## functions

Dans le fichier functions, nous avons créé des fichiers csv et geojson permettant la récupération de données et leur affichage. Nous avons importé et travaillé sur une API provenant :  
*https://public.opendatasoft.com/explore/dataset/liste-des-communes-classees-en-zones-defavorisees-au-1er-janvier-2017/table/?flg=fr*  

- D’abord on récupère les villes défavorisées présentes dans l’API
- Création d’un dictionnaire répertoriant et classant les villes selon leur entrée dans le tableau
- Création CSV reliant période d’entrée et nombre de villes ajoutées dans cette période
- Création CSV reliant Département / Pourcentage communes défavorisées dans le département / Nombre total de communes dans le département / Nombre de communes défavorisées dans le département
- Création d’un gros document GeoJSON comportant toutes les datas de chacune des villes défavorisées qui sont dans le département le plus défavorisé

## main

Ce fichier contient tout le code dit “front-end” de l’application dashboard.  
On y retrouve les divers dictionnaires de données traités au préalable dans functions.  
Des blocs de commentaires sont mis en place au-dessus des différentes fonctions afin d’avoir une meilleure compréhension du code.  

Nous utilisons la librairie Dash combinée avec Bootstrap pour gérer l’affichage global des différents composants.  
Bootstrap est également utilisé pour gérer l’affichage dynamique du tableau et des cartes à l’aide de boutons qui affiche ou non les containers de ces éléments.  

La librairie plotly express permet un affichage simple et efficace de l’histogramme présent.  
La librairie Dash combinée à Panda permettent également la création de tableaux de données, ce qui nous permet d’avoir une autre manière de visualiser les données.  
Enfin, nous utilisons les librairies branca, geopandas et Folium qui nous permettent d’afficher les cartes présentes sur le Dashboard.  

Folium utilise la très connue librairie Leaflet de Javascript pour générer des cartes faciles d’utilisation.  

## User Guide 

Une fois l’application lancée, il vous faut aller dans le navigateur web de votre choix à l’adresse suivante :  
**http://127.0.0.1:8050/**  
Vous arriverez sur le dashboard.  

Vous verrez d'ors et déjà le titre et la nature des données que nous avons décidé de traiter:  
Les communes françaises en zones rurales défavorisées.  
Vous aurez également la vision globale de ces données sous la forme d’un histogramme.  

Sous cet histogramme, vous verrez trois boutons :
- Le premier permet d’afficher le tableau qui est en corrélation avec l’histogramme. Ce tableau est triable en cliquant sur les flèches (haut/bas) situés à l’intérieur gauche de chaque en-tête de colonne.
- Le deuxième bouton permet d’afficher la première carte qui représente le département qui a le plus de communes en zones rurales défavorisées.
- Enfin, le troisième bouton permet d’afficher une seconde carte. Vous trouverez sur celle-ci les départements français colorés du jaune au rouge selon le pourcentage de communes défavorisées: jaune, le nombre le plus faible. Rouge, le nombre le plus élevé.

Vous pouvez afficher, ou bien cacher ces cartes et le tableau en cliquant à nouveau sur les boutons.

## Les limitations du projet

La seconde carte voit sa couleur camouflée sous un gris omniprésent.  
Les départements n'ont donc actuellement pas de gradient de couleur qui leur est visiblement appliqué.
