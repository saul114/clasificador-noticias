from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, BertModel
import torch
from newspaper import Article  # Para el scraping

# Configurar el dispositivo
device = torch.device("cpu")

# Cargar modelo BERT y tokenizador
model_name = "bert-base-multilingual-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
bert_model = BertModel.from_pretrained(model_name).to(device)

# Cargar modelo de clasificación
modelo = tf.keras.models.load_model("../modelos/modelo_clasificador.keras")

# Diccionario de clases
topic_to_label = {
    0: "Medicina", 1: "Economia", 2: "Motor", 3: "Deportes",
    4: "Religion", 5: "Militar", 6: "Politica", 7: "Ocio",
    8: "Moda", 9: "Informatica", 10: "Astronomia", 11: "Alimentacion"
}

app = Flask(__name__)

def get_bert_embedding(text, max_length=512):
    """Convierte un texto en un embedding con BERT"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()

def predict_class(text):
    """Predice la clase de una noticia"""
    embedding = get_bert_embedding(text)
    pred_probs = modelo.predict(embedding)
    pred_class = int(np.argmax(pred_probs, axis=1)[0])
    return pred_class, topic_to_label.get(pred_class, "Desconocido")

def extract_article_text(url):
    """Extrae el contenido de un artículo de noticias desde una URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return None

@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    class_idx, class_name = predict_class(text)
    return jsonify({"class": class_name, "index": class_idx})

@app.route('/scrape', methods=['POST'])
def scrape_and_classify():
    """Toma una URL, extrae la noticia y la clasifica"""
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    article_text = extract_article_text(url)
    if not article_text:
        return jsonify({"error": "No se pudo extraer la noticia"}), 400

    class_idx, class_name = predict_class(article_text)
    return jsonify({"class": class_name, "index": class_idx, "article_text": article_text[:500]})  # Limitamos la salida

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
