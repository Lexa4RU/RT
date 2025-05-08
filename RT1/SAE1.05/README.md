# SAE1.05 Traiter des données

## Groupe Trafic Internet
## Présentation 

- Ce projet fait partie entière de la SAE1.05 "Traiter des données" qui consiste à réaliser un script permettant de récupérer des données sur le [site du gouvernement](https://files.data.gouv.fr/arcep_donnees/fixe/maconnexioninternet/statistiques/last/region/).
- De les traiter de manière à garder uniquement les données que l'on souhaite.
- De les afficher sur un site web graphiquement.   

## Description
Ainsi donc le script permet de télécharger le fichier "region_debit" sur le site [data.gouv.fr](https://files.data.gouv.fr/arcep_donnees/fixe/maconnexioninternet/statistiques/last/region/region_debit.csv), retire les lignes inutiles du fichier, et envoie selon nos besoins dans plusieurs fichiers json (6 au total) les données qui nous intéressent, ensuite viens le php qui permet d'afficher les données des fichiers jsons dans un graphique établi par nos soins. 

## Auteurs
Ptak Axel, De Backer Ethan, Allary Julian.

## Les tâches 

Les tâches que nous avons eues à affronter pour parvenir à la fin du projet : 
- Télécharger  le fichier .csv 
- Trier les données présentes dans le fichier .csv en fonction de leur positionement dans le fichier
- Copie des données utiles dans des fichiers .json
- Faire le code php pour afficher les fichiers .json dans un graphique
- Documenter les codes crée afin que chaque invité puisse en comprendre toutes les finalités

## Partage des tâches 

Nous avons partagé le travail de la manière suivante : 
- Julian s'occupe en grande partie du code Python.
- Ethan travaille sur le code php et vérifie de son bon fonctionnement.
- Axel quant à lui s'occupe de la relecture des codes, de la documentation complète du projet et du maintien de l'ordre au sein de l'équipe.

## Utilisation 

Le script python s'utilise de la manière suivante : 
- ./Recup_Json_v5 {lien du fichier} {destination du fichier} 
Les deux pramètres sont obligatoires. 
Ensuite il faudra lancer l'un des URLs suivants : 
- 172.31.25.6/~/
Afin de pouvoir voir apparaitre le graphique.
