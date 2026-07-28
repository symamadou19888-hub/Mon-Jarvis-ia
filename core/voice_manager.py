import os
import subprocess
import time
import requests
from dotenv import load_dotenv

load_dotenv()

FICHIER_AUDIO_TEMP = "audio_temp.wav"


class VoiceManager:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url_transcription = "https://api.groq.com/openai/v1/audio/transcriptions"

    def parler(self, texte):
        try:
            subprocess.run(["termux-tts-speak", "-l", "fr", texte], timeout=30)
            return True
        except Exception as e:
            print(f"Erreur synthese vocale : {e}")
            return False

    def enregistrer(self, duree_secondes=5):
        try:
            if os.path.exists(FICHIER_AUDIO_TEMP):
                os.remove(FICHIER_AUDIO_TEMP)
            subprocess.run(
                ["termux-microphone-record", "-f", FICHIER_AUDIO_TEMP, "-l", str(duree_secondes)],
                timeout=duree_secondes + 5
            )
            time.sleep(duree_secondes + 1)
            return os.path.exists(FICHIER_AUDIO_TEMP)
        except Exception as e:
            print(f"Erreur enregistrement : {e}")
            return False

    def transcrire(self):
        if not os.path.exists(FICHIER_AUDIO_TEMP):
            return "Erreur : aucun fichier audio a transcrire."

        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            with open(FICHIER_AUDIO_TEMP, "rb") as f:
                fichiers = {"file": (FICHIER_AUDIO_TEMP, f, "audio/wav")}
                data = {"model": "whisper-large-v3-turbo", "language": "fr"}
                r = requests.post(self.url_transcription, headers=headers, files=fichiers, data=data, timeout=30)
                r.raise_for_status()
                resultat = r.json()
                return resultat.get("text", "").strip()
        except Exception as e:
            return f"Erreur transcription : {e}"
        finally:
            if os.path.exists(FICHIER_AUDIO_TEMP):
                os.remove(FICHIER_AUDIO_TEMP)

    def ecouter_et_transcrire(self, duree_secondes=5):
        if not self.enregistrer(duree_secondes):
            return "Erreur : impossible d'enregistrer l'audio."
        return self.transcrire()
