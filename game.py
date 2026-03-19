# game.py — Moteur de Jeu de Role Multijoueur et Interface

import os
import time
from engine import (
    Hero, Monstre, barre, d20,
    attaque_hero, attaque_monstre, invoquer
)
from data import MONSTRES, HEROES

# --- UTILITAIRES D'AFFICHAGE ---

def effacer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_etat_global(equipe_heros, equipe_monstres):
    """Affiche le tableau de bord global pour tous les combattants avec couleurs."""
    effacer_ecran()
    C_RESET = "\033[0m"
    C_VERT = "\033[32m"
    C_ROUGE = "\033[31m"
    C_CYAN = "\033[36m"
    
    print("=== ETAT DU CHAMP DE BATAILLE ===")
    
    print("\n[ GROUPE DES HEROS ]")
    for i, h in enumerate(equipe_heros):
        statut = "VIVANT" if h.pv > 0 else "KO"
        col = C_CYAN if h.eveil else C_VERT
        eveil_txt = "(Eveil Actif)" if h.eveil else ""
        
        # Affichage propre sur une seule ligne avec la couleur appliquee globalement
        print(f"{col}H{i+1}. {h.nom:<15} | {barre(h.pv, h.max_pv)} | {statut} {eveil_txt}{C_RESET}")
        
        if h.invocation and h.invocation.pv > 0:
            print(f"{C_VERT}    -> Invoc: {h.invocation.nom:<10} | {barre(h.invocation.pv, h.invocation.max_pv)}{C_RESET}")

    print("\n[ GROUPE DES MONSTRES (MJ) ]")
    for i, m in enumerate(equipe_monstres):
        statut = "VIVANT" if m.pv > 0 else "KO"
        buff_txt = "(Buff Actif)" if m.buff_actif else ""
        
        print(f"{C_ROUGE}M{i+1}. {m.nom:<15} | {barre(m.pv, m.max_pv)} | {statut} {buff_txt}{C_RESET}")
        
    print("=================================\n")

# --- MENUS ET ARCHIVES ---

def afficher_fiches_heros():
    """Affiche le menu de consultation des fiches de personnages."""
    while True:
        effacer_ecran()
        print("--- ARCHIVES DES HEROS ---\n")
        print("1. Soundjata Keita")
        print("2. Abla Pokou")
        print("3. Moro Naba")
        print("4. Retour au menu principal\n")

        choix = input("Quel heros veux-tu inspecter ? (1/2/3/4) > ")

        if choix == "4":
            break
            
        cle = None
        if choix == "1": cle = "Soundjata"
        elif choix == "2": cle = "Abla Pokou"
        elif choix == "3": cle = "Moro Naba"

        if cle:
            h = HEROES[cle]
            effacer_ecran()
            print("+" + "-" * 38 + "+")
            print(f"| {h['nom']:^36} |")
            print("+" + "-" * 38 + "+")
            print(f" Arme       : {h['arme']}")
            print(f" PV de base : {h['pv_base']}")
            print(f" Type       : {h['type'].capitalize()}")
            print(f" Affinite   : {h['affinite']}")
            
            print("\n Techniques de combat :")
            for t in h['techniques']:
                print(f"  - {t['nom']:<20} (Degats base: {t['base']}, Seuil reussite: {t['seuil']})")
                
            print(f"\n Invocation (Niveau 3) :")
            print(f"  - {h['invocation']['nom']} | PV: {h['invocation']['pv']} | Degats: {h['invocation']['degats']}")
            
            input("\n[ Appuyez sur Entree pour revenir aux archives ]")


# --- MECANIQUE DE PARTIE ---

def configurer_partie():
    """Phase 1 : Le Maitre du Jeu configure les participants."""
    effacer_ecran()
    print("=== PREPARATION DU COMBAT ===")
    
    try:
        nb_joueurs = int(input("\nCombien de joueurs (Heros) participent ? > "))
    except ValueError:
        nb_joueurs = 1
        
    equipe_heros = []
    noms_dispos = list(HEROES.keys())
    
    for i in range(nb_joueurs):
        print(f"\nChoix pour le Joueur {i+1} :")
        for j, nom in enumerate(noms_dispos):
            print(f"{j+1}. {nom}")
        try:
            choix = int(input("Numero du Heros > ")) - 1
            equipe_heros.append(Hero(noms_dispos[choix]))
        except (ValueError, IndexError):
            print("Choix invalide, Soundjata selectionne par defaut.")
            equipe_heros.append(Hero("Soundjata"))

    try:
        nb_monstres = int(input("\nCombien de monstres le Maitre du Jeu deploie-t-il ? > "))
    except ValueError:
        nb_monstres = 1
        
    equipe_monstres = []
    for i in range(nb_monstres):
        print(f"\nChoix pour le Monstre {i+1} :")
        for niv, data in MONSTRES.items():
            print(f"{niv}. {data['nom']} (Niveau {niv} | {data['pv']} PV)")
        try:
            choix = int(input("Niveau du monstre > "))
            equipe_monstres.append(Monstre(MONSTRES[choix]))
        except (ValueError, KeyError):
            print("Choix invalide, Mamlambo selectionne par defaut.")
            equipe_monstres.append(Monstre(MONSTRES[1]))

    return equipe_heros, equipe_monstres


def lancer_combat():
    """Phase 2 : La boucle principale de resolution."""
    equipe_heros, equipe_monstres = configurer_partie()
    
    effacer_ecran()
    print("Calcul de l'initiative globale (Jet de d20)...")
    combattants = equipe_heros + equipe_monstres
    for c in combattants:
        c.initiative = d20()
        print(f"- {c.nom} a obtenu {c.initiative}")
        
    combattants.sort(key=lambda x: x.initiative, reverse=True)
    time.sleep(3)

    tour = 1
    while any(h.pv > 0 for h in equipe_heros) and any(m.pv > 0 for m in equipe_monstres):
        afficher_etat_global(equipe_heros, equipe_monstres)
        print(f"--- DEBUT DU TOUR {tour} ---")
        
        for perso in combattants:
            if perso.pv <= 0:
                continue
            
            if not any(h.pv > 0 for h in equipe_heros) or not any(m.pv > 0 for m in equipe_monstres):
                break

            print(f"\n>>> C'est au tour de : {perso.nom}")
            time.sleep(1)
            
            if isinstance(perso, Hero):
                print("Actions disponibles :")
                print(f"1. Attaquer avec {perso.techniques[0]['nom']}")
                print(f"2. Attaquer avec {perso.techniques[1]['nom']}")
                
                options = ["1", "2"]
                if perso.peut_eveiller():
                    print("3. Activer l'Eveil (Passe le tour d'attaque)")
                    options.append("3")
                if perso.peut_invoquer():
                    print("4. Invoquer un allie")
                    options.append("4")
                if perso.invocation is not None and perso.invocation.pv > 0:
                    print("5. Ordre a l'invocation : Attaquer")
                    options.append("5")
                
                choix_action = input("Votre choix > ")
                
                if choix_action == "3" and "3" in options:
                    perso.activer_eveil()
                    print(f"L'Eveil est active. Les caracteristiques de {perso.nom} augmentent.")
                    time.sleep(2)
                    continue
                    
                if choix_action == "4" and "4" in options:
                    invoquer(perso)
                    print(f"{perso.nom} realise son invocation !")
                    time.sleep(2)
                    continue

                print("\nCibles ennemies valides :")
                cibles = [m for m in equipe_monstres if m.pv > 0]
                for i, m in enumerate(cibles):
                    print(f"{i+1}. {m.nom} ({m.pv} PV)")
                
                try:
                    choix_cible = int(input("Quelle cible attaquer (numero) ? > ")) - 1
                    cible = cibles[choix_cible]
                except (ValueError, IndexError):
                    cible = cibles[0]
                
                if choix_action == "5" and "5" in options:
                    print(f"L'invocation de {perso.nom} attaque {cible.nom} !")
                    dmg = perso.invocation.degats
                    cible.pv -= dmg
                    print(f"Touche ! {dmg} degats infliges.")
                else:
                    tech = perso.techniques[int(choix_action) - 1] if choix_action in ["1", "2"] else perso.techniques[0]
                    dmg, touche = attaque_hero(perso, cible, tech)
                    if touche:
                        print(f"Touche ! {dmg} degats infliges a {cible.nom}.")
                    else:
                        print("L'attaque a echoue.")
                
                time.sleep(2)
                
            elif isinstance(perso, Monstre):
                print("Actions du Maitre du Jeu :")
                print("1. Attaquer un heros")
                print(f"2. Se soigner (+{perso.valeur_soin} PV)")
                print(f"3. Se buffer (+{perso.valeur_buff} Degats a la prochaine attaque)")
                
                choix_mj = input("Choix du MJ > ")
                
                if choix_mj == "2":
                    soin = perso.se_soigner()
                    print(f"Action MJ : {perso.nom} recupere {soin} PV.")
                elif choix_mj == "3":
                    bonus = perso.activer_buff()
                    print(f"Action MJ : {perso.nom} accumule de la puissance (+{bonus} degats).")
                else:
                    print("\nCibles heros valides :")
                    cibles = [h for h in equipe_heros if h.pv > 0]
                    for i, h in enumerate(cibles):
                        print(f"{i+1}. {h.nom} ({h.pv} PV)")
                    
                    try:
                        choix_cible = int(input("Cible du MJ (numero) ? > ")) - 1
                        cible = cibles[choix_cible]
                    except (ValueError, IndexError):
                        cible = cibles[0]
                    
                    dmg, touche = attaque_monstre(cible, perso)
                    if touche:
                        print(f"Action MJ : {perso.nom} attaque et inflige {dmg} degats a {cible.nom}.")
                    else:
                        print(f"Action MJ : {perso.nom} rate son attaque.")
                
                time.sleep(2)
                
        tour += 1

    afficher_etat_global(equipe_heros, equipe_monstres)
    print("=== FIN DU COMBAT ===")
    if any(h.pv > 0 for h in equipe_heros):
        print("RESULTAT : VICTOIRE DES JOUEURS")
    else:
        print("RESULTAT : VICTOIRE DU MAITRE DU JEU")
    
    input("\n[ Appuyez sur Entree pour revenir au menu principal ]")

# --- POINT D'ENTREE ---

def menu_principal():
    """Le vrai point d'entree du programme."""
    while True:
        effacer_ecran()
        print("*" * 35)
        print("* LEGENDES AFRICAINES : L'EPOPEE *")
        print("*" * 35 + "\n")
        
        print("1. Lancer l'Aventure (Multijoueur)")
        print("2. Consulter les Fiches des Heros")
        print("3. Quitter le jeu\n")
        
        choix = input("Que voulez-vous faire ? (1/2/3) > ")
        
        if choix == "1":
            lancer_combat()
        elif choix == "2":
            afficher_fiches_heros()
        elif choix == "3":
            print("\nMerci d'avoir joue. Au revoir !")
            break

if __name__ == "__main__":
    menu_principal()