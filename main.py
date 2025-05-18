import json
import os

FICHIER = "bibliotheque.json"

def charger_bibliotheque():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def sauvegarder_bibliotheque(bibliotheque):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

def generer_id(bibliotheque):
    if not bibliotheque:
        return 1
    else:
        return max(livre["ID"] for livre in bibliotheque) + 1

def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    for livre in bibliotheque:
        lu = "✅" if livre["Lu"] else "❌"
        note = livre["Note"] if livre["Note"] is not None else "-"
        commentaire = livre.get("Commentaire", "")
        print(f'ID: {livre["ID"]} | {livre["Titre"]} - {livre["Auteur"]} ({livre["Année"]}) | Lu: {lu} | Note: {note}')
        if commentaire:
            print(f'  Commentaire: {commentaire}')

def ajouter_livre(bibliotheque):
    titre = input("Titre du livre : ")
    auteur = input("Auteur : ")
    try:
        annee = int(input("Année de publication : "))
    except ValueError:
        print("Année invalide. Livre non ajouté.")
        return
    id_unique = generer_id(bibliotheque)
    nouveau_livre = {
        "ID": id_unique,
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    bibliotheque.append(nouveau_livre)
    print("Livre ajouté !")

def supprimer_livre(bibliotheque):
    try:
        id_a_supprimer = int(input("Entrez l'ID du livre à supprimer : "))
    except ValueError:
        print("ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_a_supprimer:
            confirmer = input(f"Confirmez la suppression de '{livre['Titre']}' ? (o/n) : ").lower()
            if confirmer == "o":
                bibliotheque.remove(livre)
                print("Livre supprimé.")
            else:
                print("Suppression annulée.")
            return
    print("Livre non trouvé.")

def rechercher_livre(bibliotheque):
    mot_clef = input("Entrez un mot-clé à rechercher (titre ou auteur) : ").lower()
    resultats = [livre for livre in bibliotheque if mot_clef in livre["Titre"].lower() or mot_clef in livre["Auteur"].lower()]
    if not resultats:
        print("Aucun livre trouvé avec ce mot-clé.")
    else:
        print("Résultats de la recherche :")
        for livre in resultats:
            lu = "✅" if livre["Lu"] else "❌"
            note = livre["Note"] if livre["Note"] is not None else "-"
            print(f'ID: {livre["ID"]} | {livre["Titre"]} - {livre["Auteur"]} ({livre["Année"]}) | Lu: {lu} | Note: {note}')

def marquer_lu(bibliotheque):
    try:
        id_livre = int(input("Entrez l'ID du livre à marquer comme lu : "))
    except ValueError:
        print("ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_livre:
            livre["Lu"] = True
            try:
                note = int(input("Entrez une note sur 10 : "))
                if 0 <= note <= 10:
                    livre["Note"] = note
                else:
                    print("Note invalide, doit être entre 0 et 10.")
                    livre["Note"] = None
            except ValueError:
                print("Note invalide, aucune note enregistrée.")
                livre["Note"] = None
            commentaire = input("Ajoutez un commentaire (optionnel) : ")
            livre["Commentaire"] = commentaire
            print(f"Le livre '{livre['Titre']}' a été marqué comme lu.")
            return
    print("Livre non trouvé.")

def afficher_par_etat(bibliotheque):
    choix = input("Afficher les livres (l)us ou (n)on lus ? ").lower()
    if choix == "l":
        livres = [livre for livre in bibliotheque if livre["Lu"]]
    elif choix == "n":
        livres = [livre for livre in bibliotheque if not livre["Lu"]]
    else:
        print("Choix invalide.")
        return
    if not livres:
        print("Aucun livre correspondant.")
        return
    for livre in livres:
        note = livre["Note"] if livre["Note"] is not None else "-"
        print(f'ID: {livre["ID"]} | {livre["Titre"]} - {livre["Auteur"]} ({livre["Année"]}) | Note: {note}')

def trier_livres(bibliotheque):
    print("Trier par :")
    print("1. Année")
    print("2. Auteur")
    print("3. Note")
    choix = input("Choix : ")
    if choix == "1":
        livres_tries = sorted(bibliotheque, key=lambda x: x["Année"])
    elif choix == "2":
        livres_tries = sorted(bibliotheque, key=lambda x: x["Auteur"].lower())
    elif choix == "3":
        livres_tries = sorted(bibliotheque, key=lambda x: (x["Note"] is None, x["Note"]), reverse=True)
    else:
        print("Choix invalide.")
        return
    for livre in livres_tries:
        lu = "✅" if livre["Lu"] else "❌"
        note = livre["Note"] if livre["Note"] is not None else "-"
        print(f'ID: {livre["ID"]} | {livre["Titre"]} - {livre["Auteur"]} ({livre["Année"]}) | Lu: {lu} | Note: {note}')

def menu():
    print("\n===== MENU =====")
    print("1. Afficher tous les livres")
    print("2. Ajouter un livre")
    print("3. Supprimer un livre")
    print("4. Rechercher un livre")
    print("5. Marquer un livre comme lu")
    print("6. Afficher les livres lus ou non lus")
    print("7. Trier les livres")
    print("8. Quitter")
    print("================")

def main():
    bibliotheque = charger_bibliotheque()
    while True:
        menu()
        choix = input("Choisis une option : ")
        if choix == "1":
            afficher_livres(bibliotheque)
        elif choix == "2":
            ajouter_livre(bibliotheque)
        elif choix == "3":
            supprimer_livre(bibliotheque)
        elif choix == "4":
            rechercher_livre(bibliotheque)
        elif choix == "5":
            marquer_lu(bibliotheque)
        elif choix == "6":
            afficher_par_etat(bibliotheque)
        elif choix == "7":
            trier_livres(bibliotheque)
        elif choix == "8":
            sauvegarder_bibliotheque(bibliotheque)
            print("Bibliothèque sauvegardée. Au revoir !")
            break
        else:
            print("Option invalide, réessaie.")

if __name__ == "__main__":
    main()


