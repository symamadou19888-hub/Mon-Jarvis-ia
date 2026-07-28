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
from mission_manager import MissionManager
from coordination_manager import CoordinationManager
from validation_manager import ValidationManager
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

        self.ai_engine = AIEngine(memory_manager=self.memory_manager)
        self.contexte = charger_contexte()
        self.decision_engine = DecisionEngine(
            self.brain_manager,
            self.agent_manager
        )
        self.mission_manager = MissionManager()
        self.coordination_manager = CoordinationManager(self.mission_manager, self.logger)
        self.validation_manager = ValidationManager(self.logger)

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
        self.mission_manager.afficher_missions()
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
            decision = self.decision_engine.decider(commande)
            agent = decision["agent"]
            analyse = decision["analyse"]

            self.coordination_manager.preparer(decision, commande)

            mission_id = None
            print(f"[Agent : {agent}]")
            if analyse.get("validation_requise"):
                print(f"[Attention : cette action peut avoir un impact important - risques : {analyse.get('risques')}]")
                mission = self.mission_manager.creer_mission(
                    nom=analyse.get("resume", commande),
                    objectif=commande,
                    agents=[agent],
                    priorite="haute" if analyse.get("risques") in ["moyen", "eleve"] else "normale"
                )
                mission_id = mission["id"]
                print(f"[Mission creee : {mission_id}]")
                self.coordination_manager.demarrer_mission(mission_id)

            contexte_agent = self.decision_engine.obtenir_contexte_agent(agent)
            contexte_complet = self.contexte + "\n\n" + contexte_agent

            historique = self.memory_manager.obtenir_historique_recent()
            reponse = self.ai_engine.demander(commande, contexte=contexte_complet, historique=historique)

            validation = self.validation_manager.valider(reponse, mission_id)
            if not validation["valide"]:
                print(f"[Validation echouee : {validation['avertissement']}]")
                if mission_id:
                    self.mission_manager.mettre_a_jour_statut(mission_id, "bloquee")
            elif validation.get("avertissement"):
                print(f"[Avertissement : {validation['avertissement']}]")

            self.coordination_manager.superviser_resultat(reponse, mission_id)
            reponse = self.coordination_manager.livrer(reponse, mission_id)

            print(reponse)
            if not reponse.startswith("Erreur IA"):
                reponse_a_memoriser = reponse.replace("[Secours Gemini] ", "").strip()
                self.memory_manager.ajouter_echange(commande, reponse_a_memoriser)

        else:
            print(resultat)
