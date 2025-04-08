# 🤖 Intelligent Chatbot using BERT | NLP Project

This project is an advanced Natural Language Processing (NLP) based chatbot that classifies user intent, detects sentiment, and sets the foundation for a context-aware conversational assistant. It leverages pre-trained BERT models and the Hugging Face Transformers library.

---

## 📌 Project Goal

Build an advanced AI-powered chatbot that can:

- ✅ Classify user intent accurately
- 😊 Detect user sentiment (positive, negative, neutral)
- 🧠 Maintain context over conversations *(work in progress)*
- 💬 Generate appropriate responses based on intent *(next milestone)*

---

## 📂 Dataset

- **Source**: Hugging Face 🤗 Datasets
- **Name**: `Bhuvaneshwari/intent_classification`
- **Fields**: `text`, `intent`
- **Size**: 13,808 training samples

---

## 🛠️ Technologies & Libraries

- Python
- Hugging Face Transformers
- Datasets Library
- PyTorch
- scikit-learn
- Evaluate (for metrics)
- Weights & Biases (for tracking)
- Google Colab / Jupyter Notebook

---

## 🔄 Workflow

### 1. Load and Explore Dataset
```python
from datasets import load_dataset
ds = load_dataset("Bhuvaneshwari/intent_classification")
