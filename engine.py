# engine.py — Moteur du jeu

import os
import time
import random
from data import HEROES, MONSTRES, ENVIRONNEMENTS, INCREMENTS, INCREMENT_DEGATS


# Couleurs ANSI

G = "\033[32m"   # Vert
R = "\033[31m"   # Rouge
Y = "\033[33m"   # Jaune
B = "\033[34m"   # Bleu
M = "\033[35m"   # Magenta
E = "\033[36m"   # Cyan (Éveil)
C = "\033[0m"    # Reset


# Utilitaires

def d20():
    return random.randint(1, 20)


def barre(pv, max_pv, col=G):
    ratio = max(0, min(1, pv / max_pv))
    blocs = int(ratio * 20)
    return f"{col}{'█' * blocs}{'░' * (20 - blocs)}{C} {max(0, pv)}/{max_pv} PV"


def cine(txt, col=B):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{col}╔" + "═" * 40 + "╗")
    print(f"║ {C}{txt:<38}{col} ║")
    print("╚" + "═" * 40 + "╝" + C)
    input("\n[ Entrée ]")


# Classes principales

class Hero:
    def __init__(self, key):
        data = HEROES[key]
        self.key = key
        self.nom = data["nom"]
        self.type = data["type"]
        self.arme = data["arme"]
        self.affinite = data["affinite"]
        self.techniques = [t.copy() for t in data["techniques"]]
        self.invoc_data = data["invocation"]

        self.niveau = 1
        self.max_pv = data["pv_base"]
        self.pv = self.max_pv

        # Éveil
        self.eveil = False
        self.eveil_tours = 0
        self.eveil_utilise = False

        # Invocation
        self.invocation = None
        self.invoc_tours = 0
        self.invoc_utilisee = False


    # ÉVEIL

    def activer_eveil(self):
        self.eveil = True
        self.eveil_tours = 4
        self.eveil_utilise = True

    def maj_eveil(self):
        if self.eveil:
            self.eveil_tours -= 1
            if self.eveil_tours <= 0:
                self.eveil = False

    def peut_eveiller(self):
        return (
            self.pv <= 30
            and not self.eveil
            and not self.eveil_utilise
            and self.invocation is None
        )

  
    # INVOCATION

    def peut_invoquer(self):
        return (
            self.niveau >= 3
            and self.invocation is None
            and not self.invoc_utilisee
            and not self.eveil
        )

    
    # LEVEL UP
    
    def level_up(self):
        old_pv = self.max_pv
        old_degats = [t["base"] for t in self.techniques]

        # PV
        if self.niveau - 1 < len(INCREMENTS):
            self.max_pv += INCREMENTS[self.niveau - 1]

        # Dégâts techniques
        for t in self.techniques:
            t["base"] += INCREMENT_DEGATS

        self.pv = self.max_pv

        new_degats = [t["base"] for t in self.techniques]

        debloque = []
        if self.niveau == 3:
            debloque.append("Invocation")

        return {
            "old_pv": old_pv,
            "new_pv": self.max_pv,
            "old_degats": old_degats,
            "new_degats": new_degats,
            "debloque": debloque,
        }


class Invocation:
    def __init__(self, data):
        self.nom = data["nom"]
        self.pv = data["pv"]
        self.max_pv = data["pv"]
        self.degats = data["degats"]
        self.type = data["type"]
        self.attaque_nom = data["attaque_nom"]


class Monstre:
    def __init__(self, data):
        self.nom = data["nom"]
        self.niveau = data["niveau"]
        self.pv = data["pv"]
        self.max_pv = data["pv"]
        self.dg1 = data["dg1"]
        self.dg2 = data["dg2"]
        self.seuil1 = data["seuil1"]
        self.seuil2 = data["seuil2"]
        self.type = data["type"]
        self.resistance = data["resistance"]
        self.env = data["env"]



# Calcul des dégâts

def appliquer_resistances(dmg, type_atk, monstre):
    if type_atk == monstre.resistance:
        return int(dmg * 0.5)
    return dmg


def bonus_environnement(hero, monstre, dmg):
    env = monstre.env
    bonus_type = ENVIRONNEMENTS[env]["bonus_type"]

    if hero.type == bonus_type:
        dmg += 5
    if monstre.type == bonus_type:
        dmg += 5

    return dmg


# Attaque du héros

def attaque_hero(hero, monstre, technique):
    seuil = technique["seuil"]
    base = technique["base"]
    type_atk = technique["type"]

    if d20() < seuil:
        return 0, False

    dmg = base

    if hero.eveil:
        dmg = int(dmg * 1.5)

    dmg = appliquer_resistances(dmg, type_atk, monstre)
    dmg = bonus_environnement(hero, monstre, dmg)

    monstre.pv -= dmg
    return dmg, True


# Attaque du monstre

def attaque_monstre(hero, monstre):
    jet = d20()
    if jet >= monstre.seuil2:
        dmg = monstre.dg2
    elif jet >= monstre.seuil1:
        dmg = monstre.dg1
    else:
        return 0, False

    if hero.invocation:
        hero.invocation.pv -= dmg
    else:
        hero.pv -= dmg

    return dmg, True


# Invocation

def invoquer(hero):
    hero.invocation = Invocation(hero.invoc_data)
    hero.invoc_tours = 3
    hero.invoc_utilisee = True


def attaque_invocation(hero, monstre):
    inv = hero.invocation
    dmg = inv.degats

    dmg = appliquer_resistances(dmg, inv.type, monstre)
    dmg = bonus_environnement(hero, monstre, dmg)

    monstre.pv -= dmg

    print(f"{Y}{inv.nom} bondit...")
    time.sleep(0.4)
    print("Impact !")
    time.sleep(0.4)
    print(f"{G}{dmg} dégâts infligés !{C}")
    time.sleep(0.8)

    return dmg


def tour_invocation(hero, monstre):
    attaque_invocation(hero, monstre)

    if monstre.pv > 0:
        dmg, touche = attaque_monstre(hero, monstre)
        if touche:
            print(f"{R}L'ennemi frappe l'invocation : -{dmg}{C}")
        else:
            print("L'ennemi rate son attaque.")
        time.sleep(1.8)

    hero.invoc_tours -= 1
    if hero.invoc_tours <= 0 or hero.invocation.pv <= 0:
        hero.invocation = None


# Cinématiques avancées

def cine_intro_niveau(niveau, monstre):
    os.system('cls' if os.name == 'nt' else 'clear')

    # Cadre titre (tout en blanc)
    print("╔" + "═" * 40 + "╗")
    titre = f"{monstre.nom} — Niveau {niveau}"
    print(f"║ {titre:<38} ║")
    print("╚" + "═" * 40 + "╝")

    # Environnement (en bleu uniquement)
    print(f"\n\033[34m{monstre.env}\033[0m")

    # Ambiance narrative (en blanc)
    ambiance = {
        "Marais du Delta": "Une brume lourde s’élève du sol… Des silhouettes rampent sous l’eau stagnante.",
        "Forêt des Spectres": "Les arbres murmurent… Des yeux brillent entre les branches.",
        "Temple de l’Oubli": "Un souffle froid traverse les ruines anciennes… Les ombres semblent t’observer.",
        "Plaines de la Savane": "Le vent chaud soulève la poussière… Un rugissement lointain résonne.",
        "Antre du Grootslang": "La roche tremble… Une aura maléfique s’échappe des profondeurs.",
    }

    creature = {
        "Mamlambo": "Créature reptilienne aux écailles luisantes, affamée de chair fraîche.",
        "Asanbosam": "Vampire arboricole aux crocs d’acier, tapi dans les hauteurs.",
        "Popobawa": "Esprit vengeur aux ailes déployées, maître des illusions nocturnes.",
        "Tokoloshe": "Démon farceur et cruel, rapide comme l’éclair.",
        "Seth – Roi des Enfers": "Divinité colérique, incarnation du chaos et du feu éternel.",
    }

    print(ambiance.get(monstre.env, ""))
    print(creature.get(monstre.nom, ""))
    print()
    input("[ Entrée ]")



def cine_evolution(hero, infos):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{B}Le pouvoir de {hero.nom} grandit...{C}\n")

    print(f"NIVEAU {hero.niveau} atteint !\n")

    # PV
    print(f"PV : {infos['old_pv']} → {infos['new_pv']}")

    # Techniques améliorées
    print("\nTechniques améliorées :")
    for i, tech in enumerate(hero.techniques):
        gain = infos["new_degats"][i] - infos["old_degats"][i]
        print(f"- {tech['nom']} : +{gain} dégâts")

    # Compétences débloquées
    if infos["debloque"]:
        print("\nNouvelles aptitudes :")
        for a in infos["debloque"]:
            print(f"- {a}")

    print()
    input("[ Entrée ]")
