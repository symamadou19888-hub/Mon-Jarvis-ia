import os
import json
import requests

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

def supprimer_fichier(chemin):
    chemin_complet = os.path.abspath(chemin)
    if not chemin_complet.startswith(DOSSIER_AUTORISE):
        return "Erreur : accès refusé en dehors du projet."
    if not os.path.exists(chemin_complet):
        return f"Erreur : le fichier {chemin} n'existe pas, rien a supprimer."
    os.remove(chemin_complet)
    return f"Fichier {chemin} supprime avec succes."

def lister_fichiers(dossier="."):
    chemin_complet = os.path.abspath(dossier)
    if not chemin_complet.startswith(DOSSIER_AUTORISE):
        return "Erreur : accès refusé en dehors du projet."
    if not os.path.exists(chemin_complet):
        return f"Erreur : le dossier {dossier} n'existe pas."
    if not os.path.isdir(chemin_complet):
        return f"Erreur : {dossier} n'est pas un dossier."
    elements = os.listdir(chemin_complet)
    if not elements:
        return f"Le dossier {dossier} est vide."
    return "\n".join(sorted(elements))

def creer_dossier(chemin):
    chemin_complet = os.path.abspath(chemin)
    if not chemin_complet.startswith(DOSSIER_AUTORISE):
        return "Erreur : accès refusé en dehors du projet."
    if os.path.exists(chemin_complet):
        return f"Le dossier {chemin} existe deja."
    os.makedirs(chemin_complet)
    return f"Dossier {chemin} cree avec succes."

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


import base64

def _headers_github():
    token = os.getenv("GITHUB_TOKEN")
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

def github_lister_repos():
    url = "https://api.github.com/user/repos"
    try:
        r = requests.get(url, headers=_headers_github(), timeout=15)
        r.raise_for_status()
        repos = r.json()
        if not repos:
            return "Aucun depot trouve."
        return "\n".join(f"- {repo['full_name']}" for repo in repos)
    except Exception as e:
        return f"Erreur GitHub : {e}"

def github_lire_fichier(repo, chemin):
    url = f"https://api.github.com/repos/{repo}/contents/{chemin}"
    try:
        r = requests.get(url, headers=_headers_github(), timeout=15)
        r.raise_for_status()
        data = r.json()
        contenu_b64 = data.get("content", "")
        contenu_decode = base64.b64decode(contenu_b64).decode("utf-8")
        return contenu_decode
    except Exception as e:
        return f"Erreur GitHub : {e}"

def github_ecrire_fichier(repo, chemin, contenu, message="Mise a jour via Jarvis"):
    url = f"https://api.github.com/repos/{repo}/contents/{chemin}"
    try:
        sha = None
        r_check = requests.get(url, headers=_headers_github(), timeout=15)
        if r_check.status_code == 200:
            sha = r_check.json().get("sha")

        contenu_b64 = base64.b64encode(contenu.encode("utf-8")).decode("utf-8")
        payload = {"message": message, "content": contenu_b64}
        if sha:
            payload["sha"] = sha

        r = requests.put(url, headers=_headers_github(), json=payload, timeout=15)
        r.raise_for_status()
        return f"Fichier {chemin} envoye avec succes sur {repo}."
    except Exception as e:
        return f"Erreur GitHub : {e}"
