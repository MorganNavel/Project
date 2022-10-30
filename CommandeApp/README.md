# CommandeApp
## Bibliothèques

- GUI (Graphic User Interface with tkinter)
- SQLite DB

## Pourquoi avoir créer ce projet?

Cette application avez pour but d'aider mon père à faire les commandes de nourriture dans l'entreprise où il travaille. Mon père n'étant embauché en tant que cuisinier mais n'ayant pas le choix de devoir faire ces commandes et l'entreprise n'ayant pas d'outils afin de lui facilité la tâche, et étant obligé de tout faire à la main. J'ai décidé de faire cette application.

## Qu'est ce que cette application permet de faire?

Grâce à cette application vous pouvez :
- Ajouter à la base de donnée, stocker en local dans un fichier ".db", un produit avec un identifiant, un libellé, et une unité de mesure.
- Créer une commande, en ajoutant une quantité à votre produit.
- Générer un tableau Excel de toutes les informations de votre base de donnée, et cela une fois votre commande terminer.

Note : Dans votre base de donnée les produits auront par default leur quantité à 0, et une fois que votre fichier est généré l'ensemble des quantités des produits repasse à 0, la commande précédente est donc perdu une fois que ce fichier est généré.