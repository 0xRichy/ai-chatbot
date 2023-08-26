from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import sqlite3
import requests
import json

app = Flask(__name__)

# Initialisation du chatbot
chatbot = ChatBot("MyBot")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Initialisation de la base de données SQLite
conn = sqlite3.connect('chatbot.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS interactions (user_query TEXT, bot_response TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS history (user_id TEXT, conversation TEXT)''')

# Variable globale pour la clé API Bing
bing_api_key = ""

# Fonction pour effectuer une recherche Bing
def bing_search(query):
    global bing_api_key
    url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": query, "count": 1}

    response = requests.get(url, headers=headers, params=params)
    search_results = response.json()

    return search_results['webPages']['value'][0]['snippet']

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        api_key = request.form.get("api_key")
        global bing_api_key
        bing_api_key = api_key
        return "Settings updated"
    return render_template("settings.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_query = request.args.get("msg")
    bot_response = chatbot.get_response(user_query).text

    # Sauvegarde de l'interaction dans la base de données
    c.execute("INSERT INTO interactions VALUES (?, ?)", (user_query, bot_response))
    conn.commit()

    # Si l'utilisateur demande une recherche Bing
    if "search for" in user_query:
        search_query = user_query.replace("search for ", "")
        bot_response = bing_search(search_query)

    return bot_response

if __name__ == "__main__":
    app.run()
