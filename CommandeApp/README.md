# CommandeApp
## Bibliothèques

- GUI (Graphic User Interface avec tkinter)
- SQLite3

## Pourquoi avoir créer ce projet?

Cette application avait pour but d'aider mon père à faire les commandes de nourritures afin de pouvoir lui faire gagner du temps. L'entreprise où il travaille n'ayant personne pour faire les commandes mon père est donc obligé de les faire à la main, car l'entreprise n'a pas d'outils qui lui permette de lui facilité la tâche, il est donc obligé d'y consacré beaucoup de temps hors de ses heures de travail.

## Qu'est ce que cette application permet de faire?

Grâce à cette application vous pouvez :
- Ajouter à la base de donnée, stocker en local dans un fichier ".db", un produit avec un identifiant, un libellé, et une unité de mesure.
- Créer une commande, en ajoutant une quantité à votre produit.
- Générer un tableau Excel de toutes les informations de votre base de donnée, et cela une fois votre commande terminer.

Note : Dans votre base de donnée les produits auront par default leur quantité à 0, et une fois que votre fichier est généré l'ensemble des quantités des produits repasse à 0, la commande précédente est donc perdu une fois que ce fichier est généré.