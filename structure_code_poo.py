import random
import time


# --- STRUCTURE POO (BASES) ---
class Creature:
    def __init__(self, nom, pv, ca, type_degat):
        self.nom = nom
        self.pv = pv
        self.max_pv = pv
        self.ca = ca  # Score à battre pour toucher
        self.type_degat = type_degat
        self.initiative = 0

    def lancer_initiative(self):
        self.initiative = random.randint(1, 20)
        return self.initiative

    def est_vivante(self):
        return self.pv > 0

    def recevoir_degats(self, montant):
        self.pv -= montant
        if self.pv < 0: self.pv = 0
        return montant


class Hero(Creature):
    def __init__(self, nom, pv, ca, type_degat, arme, histoire):
        super().__init__(nom, pv, ca, type_degat)
        self.arme = arme
        self.histoire = histoire


class Monstre(Creature):
    def __init__(self, nom, pv, ca, type_degat, resistance):
        super().__init__(nom, pv, ca, type_degat)
        self.resistance = resistance  # Type de dégât réduit par 2

    def recevoir_degats(self, montant, type_attaque):
        # Polymorphisme : gestion de la résistance
        if type_attaque == self.resistance:
            montant //= 2
            print(f"🛡️  Le {self.nom} est résistant au type {type_attaque} !")
        return super().recevoir_degats(montant)


# --- NOUVEAU CATALOGUE ÉLARGI ---

catalogue_heros = [
    # Guerriers Classiques
    Hero("Shaka Zulu", 110, 15, "Percant", "Lance Iklwa", "Roi Zoulou, maître de la tactique"),
    Hero("Reine Amina", 95, 17, "Tranchant", "Sabre de Zaria", "Conquérante Haoussa indomptable"),

    # Nouveaux Héros
    Hero("Samory Touré", 100, 16, "Percant", "Fusil de l'Empire", "Le Lion du Soudan, résistant Mandingue"),
    Hero("Makeda", 90, 18, "Magique", "Sceptre de Saba", "La Reine de Saba, sagesse éthiopienne"),
    Hero("Behanzin", 105, 14, "Tranchant", "Recade d'Abomey", "Le Roi Requin du Dahomey"),
    Hero("Nzambi", 80, 15, "Magique", "Bâton de Création", "Esprit protecteur du bassin du Congo")
]

catalogue_monstres = [
    # Monstres de base
    Monstre("Grootslang", 130, 13, "Contondant", "Tranchant"),
    Monstre("Popobawa", 85, 16, "Magique", "Percant"),

    # Nouveaux Monstres Mythiques
    Monstre("Kongamato", 90, 15, "Percant", "Magique"),  # Ptérodactyle des marais (Zambie)
    Monstre("Ninki Nanka", 160, 12, "Feu", "Contondant"),  # Dragon-crocodile (Gambie)
    Monstre("Tikoloshe", 60, 18, "Poison", "Magique"),  # Esprit malin (Afrique du Sud)
    Monstre("Kikiyaon", 110, 14, "Tranchant", "Feu")  # Homme-oiseau terrifiant (Afrique de l'Ouest)
]


# --- MOTEUR DE JEU (REPL) ---

def combat():
    print("🌍 --- LÉGENDES D'AUBE-TERRE : LE COMBAT FINAL --- 🌍\n")

    # 1. Sélection des Héros
    equipe_joueur = []
    try:
        nb_heros = int(input("Combien de héros dans votre groupe ? "))
        for i in range(nb_heros):
            print("\n--- Choisissez votre héros ---")
            for idx, h in enumerate(catalogue_heros):
                print(f"{idx} - {h.nom} | {h.histoire}")
            choix = int(input("Votre choix (numéro) : "))
            equipe_joueur.append(catalogue_heros[choix])
    except:
        print("Erreur de saisie. On commence avec Shaka par défaut.")
        equipe_joueur = [catalogue_heros[0]]

    # 2. Génération des Monstres
    nb_ennemis = int(input("\nCombien de monstres voulez-vous affronter ? "))
    equipe_ennemis = [random.choice(catalogue_monstres) for _ in range(nb_ennemis)]

    # 3. Initiative
    combattants = equipe_joueur + equipe_ennemis
    for c in combattants:
        c.lancer_initiative()
    combattants.sort(key=lambda x: x.initiative, reverse=True)  # Tri par initiative

    # 4. Boucle de Combat
    while any(h.est_vivante() for h in equipe_joueur) and any(m.est_vivante() for m in equipe_ennemis):
        for perso in combattants:
            if not perso.est_vivante(): continue

            if isinstance(perso, Hero):
                # Tour du Joueur
                cibles = [m for m in equipe_ennemis if m.est_vivante()]
                if not cibles: break
                print(f"\n👉 C'est au tour de {perso.nom} ({perso.pv} PV)")
                print("Cibles : " + ", ".join([f"{i}:{c.nom}({c.pv}PV)" for i, c in enumerate(cibles)]))
                c_idx = int(input("Cible : "))
                cible = cibles[c_idx]
            else:
                # Tour du Monstre
                cibles = [h for h in equipe_joueur if h.est_vivante()]
                if not cibles: break
                cible = random.choice(cibles)
                print(f"\n👹 {perso.nom} attaque {cible.nom} !")

            # Jet de dé
            jet = random.randint(1, 20)
            if jet == 20:
                dmg = 30  # Critique
                print(f"🔥 CRITIQUE ! {cible.nom} subit {dmg} dégâts !")
                cible.recevoir_degats(dmg, perso.type_degat) if isinstance(cible, Monstre) else cible.recevoir_degats(
                    dmg)
            elif jet >= cible.ca:
                dmg = random.randint(10, 20)
                print(f"⚔️ Touche ! {dmg} dégâts.")
                cible.recevoir_degats(dmg, perso.type_degat) if isinstance(cible, Monstre) else cible.recevoir_degats(
                    dmg)
            else:
                print("🛡️ Raté !")
            time.sleep(0.5)

    if any(h.est_vivante() for h in equipe_joueur):
        print("\n✨ VICTOIRE ! La terre est sauvée !")
    else:
        print("\n💀 DÉFAITE... Les monstres ont gagné.")


if __name__ == "__main__":
    combat()