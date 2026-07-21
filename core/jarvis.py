class Jarvis:
    def __init__(self):
        self.nom = "Jarvis"
        self.version = "0.1"

    def start(self):
        print(f"{self.nom} version {self.version} démarré.")
        print("Système prêt.")

        while True:
            commande = input("Vous : ")

            if commande.lower() in ["quitter", "exit", "stop"]:
                print("Jarvis arrêté.")
                break

            self.traiter_commande(commande)

    def traiter_commande(self, commande):
        print(f"Jarvis analyse : {commande}")
