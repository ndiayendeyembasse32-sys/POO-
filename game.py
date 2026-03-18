# game.py — Boucle principale

import os
import time
from engine import (
    Hero, Monstre, barre, cine, cine_intro_niveau, cine_evolution,
    attaque_hero, attaque_monstre,
    invoquer, tour_invocation
)
from data import MONSTRES


def choisir_hero():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Choisis ton héros :\n")
    print("1. Soundjata — Guerrier Mandingue (Tranchant)")
    print("2. Abla Pokou — Reine Baoulé (Magie)")
    print("3. Moro Naba — Chef Mossi (Feu)\n")

    choix = input("Choix > ")

    if choix == "2":
        return Hero("Abla Pokou")
    elif choix == "3":
        return Hero("Moro Naba")
    return Hero("Soundjata")


def afficher_etat(hero, monstre):
    os.system('cls' if os.name == 'nt' else 'clear')

    col = "\033[36m" if hero.eveil else "\033[34m"

    print(f"{col}{hero.nom:<12} {barre(hero.pv, hero.max_pv, col)}")
    print(f"\033[31m{monstre.nom:<12} {barre(monstre.pv, monstre.max_pv, '\033[31m')}\033[0m\n")

    if hero.invocation:
        print(f"Invocation : {hero.invocation.nom} ({hero.invocation.pv}/{hero.invocation.max_pv} PV)\n")


def combat(hero, monstre):
    cine_intro_niveau(monstre.niveau, monstre)

    while hero.pv > 0 and monstre.pv > 0:

        if hero.invocation:
            afficher_etat(hero, monstre)
            tour_invocation(hero, monstre)
            hero.maj_eveil()
            continue

        afficher_etat(hero, monstre)

        if hero.peut_eveiller():
            rep = input("ÉVEILLER ? (o/n) : ").lower()
            if rep == "o":
                hero.activer_eveil()
                print("\nMode ÉVEIL activé, tu passes ton tour...")
                time.sleep(1.5)

                dmg_m, touche_m = attaque_monstre(hero, monstre)
                if touche_m:
                    print(f"\033[31mReçu : -{dmg_m}\033[0m")
                else:
                    print("L'ennemi rate son attaque.")
                time.sleep(1.8)

                hero.maj_eveil()
                continue

        print("1.", hero.techniques[0]["nom"])
        print("2.", hero.techniques[1]["nom"])
        if hero.peut_invoquer():
            print(f"3. Invocation : {hero.invoc_data['nom']}")
        print()

        choix = input("Action > ")

        if choix == "3" and hero.peut_invoquer():
            invoquer(hero)
            print(f"\n{hero.invoc_data['nom']} est invoqué !")
            time.sleep(1.2)
            continue

        if choix not in ["1", "2"]:
            continue

        tech = hero.techniques[int(choix) - 1]

        dmg, touche = attaque_hero(hero, monstre, tech)
        if touche:
            print(f"\033[32mTouché ! -{dmg}\033[0m")
        else:
            print(f"\033[31mRaté !\033[0m")

        time.sleep(0.8)

        if monstre.pv <= 0:
            break

        dmg_m, touche_m = attaque_monstre(hero, monstre)
        if touche_m:
            print(f"\033[31mReçu : -{dmg_m}\033[0m")
        else:
            print("L'ennemi rate son attaque.")

        time.sleep(1.8)
        hero.maj_eveil()

    if hero.pv > 0:
        cine(f"{monstre.nom} vaincu !")

        if monstre.niveau < 5:
            hero.niveau += 1
            infos = hero.level_up()
            cine_evolution(hero, infos)
    else:
        cine("GAME OVER")


def jouer():
    hero = choisir_hero()

    for niv in range(1, 6):
        monstre = Monstre(MONSTRES[niv])

        hero.pv = hero.max_pv
        hero.invocation = None
        hero.invoc_tours = 0
        hero.invoc_utilisee = False
        hero.eveil = False
        hero.eveil_tours = 0

        combat(hero, monstre)
        if hero.pv <= 0:
            break

    if hero.pv > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔" + "═" * 40 + "╗")
        print("║           VICTOIRE FINALE !           ║")
        print("╚" + "═" * 40 + "╝\n")

        print("Après un combat titanesque, le héros terrasse Seth,")
        print("le Roi des Enfers, et met fin à son règne de chaos.")
        print("Les terres retrouvent enfin la paix, et ton nom")
        print("résonnera à jamais dans les légendes.\n")

        print("L’épopée s’achève… mais ton histoire ne fait que commencer.")
        input("\n[ Entrée ]")


if __name__ == "__main__":
    jouer()
