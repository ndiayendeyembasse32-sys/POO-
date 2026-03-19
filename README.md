#  Légendes Africaines : L'Épopée (Projet POO)

Projet Python - EPSI

Un système de jeu de combat type RPG (Role Playing Game) en ligne de commande (REPL), développé en Python en utilisant les concepts avancés de la Programmation Orientée Objet (POO). 
Au lieu d'un univers fantastique classique, ce projet met à l'honneur de grandes figures de l'histoire et de la mythologie africaine.

# Équipe du Projet
Ndeye Mbasse Ndiaye: Chef d'Orchestre (Architecture de la boucle principale REPL, Intégration Git, Gestion du projet)
Marc Lolobgo : Architecte POO (Classes, Héritage, Polymorphisme)
Emmanuel Loukou : Maître des Mécaniques (Moteur de calculs, Lancers de dés)
David Sawagado : Créateur de Contenu (Données historiques, Bestiaire, Équilibrage)
Maimouna Kaba: Designer Console (Interface textuelle, Cinématiques, Menus)
# Prérequis et Lancement
Le jeu a été conçu pour tourner de manière fluide dans n'importe quel terminal, sans interface graphique lourde.

Pour lancer le jeu :
1. Ouvrez votre terminal (ou invite de commande).
2. Naviguez jusqu'au dossier du projet.
3. Exécutez le fichier principal avec Python :
   ```bash
   python game.py
# Architecture du Code (Modularité)
Pour éviter les conflits de fusion sur Git à 5 personnes et garder un code propre, nous avons séparé la logique en trois fichiers distincts (façon API) :

data.py: Stockage des dictionnaires de personnages, de l'arsenal et des environnements (Base de données).

engine.py: Les classes ( Hero, Monstre, Invocation) et le moteur mathématique de résolution des attaques.

game.py: L'interface utilisateur, les menus interactifs et la boucle principale du combat (REPL).

# Fonctionnalités Supplémentaires (Bonus)
En plus des consignes de base (Attaque, Héritage, Polymorphisme), notre équipe a intégré les mécaniques avancées suivantes :

Le Mode Éveil (Transformation) : Lorsqu'un héros tombe en dessous d'un certain seuil critique de points de vie, il peut choisir d'activer son "Éveil", ce qui booste considérablement ses dégâts de base de façon temporaire.

L'Avantage Contextuel (Terrain) : Les arènes changent à chaque niveau (ex : Forêt des Spectres ). Si le type d'attaque d'une créature correspond à l'arène, elle reçoit un bonus de dégâts mathématiques.

Le Système d'Invocation : Grâce à la POO, un héros de niveau 3 peut instancier un nouvel objet Invocationen plein combat. Cet objet (ex : le Lion du Mandé ) prend les coups et attaque à la place du héros pendant 3 tours.

Cinématiques et Interface Dynamique : Utilisation de rafraîchissements de console et de pauses ( time.sleep()) pour donner un vrai rythme textuel au combat.

Progression (Level-Up) : Un système d'enchaînement de 5 niveaux de difficulté croissante avec augmentation des statistiques du héros entre chaque combat.
