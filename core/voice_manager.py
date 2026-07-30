import os
import subprocess
import time
import wave
import struct
import requests
from dotenv import load_dotenv

load_dotenv()

FICHIER_AUDIO_TEMP = "audio_temp.wav"


class VoiceManager:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url_transcription = "https://api.groq.com/openai/v1/audio/transcriptions"

    def _nettoyer_texte(self, texte):
        import re
        texte = texte.replace("[Secours Gemini]", "")
        texte = re.sub(r"\*\*|\*|#{1,6}\s*|_{1,2}|`", "", texte)
        texte = re.sub(r"^-{2,}$", "", texte, flags=re.MULTILINE)
        texte = re.sub(r"^\s*-\s+", "", texte, flags=re.MULTILINE)
        return texte.strip()

    MAX_MOTS_VOCAL = 80

    def _limiter_longueur(self, texte):
        mots = texte.split()
        if len(mots) <= self.MAX_MOTS_VOCAL:
            return texte
        return " ".join(mots[:self.MAX_MOTS_VOCAL]) + ". Pour plus de details, consultez l'interface texte."

    def parler(self, texte):
        try:
            texte_propre = self._nettoyer_texte(texte)
            texte_propre = self._limiter_longueur(texte_propre)
            nb_mots = len(texte_propre.split())
            duree_estimee = max(1, nb_mots / 4.2)
            timeout_tts = duree_estimee + 15

            subprocess.run(["termux-tts-speak", "-l", "fr", texte_propre], timeout=timeout_tts)
            time.sleep(duree_estimee)
            return True
        except subprocess.TimeoutExpired:
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Erreur synthese vocale : {e}")
            return False

    VOLUME_MIN_VOIX = 300

    def _mesurer_volume(self, chemin_fichier):
        fichier_converti = chemin_fichier + "_conv.wav"
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", chemin_fichier, "-ar", "16000", "-ac", "1", fichier_converti],
                capture_output=True, timeout=15
            )

            if not os.path.exists(fichier_converti):
                return 0

            with wave.open(fichier_converti, "rb") as wf:
                nb_frames = wf.getnframes()
                if nb_frames == 0:
                    return 0
                donnees = wf.readframes(nb_frames)
                echantillons = struct.unpack(f"<{len(donnees)//2}h", donnees)
                if not echantillons:
                    return 0
                somme_carres = sum(s * s for s in echantillons)
                rms = (somme_carres / len(echantillons)) ** 0.5
                return rms
        except Exception as e:
            print(f"Erreur mesure volume : {e}")
            return 0
        finally:
            if os.path.exists(fichier_converti):
                os.remove(fichier_converti)

    def enregistrer(self, duree_secondes=5):
        try:
            if os.path.exists(FICHIER_AUDIO_TEMP):
                os.remove(FICHIER_AUDIO_TEMP)

            subprocess.run(
                ["termux-microphone-record", "-f", FICHIER_AUDIO_TEMP, "-l", str(duree_secondes)],
                timeout=duree_secondes + 5
            )

            time.sleep(duree_secondes + 1)

            if not os.path.exists(FICHIER_AUDIO_TEMP):
                return False

            return True

        except Exception as e:
            print(f"Erreur enregistrement : {e}")
            return False

    PHRASES_HALLUCINATION = [
        "sous-titrage", "sous-titre", "société radio-canada", "radio-canada",
        "amara.org", "merci d'avoir regarde", "merci d'avoir regardé",
        "abonnez-vous", "n'hesitez pas a vous abonner"
    ]

    def _est_hallucination(self, texte):
        texte_lower = texte.strip().lower()
        if len(texte_lower) < 3:
            return True
        for phrase in self.PHRASES_HALLUCINATION:
            if phrase in texte_lower:
                return True
        return False

    def transcrire(self):
        if not os.path.exists(FICHIER_AUDIO_TEMP):
            return "Erreur : aucun fichier audio a transcrire."

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            with open(FICHIER_AUDIO_TEMP, "rb") as f:
                fichiers = {
                    "file": (FICHIER_AUDIO_TEMP, f, "audio/wav")
                }

                data = {
                    "model": "whisper-large-v3",
                    "language": "fr",
                    "prompt": "Conversation avec Jarvis, assistant IA personnel. Vocabulaire technique : projet, tache, GitHub, code, fichier, agent."
                }

                r = requests.post(
                    self.url_transcription,
                    headers=headers,
                    files=fichiers,
                    data=data,
                    timeout=30
                )

                r.raise_for_status()

                resultat = r.json()
                texte = resultat.get("text", "").strip()

                if self._est_hallucination(texte):
                    return "Erreur : aucune parole detectee."

                return texte

        except Exception as e:
            return f"Erreur transcription : {e}"

        finally:
            if os.path.exists(FICHIER_AUDIO_TEMP):
                os.remove(FICHIER_AUDIO_TEMP)

    def ecouter_et_transcrire(self, duree_secondes=5):
        if not self.enregistrer(duree_secondes):
            return "Erreur : impossible d'enregistrer l'audio."

        return self.transcrire()
