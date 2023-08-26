from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)
openai.api_key = ''

def obtenir_reponse_utilisateur(message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=50
    )
    return response.choices[0].text.strip()

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        openai.api_key = request.form["api_key"]
        return redirect(url_for('chatbot'))
    return render_template("index.html", api_key=openai.api_key)

@app.route("/chat", methods=["POST"])
def get_chat_response():
    user_input = request.form["user_input"]
    chatbot_response = obtenir_reponse_utilisateur(user_input)
    return {"response": chatbot_response}

if __name__ == "__main__":
    app.run(debug=True)

