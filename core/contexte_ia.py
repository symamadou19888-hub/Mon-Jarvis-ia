import os

def charger_contexte():
    fichiers = [
        "partenaire/brain/identity.md",
        "partenaire/brain/mission.md",
        "partenaire/brain/personality.md",
        "partenaire/brain/rules.md"
    ]

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    contenu_total = ""

    for fichier in fichiers:
        chemin = os.path.join(base, fichier)
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                contenu_total += f.read() + "\n\n"

    return contenu_total
