# Légendes Africaines : L'Épopée (Projet POO)

**Projet Python - EPSI**

Un système de jeu de rôle (RPG) en ligne de commande (REPL), développé en Python en utilisant les concepts avancés de la Programmation Orientée Objet (POO). 
Ce projet met à l'honneur de grandes figures de l'histoire et de la mythologie africaine à travers un système de combat multijoueur asymétrique (Joueurs contre Maître du Jeu).

## Équipe du Projet
Ndeye Mbasse Ndiaye : Chef d'Orchestre (Architecture multijoueur, Intégration Git, Gestion du projet)
Marc Lolobgo : Architecte POO (Classes, Héritage, Polymorphisme)
Emmanuel Loukou: Maître des Mécaniques (Moteur de calculs, Lancers de dés, Initiative)
David sawagado : Créateur de Contenu (Données historiques, Bestiaire, Équilibrage)
Maimouna Kaba : Designer Console (Interface textuelle, Menus, Affichage dynamique)

## Prérequis et Lancement
Le jeu a été conçu pour s'exécuter de manière fluide dans n'importe quel terminal standard, sans nécessiter d'interface graphique lourde ou de bibliothèques externes.

**Pour lancer le jeu :**
1. Ouvrez votre terminal ou invite de commande.
2. Naviguez jusqu'au répertoire racine du projet.
3. Exécutez le fichier principal avec Python :
   ```bash
   python game.py
Architecture du Code (Modularité)
Pour garantir la maintenabilité du code et un travail collaboratif efficace sur Git, l'architecture a été divisée en trois modules distincts :

data.py: Base de données statiques (dictionnaires) contenant les caractéristiques des héros, le bestiaire des monstres et les statistiques d'équipement.

engine.py: Moteur logique contenant les classes POO ( Hero, Monstre, Invocation) et les fonctions mathématiques de résolution de combat.

game.py: Interface utilisateur, gestion des menus, boucle de gameplay REPL et gestion de l'état global du champ de bataille.

Fonctionnalités Principales et Avancées
En plus des consignes de base (Héritage, Polymorphisme), notre équipe a développé un véritable moteur de jeu de rôle interactif :

Multijoueur Asymétrique (Nouveau) : Le jeu permet désormais à plusieurs joueurs de s'allier contre un joueur incarnant le Maître du Jeu (MJ), qui déploie et contrôle les monstres.

Système d'Initiative Dynamique : Au début de chaque affrontement, un jet de dé 20 est effectué pour chaque entité (Héros et Monstres) afin de déterminer un ordre de passage strict.

Ciblage Manuel : Fini les attaques aléatoires ; les joueurs et le MJ doivent analyser le champ de bataille et sélectionner précisément la cible de leurs attaques.

Actions du Maître du Jeu : Le MJ dispose de capacités tactiques uniques, lui permettant de soigner ses créatures ou d'accumuler des bonus de dégâts (Buffs) au lieu de simplement attaquer.

Le Mode Éveil : Lorsqu'un héros tombe en dessous d'un seuil critique de points de vie, il peut sacrifier son tour d'attaque pour s'éveiller, altérant drastiquement ses dégâts pour le reste du combat.

Système d'Invocation : Grâce à l'instanciation dynamique d'objets, un héros peut invoquer un allié sur le terrain. L'invocation possède ses propres statistiques et peut recevoir des ordres de ciblage.