class Jarvis:
    def __init__(self):
        self.name = "Jarvis"
        self.version = "1.0.0"

    def start(self):
        print(f"{self.name} {self.version} est prêt.")

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.start()
