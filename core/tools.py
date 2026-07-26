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
