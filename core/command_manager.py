class CommandManager:

    def traiter(self, commande):
        commande = commande.lower().strip()

        if commande in ["bonjour", "salut", "hello"]:
            return "Bonjour, je suis Jarvis. Systeme operationnel."

        elif commande in ["qui es tu", "qui es-tu", "présente toi"]:
            return "Je suis Jarvis, ton assistant IA personnel."

        elif commande == "agents":
            return "Agents disponibles : Directeur IA, Developpeur, Designer, Recherche, Business."

        elif commande == "memoire":
            return "La memoire de Jarvis est active."

        elif commande == "version":
            return "Jarvis version 0.1."

        elif commande == "aide":
            return "Commandes disponibles : bonjour, qui es-tu, agents, memoire, version, aide."

        else:
            return "Commande inconnue. Tape aide pour voir les commandes."
