import os
import json
import requests
from dotenv import load_dotenv
from tools import lire_fichier, ecrire_fichier

load_dotenv()

OUTILS = [
    {
        "type": "function",
        "function": {
            "name": "lire_fichier",
            "description": "Lit le contenu d'un fichier du projet",
            "parameters": {
                "type": "object",
                "properties": {
                    "chemin": {"type": "string", "description": "Chemin relatif du fichier a lire"}
                },
                "required": ["chemin"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ecrire_fichier",
            "description": "Ecrit ou remplace le contenu d'un fichier du projet",
            "parameters": {
                "type": "object",
                "properties": {
                    "chemin": {"type": "string", "description": "Chemin relatif du fichier a ecrire"},
                    "contenu": {"type": "string", "description": "Contenu a ecrire dans le fichier"}
                },
                "required": ["chemin", "contenu"]
            }
        }
    }
]

FONCTIONS_DISPONIBLES = {
    "lire_fichier": lire_fichier,
    "ecrire_fichier": ecrire_fichier
}


class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    def demander(self, message, contexte="", historique=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if contexte:
            messages.append({"role": "system", "content": contexte})

        if historique:
            for echange in historique:
                messages.append({"role": "user", "content": echange["question"]})
                messages.append({"role": "assistant", "content": echange["reponse"]})

        messages.append({"role": "user", "content": message})

        try:
            for _ in range(5):
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "tools": OUTILS
                }
                reponse = requests.post(self.url, headers=headers, json=payload, timeout=30)
                reponse.raise_for_status()
                data = reponse.json()
                choix = data["choices"][0]["message"]

                if choix.get("tool_calls"):
                    messages.append(choix)
                    for appel in choix["tool_calls"]:
                        nom_fonction = appel["function"]["name"]
                        arguments = json.loads(appel["function"]["arguments"])
                        fonction = FONCTIONS_DISPONIBLES.get(nom_fonction)
                        resultat = fonction(**arguments) if fonction else "Outil inconnu."
                        messages.append({
                            "role": "tool",
                            "tool_call_id": appel["id"],
                            "content": str(resultat)
                        })
                else:
                    return choix["content"]

            return "Erreur : trop d'appels d'outils enchaines."
        except Exception as e:
            return f"Erreur IA : {e}"
