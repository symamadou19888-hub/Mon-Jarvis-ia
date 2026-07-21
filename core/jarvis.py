import json
import os
from agent_manager import AgentManager
from command_manager import CommandManager
from memory_manager import MemoryManager
from skill_manager import SkillManager


class Jarvis:
    def __init__(self):
        self.config = self.charger_config()
        self.memory_manager = MemoryManager()
        self.agent_manager = AgentManager()
        self.command_manager = CommandManager()
        self.skill_manager = SkillManager()

        self.nom = self.config["nom"]
        self.version = self.config["version"]

    def charger_config(self):
        chemin = os.path.join("config", "settings.json")

        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    def start(self):
        print(f"{self.nom} version {self.version} démarré.")
        print("Mémoire chargée.")
        self.agent_manager.afficher_agents()
        self.skill_manager.afficher_skills()
        print("Système prêt.")

        while True:
            commande = input("Vous : ")

            if commande.lower() in ["quitter", "exit", "stop"]:
                print("Jarvis arrêté.")
                break

            self.traiter_commande(commande)

    def traiter_commande(self, commande):
        resultat = self.command_manager.traiter(commande)
        print(resultat)
