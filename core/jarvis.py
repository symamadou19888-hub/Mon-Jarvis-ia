import json
import os
from agent_manager import AgentManager
from command_manager import CommandManager
from memory_manager import MemoryManager
from skill_manager import SkillManager
from brain_manager import BrainManager
from logger import Logger
from system_checker import SystemChecker
from task_manager import TaskManager
from project_manager import ProjectManager
from data_manager import DataManager
from event_manager import EventManager
from context_manager import ContextManager
from knowledge_manager import KnowledgeManager
from decision_engine import DecisionEngine
from ai_engine import AIEngine
from contexte_ia import charger_contexte


class Jarvis:
    def __init__(self):
        self.config = self.charger_config()
        self.memory_manager = MemoryManager()
        self.agent_manager = AgentManager()
        self.command_manager = CommandManager()
        self.skill_manager = SkillManager()
        self.brain_manager = BrainManager()
        self.logger = Logger()
        self.system_checker = SystemChecker()
        self.task_manager = TaskManager()
        self.project_manager = ProjectManager()
        self.data_manager = DataManager()
        self.event_manager = EventManager()
        self.context_manager = ContextManager()
        self.knowledge_manager = KnowledgeManager()

        self.ai_engine = AIEngine()
        self.contexte = charger_contexte()
        self.decision_engine = DecisionEngine(
            self.brain_manager,
            self.agent_manager
        )

        self.nom = self.config["nom"]
        self.version = self.config["version"]

    def charger_config(self):
        chemin = os.path.join("config", "settings.json")

        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    def start(self):
        if not self.system_checker.verifier():
            print("Erreur : système incomplet.")
            return

        self.logger.enregistrer("Démarrage de Jarvis")

        print(f"{self.nom} version {self.version} démarré.")
        print("Mémoire chargée.")
        self.agent_manager.afficher_agents()
        self.skill_manager.afficher_skills()
        self.brain_manager.afficher_brain()
        self.task_manager.afficher_taches()
        self.project_manager.afficher_projets()
        self.knowledge_manager.afficher_connaissances()
        print("Système prêt.")

        while True:
            commande = input("Vous : ")

            if commande.lower() in ["quitter", "exit", "stop"]:
                self.logger.enregistrer("Arrêt de Jarvis")
                print("Jarvis arrêté.")
                break

            self.traiter_commande(commande)

    def traiter_commande(self, commande):
        self.logger.enregistrer(f"Commande reçue : {commande}")

        resultat = self.command_manager.traiter(commande)

        if "Commande inconnue" in resultat:
            agent = self.decision_engine.choisir_agent(commande)
            print(f"[Agent : {agent}]")

            contexte_agent = self.decision_engine.obtenir_contexte_agent(agent)
            contexte_complet = self.contexte + "\n\n" + contexte_agent

            historique = self.memory_manager.obtenir_historique_recent()
            reponse = self.ai_engine.demander(commande, contexte=contexte_complet, historique=historique)
            print(reponse)
            self.memory_manager.ajouter_echange(commande, reponse)

        else:
            print(resultat)
