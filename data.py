import random

# ============================================
# CLASSES
# ============================================

class Creature:
    def __init__(self, nom, pv, ca, type_degat):
        self.nom = nom
        self.pv = pv
        self.max_pv = pv
        self.ca = ca
        self.type_degat = type_degat
        self.initiative = 0
        self.etats = []

    def est_vivante(self):
        return self.pv > 0

    def lancer_initiative(self):
        self.initiative = random.randint(1, 20)
        return self.initiative

    def recevoir_degats(self, montant, type_attaque=None):
        self.pv = max(0, self.pv - montant)
        return montant

class Hero(Creature):
    def __init__(self, nom, pv, ca, type_degat, arme, histoire, special=None):
        super().__init__(nom, pv, ca, type_degat)
        self.arme = arme
        self.histoire = histoire
        self.type_special = special
        self.special_disponible = True

    def invoquer(self):
        if self.type_special == "invocation" and self.special_disponible:
            self.special_disponible = False
            
            if "Soundiata" in self.nom:
                return Creature("Lion du Mali", 50, 14, "Tranchant")
            elif "Abla Pokou" in self.nom:
                return Creature("Gardien du Fleuve", 60, 16, "Contondant")
        return None

class Monstre(Creature):
    def __init__(self, nom, pv, ca, type_degat, resistance):
        super().__init__(nom, pv, ca, type_degat)
        self.resistance = resistance

    def recevoir_degats(self, montant, type_attaque=None):
        if type_attaque == self.resistance:
            montant //= 2
        return super().recevoir_degats(montant)

    def mode_eveil(self):
        if self.pv < (self.max_pv * 0.3):
            self.ca += 2
            return True
        return False

# ============================================
# DONNÉES 
# ============================================

# HÉROS (2 existants)
soundiata = Hero(
    nom="Soundiata Keïta",
    pv=120,
    ca=16,
    type_degat="Tranchant",
    arme="Épée Royale",
    histoire="Fondateur de l'Empire du Mali",
    special="invocation"
)

abla_pokou = Hero(
    nom="Abla Pokou",
    pv=100,
    ca=15,
    type_degat="Magique",
    arme="Bâton Sacré",
    histoire="Princesse Baoulé qui sacrifia son enfant",
    special="invocation"
)

# ============================================
# MONSTRES (2 anciens + 3 nouveaux = 5)
# ============================================

# 1. Mobutu Sese Seko (existant)
mobutu = Monstre(
    nom="Mobutu Sese Seko",
    pv=150,
    ca=14,
    type_degat="Contondant",
    resistance="Percant"
)

# 2. Soumaoro Kanté (existant)
soumaoro = Monstre(
    nom="Soumaoro Kanté",
    pv=140,
    ca=16,
    type_degat="Poison",
    resistance="Tranchant"
)

# 3. NOUVEAU : Béhanzin (Roi du Dahomey)
behanzin = Monstre(
    nom="Béhanzin",
    pv=160,
    ca=15,
    type_degat="Feu",
    resistance="Magique"  # Résiste à la magie
)

# 4. NOUVEAU : Samory Touré (Résistant guinéen)
samory = Monstre(
    nom="Samory Touré",
    pv=145,
    ca=17,
    type_degat="Percant",
    resistance="Contondant"  # Résiste aux dégâts contondants
)

# 5. NOUVEAU : Shaka Zulu (Guerrier zoulou)
shaka = Monstre(
    nom="Shaka Zulu",
    pv=155,
    ca=16,
    type_degat="Tranchant",
    resistance="Percant"  # Résiste aux attaques perçantes
)

# ============================================
# LISTES POUR MAIN.PY
# ============================================

# Liste des héros (toujours 2)
heros = [soundiata, abla_pokou]

# Liste des monstres (maintenant 5)
monstres = [mobutu, soumaoro, behanzin, samory, shaka]

# Optionnel : exporter aussi les classes si nécessaire
__all__ = ['Creature', 'Hero', 'Monstre', 'heros', 'monstres']