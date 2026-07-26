import os

DOSSIER_AUTORISE = os.getcwd()

def lire_fichier(chemin):
    chemin_complet = os.path.abspath(chemin)
    if not chemin_complet.startswith(DOSSIER_AUTORISE):
        return "Erreur : accès refusé en dehors du projet."
    if not os.path.exists(chemin_complet):
        return f"Erreur : le fichier {chemin} n'existe pas."
    with open(chemin_complet, "r", encoding="utf-8") as f:
        return f.read()

def ecrire_fichier(chemin, contenu):
    chemin_complet = os.path.abspath(chemin)
    if not chemin_complet.startswith(DOSSIER_AUTORISE):
        return "Erreur : accès refusé en dehors du projet."
    with open(chemin_complet, "w", encoding="utf-8") as f:
        f.write(contenu)
    return f"Fichier {chemin} écrit avec succès."
