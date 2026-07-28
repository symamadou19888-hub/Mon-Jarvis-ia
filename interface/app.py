import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from flask import Flask, render_template, request
from jarvis import Jarvis

app = Flask(__name__)

jarvis = Jarvis()

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/envoyer", methods=["POST"])
def envoyer():
    message = request.form["message"]
    reponse = jarvis.traiter_commande(message, retourner_reponse=True)
    return reponse

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
