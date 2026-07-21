class Jarvis:
    def __init__(self):
        self.name = "Jarvis"
        self.version = "1.0.0"
        self.status = "Initialisation"

    def start(self):
        self.status = "En ligne"

        print("=" * 40)
        print(f"{self.name} v{self.version}")
        print("Assistant IA personnel")
        print(f"Statut : {self.status}")
        print("=" * 40)

    def stop(self):
        self.status = "Arrêt"
        print("Jarvis est arrêté.")
