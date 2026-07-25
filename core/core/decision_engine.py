class DecisionEngine:

    def __init__(self, brain_manager, agent_manager):
        self.brain_manager = brain_manager
        self.agent_manager = agent_manager

    def analyser(self, demande):

        demande = demande.lower()

        decision = {
            "demande": demande,
            "objectif": "",
            "agent": "",
            "action": ""
        }

        if "application" in demande or "site" in demande or "projet" in demande:
            decision["objectif"] = "Créer ou améliorer un projet"
            decision["agent"] = "01_developpeur"
            decision["action"] = "Analyser le projet et proposer une solution"

        elif "information" in demande or "recherche" in demande:
            decision["objectif"] = "Trouver des informations"
            decision["agent"] = "03_recherche"
            decision["action"] = "Effectuer une recherche"

        elif "design" in demande or "image" in demande:
            decision["objectif"] = "Créer une solution visuelle"
            decision["agent"] = "02_designer"
            decision["action"] = "Créer une proposition de design"

        else:
            decision["objectif"] = "Analyser la demande"
            decision["agent"] = "00_directeur_ia"
            decision["action"] = "Réfléchir à la meilleure approche"

        return decision
