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

    def choisir_agent(self, demande):
        liste_agents = list(self.agent_manager.agents.keys())

        prompt = (
            f"Voici une liste d'agents specialises : {', '.join(liste_agents)}. "
            f"Pour la demande suivante : \"{demande}\", "
            f"quel est l'agent le plus adapte ? "
            f"Reponds uniquement avec le nom exact de l'agent, sans rien d'autre."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            reponse = requests.post(self.url, headers=headers, json=payload, timeout=15)
            reponse.raise_for_status()
            data = reponse.json()
            choix = data["choices"][0]["message"]["content"].strip()

            for agent in liste_agents:
                if agent in choix:
                    return agent

            return "00_directeur_ia"
        except Exception:
            return "00_directeur_ia"

    def obtenir_contexte_agent(self, nom_agent):
        return self.agent_manager.agents.get(nom_agent, "")
