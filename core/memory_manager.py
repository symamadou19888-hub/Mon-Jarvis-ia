import json
import os


class MemoryManager:
    def __init__(self):
        self.chemin = os.path.join("memory", "memory.json")
        self.memoire = self.charger()

    def charger(self):
        with open(self.chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    def sauvegarder(self):
        with open(self.chemin, "w", encoding="utf-8") as fichier:
            json.dump(self.memoire, fichier, indent=4, ensure_ascii=False)

    def ajouter_souvenir(self, souvenir):
        self.memoire["souvenirs"].append(souvenir)
        self.sauvegarder()
