# OC_project02
Utilisez les bases de Python pour l'analyse de marché
## Présentation
Le but de ce projet est d'écrire un script Python cappable de récuperer les données de tous les livres présents sur [http://books.toscrape.com/](http://books.toscrape.com/), et de les regrouper par catégories dans des fichiers CSV.
## Usage
Tout d'abbord, il faut s'assurer que `Python 3` et `PIP` sont installés et de préférence à jour sur votre machine.
Il faudra ensuite installer les dépendences necessaires au script:
```sh
pip install -r requirements.txt
```
La commande permantant de lancer le scrapping est la suivante:
```sh
python main.py
```
Une fois le script lancé, celui-ci créera un dossier `exports` dans lequel seront placées les données récuppérées, classés par catégorie.
