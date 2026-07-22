def traiter_commande(self, commande):
    self.logger.enregistrer(f"Commande reçue : {commande}")

    self.context_manager.definir("derniere_commande", commande)

    resultat = self.command_manager.traiter(commande)
    print(resultat)
