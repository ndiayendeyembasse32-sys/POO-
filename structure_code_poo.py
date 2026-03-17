import random

class Creature:
    """Classe mère gérant la structure de base de toute entité au combat."""
    def __init__(self, nom, pv, ca, type_degat):
        self.nom = nom
        self.pv = pv
        self.max_pv = pv
        self.ca = ca  # Classe d'Armure (Défense)
        self.type_degat = type_degat
        self.initiative = 0
        self.etats = []

    def est_vivante(self):
        """Vérifie si la créature a encore des points de vie."""
        return self.pv > 0

    def lancer_initiative(self):
        """Génère un score d'initiative (1d20)."""
        self.initiative = random.randint(1, 20)
        return self.initiative

    def recevoir_degats(self, montant, type_attaque=None):
        """Réduit les PV. Cette méthode peut être surchargée (Polymorphisme)."""
        self.pv = max(0, self.pv - montant)
        return montant

    def attaquer(self, cible, moteur_calcul):
        """
        Définit l'intention d'attaque. 
        Le calcul réel est délégué au Maître des Calculs (engine.py).
        """
        return moteur_calcul.calculer_attaque(self, cible)

class Hero(Creature):
    """Classe représentant les figures historiques (Joueurs)."""
    def __init__(self, nom, pv, ca, type_degat, arme, histoire, special=None):
        super().__init__(nom, pv, ca, type_degat)
        self.arme = arme
        self.histoire = histoire
        self.type_special = special  # 'invocation', 'contextuel', 'eveil'
        self.special_disponible = True

    def invoquer(self):
        """Logique d'invocation pour Soundiata Keïta ou Abla Pokou."""
        if self.type_special == "invocation" and self.special_disponible:
            self.special_disponible = False
            
            if "Soundiata" in self.nom:
                # Création d'une entité temporaire : Le Lion du Mali
                return Creature("Lion du Mali", 50, 14, "Tranchant")
                
            elif "Abla Pokou" in self.nom:
                # Création d'une entité temporaire : Esprit du Peuple Baoulé
                # (Ou un hippopotame protecteur en référence à la légende du passage du fleuve)
                return Creature("Gardien du Fleuve", 60, 16, "Contondant")
                
        return None

class Monstre(Creature):
    """Classe représentant les adversaires (PNJ)."""
    def __init__(self, nom, pv, ca, type_degat, resistance):
        super().__init__(nom, pv, ca, type_degat)
        self.resistance = resistance

    def recevoir_degats(self, montant, type_attaque=None):
        """
        Encapsulation : Le monstre vérifie lui-même sa résistance 
        avant de déduire les PV.
        """
        if type_attaque == self.resistance:
            montant //= 2
            # Note : Le message de résistance sera géré par le Designer Console
        return super().recevoir_degats(montant)

    def mode_eveil(self):
        """Boost de rage pour Mobutu ou Béhanzin quand les PV sont bas."""
        if self.pv < (self.max_pv * 0.3):
            self.ca += 2  # Augmentation de la défense en mode survie
            return True
        return False
    

class Environnement:
    def __init__(self, nom, type_bonus=None):
        self.nom = nom
        self.type_bonus = type_bonus # Ex: "Aquatique", "Savane"

    # Pour que print(environnement) affiche le nom
    def __str__(self):
        return self.nom
