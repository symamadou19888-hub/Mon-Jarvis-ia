class CommandManager:

    def traiter(self, commande):
        commande = commande.lower()

        if commande == "agents":
            return "Afficher les agents disponibles."

        elif commande == "memoire":
            return "Afficher la mémoire de Jarvis."

        elif commande == "aide":
            return "Commandes disponibles : agents, memoire, aide."

        else:
            return "Commande inconnue."
