import os
import json

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

import requests as _requests

def rechercher_web(requete):
    api_key = os.getenv("TAVILY_API_KEY")
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": requete,
        "max_results": 3
    }
    try:
        reponse = _requests.post(url, json=payload, timeout=15)
        reponse.raise_for_status()
        data = reponse.json()
        resultats = data.get("results", [])
        texte = ""
        for r in resultats:
            texte += f"- {r.get('title')}: {r.get('content')[:200]}\n"
        return texte if texte else "Aucun resultat trouve."
    except Exception as e:
        return f"Erreur recherche web : {e}"

CHEMIN_DONNEES = os.path.join("data", "projets_taches.json")

def _charger_donnees():
    if not os.path.exists(CHEMIN_DONNEES):
        return {"projets": [], "taches": []}
    with open(CHEMIN_DONNEES, "r", encoding="utf-8") as f:
        return json.load(f)

def _sauvegarder_donnees(donnees):
    with open(CHEMIN_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

def creer_projet(nom):
    donnees = _charger_donnees()
    donnees["projets"].append({"nom": nom, "statut": "en cours"})
    _sauvegarder_donnees(donnees)
    return f"Projet '{nom}' cree avec succes."

def ajouter_tache(nom, projet=""):
    donnees = _charger_donnees()
    donnees["taches"].append({"nom": nom, "projet": projet, "statut": "en attente"})
    _sauvegarder_donnees(donnees)
    return f"Tache '{nom}' ajoutee avec succes."

def lister_projets():
    donnees = _charger_donnees()
    if not donnees["projets"]:
        return "Aucun projet enregistre."
    texte = ""
    for p in donnees["projets"]:
        texte += f"- {p['nom']} ({p['statut']})\n"
    return texte

def lister_taches():
    donnees = _charger_donnees()
    if not donnees["taches"]:
        return "Aucune tache enregistree."
    texte = ""
    for t in donnees["taches"]:
        texte += f"- {t['nom']} [{t['statut']}]"
        if t["projet"]:
            texte += f" (projet: {t['projet']})"
        texte += "\n"
    return texte
