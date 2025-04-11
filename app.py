from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load pipelines
intent_classifier = pipeline("text-classification", model="bert-intent-classifier", tokenizer="bert-intent-classifier")
sentiment_analyzer = pipeline("sentiment-analysis")
ner_pipeline = pipeline("ner", grouped_entities=True)

# Store conversation
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    global messages
    if request.method == "POST":
        user_input = request.form["user_input"]

        # NLP processing
        intent = intent_classifier(user_input)[0]["label"]
        sentiment = sentiment_analyzer(user_input)[0]["label"]
        entities = [e["word"] for e in ner_pipeline(user_input)]

        # Bot response (simple logic)
        response = {
            "PlayMusic": "🎵 Playing your favorite tune!",
            "AddToPlaylist": "➕ Added to your playlist!",
            "GetWeather": "☁️ It's sunny and warm today!",
        }.get(intent, "🤖 I'm not sure how to respond to that yet.")

        # Add messages to list
        messages.append({"sender": "User", "text": user_input})
        messages.append({"sender": "Bot", "text": response})

    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
