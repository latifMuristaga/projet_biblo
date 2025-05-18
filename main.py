import json
import os

# Fichier JSON où on stocke la bibliothèque
FICHIER_BIBLIOTHEQUE = "bibliotheque.json"

# Charger la bibliothèque depuis le fichier JSON
def charger_bibliotheque():
    if os.path.exists(FICHIER_BIBLIOTHEQUE):
        with open(FICHIER_BIBLIOTHEQUE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

# Sauvegarder la bibliothèque dans le fichier JSON
def sauvegarder_bibliotheque(bibliotheque):
    with open(FICHIER_BIBLIOTHEQUE, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

# Générer un ID unique pour chaque livre
def generer_id(bibliotheque):
    if not bibliotheque:
        return 1
    else:
        ids = [livre["ID"] for livre in bibliotheque]
        return max(ids) + 1

# Afficher tous les livres
def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    for livre in bibliotheque:
        lu = "✓" if livre["Lu"] else "✗"
        note = livre["Note"] if livre["Note"] is not None else "N/A"
        print(f'ID: {livre["ID"]} | Titre: {livre["Titre"]} | Auteur: {livre["Auteur"]} | Année: {livre["Année"]} | Lu: {lu} | Note: {note}')

# Ajouter un livre
def ajouter_livre(bibliotheque):
    titre = input("Titre : ").strip()
    auteur = input("Auteur : ").strip()
    while True:
        annee = input("Année de publication : ").strip()
        if annee.isdigit():
            annee = int(annee)
            break
        else:
            print("Veuillez entrer une année valide (nombre).")
    id_livre = generer_id(bibliotheque)
    nouveau_livre = {
        "ID": id_livre,
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    bibliotheque.append(nouveau_livre)
    print(f'Livre "{titre}" ajouté avec l’ID {id_livre}.')

# Supprimer un livre par ID
def supprimer_livre(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    try:
        id_supp = int(input("Entrez l’ID du livre à supprimer : "))
    except ValueError:
        print("ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_supp:
            confirmer = input(f"Confirmez-vous la suppression du livre '{livre['Titre']}' ? (o/n) : ").lower()
            if confirmer == "o":
                bibliotheque.remove(livre)
                print("Livre supprimé.")
            else:
                print("Suppression annulée.")
            return
    print("Livre non trouvé.")

# Rechercher un livre par mot-clé dans titre ou auteur
def rechercher_livre(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    mot_cle = input("Entrez un mot-clé pour la recherche : ").lower()
    resultats = []
    for livre in bibliotheque:
        if mot_cle in livre["Titre"].lower() or mot_cle in livre["Auteur"].lower():
            resultats.append(livre)
    if not resultats:
        print("Aucun livre trouvé.")
    else:
        print(f"{len(resultats)} livre(s) trouvé(s) :")
        for livre in resultats:
            lu = "✓" if livre["Lu"] else "✗"
            note = livre["Note"] if livre["Note"] is not None else "N/A"
            print(f'ID: {livre["ID"]} | Titre: {livre["Titre"]} | Auteur: {livre["Auteur"]} | Année: {livre["Année"]} | Lu: {lu} | Note: {note}')

# Marquer un livre comme lu et ajouter note + commentaire
def marquer_comme_lu(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    try:
        id_lu = int(input("Entrez l’ID du livre à marquer comme lu : "))
    except ValueError:
        print("ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_lu:
            livre["Lu"] = True
            while True:
                note = input("Attribuez une note sur 10 (laisser vide pour ne pas noter) : ").strip()
                if note == "":
                    livre["Note"] = None
                    break
                elif note.isdigit() and 0 <= int(note) <= 10:
                    livre["Note"] = int(note)
                    break
                else:
                    print("Note invalide, entrez un nombre entre 0 et 10.")
            commentaire = input("Ajoutez un commentaire (optionnel) : ").strip()
            livre["Commentaire"] = commentaire
            print(f'Livre "{livre["Titre"]}" marqué comme lu.')
            return
    print("Livre non trouvé.")

# Afficher les livres selon leur état lu ou non lu
def afficher_selon_etat(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
    choix = input("Afficher (l)us ou (n)on lus ? ").lower()
    if choix not in ["l", "n"]:
        print("Choix invalide.")
        return
    filtre = True if choix == "l" else False
    filtres_livres = [livre for livre in bibliotheque if livre["Lu"] == filtre]
    if not filtres_livres:
        print("Aucun livre correspondant.")
    else:
        for livre in filtres_livres:
            note = livre["Note"] if livre["Note"] is not None else "N/A"
            print(f'ID: {livre["ID"]} | Titre: {livre["Titre"]} | Auteur: {livre["Auteur"]} | Année: {livre["Année"]} | Note: {note}')

# Trier les livres
def trier_livres(bibliotheque):
    if not bibliotheque:
        print("La bibliothèque est vide.")
        return
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
        # Note None à la fin
        livres_tries = sorted(bibliotheque, key=lambda x: (x["Note"] is None, x["Note"]))
    else:
        print("Choix invalide.")
        return
    for livre in livres_tries:
        lu = "✓" if livre["Lu"] else "✗"
        note = livre["Note"] if livre["Note"] is not None else "N/A"
        print(f'ID: {livre["ID"]} | Titre: {livre["Titre"]} | Auteur: {livre["Auteur"]} | Année: {livre["Année"]} | Lu: {lu} | Note: {note}')

# Boucle principale
def menu():
    bibliotheque = charger_bibliotheque()
    while True:
        print("\n===== MENU =====")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher livres lus ou non lus")
        print("7. Trier les livres")
        print("8. Quitter")
        print("================")
        choix = input("Choisis une option : ").strip()

        if choix == "1":
            afficher_livres(bibliotheque)
        elif choix == "2":
            ajouter_livre(bibliotheque)
        elif choix == "3":
            supprimer_livre(bibliotheque)
        elif choix == "4":
            rechercher_livre(bibliotheque)
        elif choix == "5":
            marquer_comme_lu(bibliotheque)
        elif choix == "6":
            afficher_selon_etat(bibliotheque)
        elif choix == "7":
            trier_livres(bibliotheque)
        elif choix == "8":
            sauvegarder_bibliotheque(bibliotheque)
            print("Bibliothèque sauvegardée. Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    menu()



