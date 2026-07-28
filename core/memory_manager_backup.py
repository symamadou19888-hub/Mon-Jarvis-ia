import json
import os
from datetime import datetime


class MemoryManager:
    def __init__(self):
        self.chemin = os.path.join("memory", "memory.json")
        self.memoire = self.charger()

    def charger(self):
        if not os.path.exists(self.chemin):
            memoire = {
                "court_terme": [],
                "long_terme": {
                    "projets": [],
                    "decisions": [],
                    "preferences_utilisateur": [],
                    "connaissances": [],
                    "erreurs": []
                }
            }

            with open(self.chemin, "w", encoding="utf-8") as fichier:
                json.dump(memoire, fichier, indent=4, ensure_ascii=False)

            return memoire

        with open(self.chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    def sauvegarder(self):
        with open(self.chemin, "w", encoding="utf-8") as fichier:
            json.dump(self.memoire, fichier, indent=4, ensure_ascii=False)

    def ajouter_echange(self, question, reponse):
        self.memoire["court_terme"].append({
            "question": question,
            "reponse": reponse,
            "date": datetime.now().isoformat()
        })

        self.memoire["court_terme"] = self.memoire["court_terme"][-5:]
        self.sauvegarder()

    def obtenir_historique_recent(self, nombre=5):
        return self.memoire["court_terme"][-nombre:]

    def memoriser(self, categorie, contenu):
        if categorie not in self.memoire["long_terme"]:
            return False

        self.memoire["long_terme"][categorie].append({
            "contenu": contenu,
            "date": datetime.now().isoformat()
        })

        self.sauvegarder()
        return True

    def rechercher_souvenir(self, mot_cle):
        resultats = []

        for categorie, souvenirs in self.memoire["long_terme"].items():
            for souvenir in souvenirs:
                if mot_cle.lower() in souvenir["contenu"].lower():
                    resultats.append({
                        "categorie": categorie,
                        "contenu": souvenir["contenu"],
                        "date": souvenir["date"]
                    })

        return resultats
