import os
import time
import random


# --- LOGIQUE TECHNIQUE ---
def d20():
    return random.randint(1, 20)


def lancer_degats(formule):
    try:
        nb, faces = map(int, formule.lower().split('d'))
        return sum(random.randint(1, faces) for _ in range(nb))
    except:
        return 5


# --- STRUCTURE POO ---
class Hero:
    def __init__(self, nom, intro, pv, ca, competences):
        self.nom = nom
        self.intro = intro
        self.pv = self.max_pv = pv
        self.ca = ca
        self.competences = competences  # Liste de dictionnaires
        self.niveau = 1
        self.arme_nom = "Poings nus"
        self.arme_degats = "1d4"


class Monstre:
    def __init__(self, nom, pv, ca, degats, loot=None):
        self.nom = nom
        self.pv = pv
        self.ca = ca
        self.degats = degats
        self.loot = loot


# --- DESIGN & FLUIDITÉ (Rôle 4) ---
def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear 2>/dev/null')
    print("\n" * 80)


def cinematique(texte):
    clean()
    print("═" * 60)
    for ligne in texte.split('\n'):
        print(f"  {ligne.strip()}")
        time.sleep(0.8)  # Plus rapide pour la fluidité
    print("═" * 60)
    input("\n[ Entrée ]")


def barre_vie(actuel, maximum):
    taille = 20
    remplis = int((actuel / maximum) * taille) if maximum > 0 else 0
    return f"[{'█' * remplis}{'░' * (taille - remplis)}] {actuel}/{maximum} PV"


def level_up(h):
    clean()
    h.niveau += 1
    h.max_pv += 30
    h.pv = h.max_pv
    print("✨ NIVEAU SUPÉRIEUR ! ✨\nVos PV augmentent et vous êtes soigné.")
    time.sleep(1.5)


# --- MOTEUR DE COMBAT ---
def jouer():
    clean()
    print("🌍 LÉGENDES D'AUBE-TERRE : ÉDITION ÉPIQUE")
    print("=" * 40)

    print("Sélectionnez votre héros :\n1. Shaka (Zoulou)\n2. Makeda (Saba)")
    choix = input("> ")

    if choix == "2":
        # Compétences de Makeda : Précision et Magie
        comp = [
            {"nom": "Flèche de Lumière", "seuil": 5, "degats": "1d10", "desc": "Attaque fiable"},
            {"nom": "Rayon Solaire", "seuil": 14, "degats": "4d8", "desc": "Puissant mais risqué"},
            {"nom": "Jugement Divin", "seuil": 18, "degats": "8d6", "desc": "Dévastateur"}
        ]
        h = Hero("Makeda", "Reine de Saba, protectrice du Sceptre.", 100, 14, comp)
    else:
        # Compétences de Shaka : Force brute
        comp = [
            {"nom": "Estocade", "seuil": 6, "degats": "1d12", "desc": "Coup rapide"},
            {"nom": "Éclair d'Iklwa", "seuil": 15, "degats": "5d6", "desc": "Technique royale"},
            {"nom": "Colère du Lion", "seuil": 19, "degats": "10d6", "desc": "Ultime"}
        ]
        h = Hero("Shaka", "Guerrier Zoulou, l'unificateur des clans.", 130, 16, comp)

    cinematique(f"L'épopée de {h.nom} commence...\n{h.intro}")

    aventure = [
        ("Forêt des Spectres", Monstre("Hyène Albinos", 40, 11, "1d6", {"nom": "Dague en Os", "degats": "1d8"})),
        ("Temple de l'Oubli",
         Monstre("Guerrier d'Argile", 80, 13, "1d10", {"nom": "Lance de Guerre", "degats": "2d8"})),
        ("ANTRE DU BOSS", Monstre("GROOTSLANG", 250, 15, "3d8"))
    ]

    for zone, ennemi in aventure:
        if h.pv <= 0: break
        cinematique(f"Arrivée : {zone}\nUn {ennemi.nom} bloque la route !")

        while h.pv > 0 and ennemi.pv > 0:
            clean()
            print(f"📍 {zone} | 🛡️ Niveau {h.niveau} | ⚔️ {h.arme_nom}")
            print(f"{h.nom:<12} {barre_vie(h.pv, h.max_pv)}")
            print(f"{ennemi.nom:<12} {barre_vie(ennemi.pv, ennemi.pv if ennemi.pv > 0 else 1)}")
            print("-" * 60)

            for i, c in enumerate(h.competences):
                print(f"{i + 1}. {c['nom']:<18} (Dé:{c['seuil']}+ | {c['desc']})")

            try:
                choix_atk = int(input("\nAction > ")) - 1
                atk = h.competences[choix_atk]
            except:
                atk = h.competences[0]

            jet = d20()
            print(f"\n🎲 Jet de dé : {jet}")

            # Résolution Attaque
            if jet == 20:
                dmg = lancer_degats(atk['degats']) * 2
                print(f"🔥 CRITIQUE ! {atk['nom']} inflige {dmg} dégâts !")
                ennemi.pv -= dmg
            elif jet >= atk['seuil']:
                dmg = lancer_degats(atk['degats'])
                print(f"⚔️ Réussite ! {atk['nom']} inflige {dmg} dégâts.")
                ennemi.pv -= dmg
            else:
                print(f"🛡️ Raté ! Le jet était trop faible pour {atk['nom']}.")

            # Tour Ennemi
            if ennemi.pv > 0:
                time.sleep(0.8)
                jet_e = d20()
                if jet_e >= h.ca:
                    dmg_e = lancer_degats(ennemi.degats)
                    h.pv -= dmg_e
                    print(f"👹 {ennemi.nom} contre-attaque : -{dmg_e} PV.")
                else:
                    print(f"🛡️ Vous esquivez l'attaque ennemi !")

            time.sleep(1.2)

        if h.pv > 0:
            cinematique(f"Victoire !\nLe {ennemi.nom} est terrassé.")
            if ennemi.loot:
                h.arme_nom = ennemi.loot["nom"]
                h.arme_degats = ennemi.loot["degats"]
                # On met à jour l'attaque de base avec l'arme trouvée
                h.competences[0]['degats'] = h.arme_degats
                cinematique(f"Butin : {h.arme_nom} !\nVos attaques de base sont renforcées.")
            if zone != "ANTRE DU BOSS": level_up(h)

    if h.pv > 0:
        cinematique(f"LÉGENDE ACCOMPLIE.\nAube-Terre est sauvée par {h.nom}.")
    else:
        cinematique("Mort au combat...\nVotre voyage s'arrête ici.")


if __name__ == "__main__":
    jouer()