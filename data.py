
# data.py — Données du jeu


# Progression PV et dégâts
INCREMENTS = [10, 15, 20, 25, 30]
INCREMENT_DEGATS = 5  

# Environnements
ENVIRONNEMENTS = {
    "Marais du Delta": {"bonus_type": "contondant"},
    "Forêt des Spectres": {"bonus_type": "poison"},
    "Temple de l’Oubli": {"bonus_type": "magique"},
    "Plaines de la Savane": {"bonus_type": "tranchant"},
    "Antre du Grootslang": {"bonus_type": "poison"},
}

# Techniques des héros
TECHNIQUES = {
    "Soundjata": [
        {"nom": "Découpe Mortelle", "seuil": 6, "base": 22, "type": "tranchant"},
        {"nom": "Shishi-Ssonsson", "seuil": 14, "base": 42, "type": "tranchant"},
    ],
    "Abla Pokou": [
        {"nom": "Tremblement de Terre", "seuil": 6, "base": 20, "type": "magique"},
        {"nom": "La Foudre", "seuil": 14, "base": 40, "type": "magique"},
    ],
    "Moro Naba": [
        {"nom": "Soleil Cruel", "seuil": 6, "base": 22, "type": "feu"},
        {"nom": "Lune Rouge", "seuil": 14, "base": 42, "type": "feu"},
    ],
}

# Invocations (débloquées niveau 3)
INVOCATIONS = {
    "Soundjata": {
        "nom": "Lion du Mandé",
        "pv": 48,
        "degats": 35,
        "type": "tranchant",
        "attaque_nom": "Griffes du Mandé",
    },
    "Abla Pokou": {
        "nom": "Hippopotame Sacré",
        "pv": 53,
        "degats": 40,
        "type": "contondant",
        "attaque_nom": "Charge Sacrée",
    },
    "Moro Naba": {
        "nom": "Masque Guerrier",
        "pv": 50,
        "degats": 35,
        "type": "feu",
        "attaque_nom": "Coup Spirituel",
    },
}

# Héros
HEROES = {
    "Soundjata": {
        "nom": "Soundjata Keïta",
        "pv_base": 150,
        "type": "tranchant",
        "arme": "Épée Mythique Mandingue",
        "affinite": "Plaines de la Savane",
        "techniques": TECHNIQUES["Soundjata"],
        "invocation": INVOCATIONS["Soundjata"],
    },
    "Abla Pokou": {
        "nom": "Abla Pokou",
        "pv_base": 160,
        "type": "magique",
        "arme": "Bâton Sacré Baoulé",
        "affinite": "Temple de l’Oubli",
        "techniques": TECHNIQUES["Abla Pokou"],
        "invocation": INVOCATIONS["Abla Pokou"],
    },
    "Moro Naba": {
        "nom": "Moro Naba",
        "pv_base": 170,
        "type": "feu",
        "arme": "Bague Spirituelle",
        "affinite": "Antre du Grootslang",
        "techniques": TECHNIQUES["Moro Naba"],
        "invocation": INVOCATIONS["Moro Naba"],
    },
}
# Monstres avec stats indépendantes et nouvelles capacités pour le MJ
MONSTRES = {
    1: {
        "nom": "Mamlambo",
        "niveau": 1,
        "pv": 130,
        "dg1": 8,
        "dg2": 25,
        "seuil1": 8,
        "seuil2": 15,
        "type": "poison",
        "resistance": "contondant",
        "env": "Marais du Delta",
        "soin": 15,
        "buff_degats": 5
    },
    2: {
        "nom": "Asanbosam",
        "niveau": 2,
        "pv": 150,
        "dg1": 18,
        "dg2": 35,
        "seuil1": 7,
        "seuil2": 15,
        "type": "tranchant",
        "resistance": "poison",
        "env": "Forêt des Spectres",
        "soin": 20,
        "buff_degats": 8
    },
    3: {
        "nom": "Popobawa",
        "niveau": 3,
        "pv": 180,
        "dg1": 22,
        "dg2": 45,
        "seuil1": 7,
        "seuil2": 15,
        "type": "magique",
        "resistance": "magique",
        "env": "Temple de l’Oubli",
        "soin": 25,
        "buff_degats": 10
    },
    4: {
        "nom": "Tokoloshe",
        "niveau": 4,
        "pv": 220,
        "dg1": 24,
        "dg2": 60,
        "seuil1": 7,
        "seuil2": 15,
        "type": "contondant",
        "resistance": "tranchant",
        "env": "Plaines de la Savane",
        "soin": 30,
        "buff_degats": 12
    },
    5: {
        "nom": "Seth – Roi des Enfers",
        "niveau": 5,
        "pv": 280,
        "dg1": 26,
        "dg2": 65,
        "seuil1": 6,
        "seuil2": 12,
        "type": "feu",
        "resistance": "poison",
        "env": "Antre du Grootslang",
        "soin": 40,
        "buff_degats": 15
    },
}