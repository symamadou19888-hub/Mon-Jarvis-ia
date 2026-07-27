import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class DecisionEngine:

    def __init__(self, brain_manager, agent_manager):
        self.brain_manager = brain_manager
        self.agent_manager = agent_manager
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

        self.outils_disponibles = [
            "lire_fichier",
            "ecrire_fichier",
            "rechercher_web",
            "creer_projet",
            "ajouter_tache",
            "lister_projets",
            "lister_taches"
        ]

    def _appeler_llm(self, prompt, timeout=15):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        reponse = requests.post(self.url, headers=headers, json=payload, timeout=timeout)
        reponse.raise_for_status()
        data = reponse.json()
        return data["choices"][0]["message"]["content"].strip()

    def choisir_agent(self, demande):
        liste_agents = list(self.agent_manager.agents.keys())

        prompt = (
            f"Voici une liste d'agents specialises : {', '.join(liste_agents)}. "
            f"Pour la demande suivante : \"{demande}\", "
            f"quel est l'agent le plus adapte ? "
            f"Reponds uniquement avec le nom exact de l'agent, sans rien d'autre."
        )

        try:
            choix = self._appeler_llm(prompt)
            for agent in liste_agents:
                if agent in choix:
                    return agent
            return "00_directeur_ia"
        except Exception:
            return "00_directeur_ia"

    def analyser_demande(self, demande):
        prompt = (
            f"Analyse cette demande utilisateur : \"{demande}\".\n\n"
            f"Reponds UNIQUEMENT avec un objet JSON valide, sans aucun texte autour, "
            f"au format exact suivant :\n"
            f'{{"difficulte": "faible|moyenne|elevee", '
            f'"risques": "aucun|faible|moyen|eleve", '
            f'"validation_requise": true ou false, '
            f'"resume": "resume court de l\'objectif en une phrase"}}\n\n'
            f"validation_requise doit etre true si l'action modifie des fichiers, "
            f"supprime des donnees, ou a un impact important. Sinon false."
        )

        defaut = {
            "difficulte": "moyenne",
            "risques": "faible",
            "validation_requise": False,
            "resume": demande
        }

        try:
            reponse = self._appeler_llm(prompt)
            reponse_nettoyee = reponse.strip()
            if reponse_nettoyee.startswith("```"):
                reponse_nettoyee = reponse_nettoyee.strip("`")
                if reponse_nettoyee.startswith("json"):
                    reponse_nettoyee = reponse_nettoyee[4:]
            analyse = json.loads(reponse_nettoyee)
            for cle in defaut:
                if cle not in analyse:
                    analyse[cle] = defaut[cle]
            return analyse
        except Exception:
            return defaut

    def choisir_outils(self, demande):
        prompt = (
            f"Voici la liste des outils disponibles : {', '.join(self.outils_disponibles)}.\n"
            f"Pour la demande suivante : \"{demande}\", "
            f"quels outils parmi cette liste seraient utiles ? "
            f"Reponds UNIQUEMENT avec les noms des outils separes par des virgules, "
            f"sans rien d'autre. Si aucun outil n'est utile, reponds : aucun."
        )

        try:
            reponse = self._appeler_llm(prompt)
            if "aucun" in reponse.lower():
                return []
            outils_choisis = [o.strip() for o in reponse.split(",")]
            return [o for o in outils_choisis if o in self.outils_disponibles]
        except Exception:
            return []

    def decider(self, demande):
        agent = self.choisir_agent(demande)
        analyse = self.analyser_demande(demande)
        outils = self.choisir_outils(demande)

        return {
            "agent": agent,
            "analyse": analyse,
            "outils_suggeres": outils
        }

    def obtenir_contexte_agent(self, nom_agent):
        return self.agent_manager.agents.get(nom_agent, "")
