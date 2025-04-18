# -*- coding: utf-8 -*-
"""Smart_chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kghmYyFSjOOJO-nRQR39yUKVpa-mxn0L
"""

!pip install datasets --upgrade

from datasets import load_dataset

dataset = load_dataset("Bhuvaneshwari/intent_classification")

dataset

# Look at a few training samples
dataset['train'][0:5]

from transformers import BertTokenizer
from datasets import DatasetDict
from sklearn.preprocessing import LabelEncoder

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Use sklearn's LabelEncoder to convert text labels to numbers
label_encoder = LabelEncoder()

# Fit on training data labels
label_encoder.fit(dataset["train"]["intent"])

# Create a function to encode labels
def encode_labels(example):
    example["label"] = label_encoder.transform([example["intent"]])[0]
    return example

# Apply to all splits
dataset = dataset.map(encode_labels)

# Define a function for tokenizing text
def tokenize_function(example):
    return tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

# Tokenize dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Keep only relevant fields
tokenized_datasets.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

from transformers import BertForSequenceClassification, TrainingArguments, Trainer
import torch

num_labels = len(label_encoder.classes_)  # e.g. 20 unique intents

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=num_labels
)

training_args = TrainingArguments(
    output_dir="./bert-intent-model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

!pip install evaluate

import evaluate
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=-1)
    return accuracy.compute(predictions=predictions, references=labels)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    compute_metrics=compute_metrics
)

import os
os.environ["WANDB_DISABLED"] = "true"

tokenized_datasets["train"] = tokenized_datasets["train"].select(range(3000))

from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./bert-intent-model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=1,     # ✅ Faster training
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

from transformers import pipeline

# Load the model
classifier = pipeline("text-classification", model="./bert-intent-model/checkpoint-188", tokenizer=tokenizer)

# Try some predictions
queries = [
    "Play a song by Taylor Swift",
    "Add this to my chill playlist",
    "Cancel my booking",
    "What’s the weather like today?",
    "Thanks for your help"
]

for query in queries:
    result = classifier(query)
    print(f"Query: {query} ➤ Predicted Intent: {result[0]['label']}")

from datasets import load_dataset

ds = load_dataset("Bhuvaneshwari/intent_classification")

print(ds["train"].features)

# Get unique intent names and sort them in the same order as training
intent_labels = ds["train"].unique("intent")
intent_labels.sort()

# Now map label index to name
id2label = {i: label for i, label in enumerate(intent_labels)}

# Predict using mapped labels
queries = [
    "Play a song by Taylor Swift",
    "Add this to my chill playlist",
    "Cancel my booking",
    "What’s the weather like today?",
    "Thanks for your help"
]

for query in queries:
    result = classifier(query)
    label_id = int(result[0]['label'].split("_")[-1])
    print(f"Query: {query} ➤ Predicted Intent: {id2label[label_id]}")

"""**Module 2: NER (Named Entity Recognition)**"""

from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

# Test it
text = "Book a flight from Mumbai to New York for next Monday"
entities = ner(text)
print(entities)

"""**✅ Module 3: Sentiment Analysis**"""

from transformers import pipeline

# Load the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Test it with example text
text = "I'm so happy with the service today!"
result = sentiment_analyzer(text)
print(result)

test_texts = [
    "I’m really disappointed with your support.",
    "Thanks! You’re the best!",
    "Can you please help me with my problem?",
    "This is terrible. I want a refund.",
    "I'm not sure if I like this."
]

for txt in test_texts:
    print(f"Text: {txt} ➤ Sentiment: {sentiment_analyzer(txt)[0]['label']}")

"""✅ Module 4: Response Generation"""

def generate_response(intent, sentiment, entities=None):
    if intent == "PlayMusic":
        return "Sure, playing your favorite song! 🎵"
    elif intent == "AddToPlaylist":
        return "Adding it to your playlist. Anything else?"
    elif intent == "RateBook":
        return "Thanks for rating! Your feedback matters. 📚"
    elif intent == "SearchCreativeWork":
        return "Looking it up for you now."
    elif intent == "GetWeather":
        return "Here’s the weather update for today ☁️"

    # Sentiment-specific additions
    if sentiment == "NEGATIVE":
        return "I'm sorry to hear that. Let me fix it right away."
    elif sentiment == "POSITIVE":
        return "Glad you liked it! 😊"
    else:
        return "Got it! Let me handle that."

intent = "AddToPlaylist"
sentiment = "POSITIVE"
entities = ["chill playlist"]

response = generate_response(intent, sentiment, entities)
print("Bot:", response)

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("./bert-intent-model/checkpoint-188")  # Use correct checkpoint name
tokenizer = AutoTokenizer.from_pretrained("./bert-intent-model/checkpoint-188")

intent_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def chatbot_pipeline(query):
    # Intent Recognition
    intent_result = intent_classifier(query)[0]
    intent = intent_result["label"]

    # Define simple rule-based responses
    if intent == "PlayMusic":
        response = "🎶 Playing your favorite song."
    elif intent == "AddToPlaylist":
        response = "✅ Adding it to your playlist. Anything else?"
    elif intent == "RateBook":
        response = "📚 Sure! Please tell me the rating."
    elif intent == "GetWeather":
        response = "☀️ Checking today's weather for you."
    elif intent == "SearchCreativeWork":
        response = "🔍 Looking it up now."
    elif intent == "BookRestaurant":
        response = "🍽️ Booking a table for you."
    elif intent == "GetNews":
        response = "🗞️ Fetching the latest news headlines."
    elif intent == "SetAlarm":
        response = "⏰ Alarm set!"
    else:
        response = "🤖 I'm still learning. Can you rephrase that?"

    return f"Intent: {intent} ➤ Bot: {response}"

queries = [
    "Play a song by Taylor Swift",
    "Add this to my chill playlist",
    "Cancel my booking",
    "What’s the weather like today?",
    "Thanks for your help"
]

for q in queries:
    print(f"User: {q}\n{chatbot_pipeline(q)}\n")

