# data.py — Le Gardien du Bestiaire
# Rôle 3 : Ce fichier instancie tous les objets du jeu (héros, monstres, armes, environnements).
# Aucun print() ici. Uniquement des données prêtes à l'emploi.

from models import Hero, Monstre, Environnement


# ============================================================
# ARMES (utilisées par les Héros)
# Chaque arme est un dictionnaire : nom, formule de dégâts, type de dégât
# ============================================================

ARMES = [
    {"nom": "Épée longue",      "degats": "1d8",  "type_degat": "Tranchant"},
    {"nom": "Lance de guerre",  "degats": "1d10", "type_degat": "Perçant"},
    {"nom": "Masse d'armes",    "degats": "1d6",  "type_degat": "Contondant"},
    {"nom": "Arc court",        "degats": "1d6",  "type_degat": "Perçant"},
    {"nom": "Hache de bataille","degats": "1d12", "type_degat": "Tranchant"},
    {"nom": "Dague",            "degats": "1d4",  "type_degat": "Perçant"},
    {"nom": "Bâton de feu",     "degats": "2d6",  "type_degat": "Feu"},
    {"nom": "Fouet empoisonné", "degats": "1d6",  "type_degat": "Poison"},
]


# ============================================================
# HÉROS — Figures historiques africaines
# Hero(nom, pv, ca, type_degat, arme, histoire, special=None)
# L'arme est assignée au moment de la sélection dans main.py
# ============================================================

def creer_heros():
    """Retourne la liste de tous les héros disponibles (sans arme assignée)."""
    return [
        Hero(
            nom="Soundiata Keïta",
            pv=130,
            ca=16,
            type_degat="Tranchant",
            arme=None,
            histoire="Fondateur de l'Empire du Mali, il se releva de sa paralysie pour libérer son peuple.",
            special="invocation"  # Peut invoquer le Lion du Mali
        ),
        Hero(
            nom="Abla Pokou",
            pv=100,
            ca=13,
            type_degat="Magique",
            arme=None,
            histoire="Reine Baoulé qui sacrifia tout pour sauver son peuple en traversant le fleuve Comoé.",
            special="invocation"  # Peut invoquer le Gardien du Fleuve
        ),
        Hero(
            nom="Yaa Asantewaa",
            pv=120,
            ca=15,
            type_degat="Tranchant",
            arme=None,
            histoire="Reine-mère Ashanti qui mena la résistance contre les colonisateurs britanniques.",
            special="contextuel"  # Bonus de dégâts contre les ennemis aux PV bas
        ),
        Hero(
            nom="Shaka Zulu",
            pv=140,
            ca=17,
            type_degat="Perçant",
            arme=None,
            histoire="Roi Zoulou et stratège militaire de génie, il révolutionna l'art de la guerre.",
            special="eveil"  # Entre en rage quand ses PV descendent sous 30%
        ),
        Hero(
            nom="Makeda de Saba",
            pv=110,
            ca=14,
            type_degat="Magique",
            arme=None,
            histoire="Reine légendaire de Saba, dont la sagesse et la lumière guidaient les peuples.",
            special=None
        ),
    ]


# ============================================================
# MONSTRES — Adversaires du Bestiaire
# Monstre(nom, pv, ca, type_degat, resistance)
# ============================================================

def creer_monstres():
    """Retourne la liste de tous les monstres disponibles."""
    return [
        Monstre(
            nom="Hyène Albinos",
            pv=40,
            ca=11,
            type_degat="Perçant",       # Morsure
            resistance="Poison"          # Immunisée au poison naturellement
        ),
        Monstre(
            nom="Guerrier d'Argile",
            pv=80,
            ca=14,
            type_degat="Contondant",     # Frappe de pierre
            resistance="Perçant"         # L'argile résiste aux lames
        ),
        Monstre(
            nom="Serpent Géant",
            pv=60,
            ca=12,
            type_degat="Poison",         # Venin
            resistance="Poison"          # Immunisé à son propre poison
        ),
        Monstre(
            nom="Éléphant de Guerre",
            pv=200,
            ca=15,
            type_degat="Contondant",     # Piétinement
            resistance="Contondant"      # Peau épaisse
        ),
        Monstre(
            nom="Esprit de la Savane",
            pv=70,
            ca=13,
            type_degat="Magique",        # Malédiction
            resistance="Tranchant"       # Immatériel, les lames glissent
        ),
        Monstre(
            nom="Crocodile Géant",
            pv=110,
            ca=16,
            type_degat="Perçant",        # Mâchoires
            resistance="Contondant"      # Cuirasse osseuse
        ),
        Monstre(
            nom="Béhanzin le Tyran",     # Mini-boss
            pv=180,
            ca=17,
            type_degat="Tranchant",      # Lame royale
            resistance="Feu"             # Insensible aux flammes
        ),
        Monstre(
            nom="GROOTSLANG",            # Boss final — Créature mythique mi-éléphant mi-serpent
            pv=280,
            ca=18,
            type_degat="Poison",         # Venin dévastateur
            resistance="Magique"         # Résiste à la magie ancienne
        ),
    ]


# ============================================================
# ENVIRONNEMENTS — Zones de combat
# Environnement(nom, type_bonus)
# Le type_bonus peut être utilisé par engine.py pour appliquer des effets
# ============================================================

def creer_environnements():
    """Retourne la liste des environnements disponibles."""
    return [
        Environnement("Forêt des Spectres",   type_bonus="Poison"),    # Les plantes empoisonnent
        Environnement("Temple de l'Oubli",    type_bonus="Magique"),   # Energie ancienne
        Environnement("Plaines de la Savane", type_bonus="Tranchant"), # Avantage aux lames
        Environnement("Marais du Delta",      type_bonus="Contondant"),# Sol lourd
        Environnement("Antre du Grootslang",  type_bonus="Poison"),    # Repaire empoisonné
    ]


# ============================================================
# ACCÈS RAPIDE — Dictionnaires indexés par nom (utile pour main.py)
# ============================================================

HEROS_PAR_NOM     = {h.nom: h for h in creer_heros()}
MONSTRES_PAR_NOM  = {m.nom: m for m in creer_monstres()}
ARMES_PAR_NOM     = {a["nom"]: a for a in ARMES}