from flask import Flask, request, jsonify
from newspaper import Article
import os
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, BertModel
import torch

app = Flask(__name__)

# Configuración del modelo BERT y clasificador
model_name = "bert-base-multilingual-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
bert_model = BertModel.from_pretrained(model_name)
device = torch.device("cpu")
bert_model.to(device)

# Cargar modelo clasificador
modelo = tf.keras.models.load_model("modelo_clasificador.keras")

# Diccionario de clases
topic_to_label = {
    "Medicina": 0, "Economia": 1, "Motor": 2, "Deportes": 3, "Religion": 4,
    "Militar": 5, "Politica": 6, "Ocio": 7, "Moda": 8, "Informatica": 9,
    "Astronomia": 10, "Alimentacion": 11
}
label_to_topic = {v: k for k, v in topic_to_label.items()}

# Función para obtener embeddings de BERT
def get_bert_embedding(text, max_length=512):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    outputs = bert_model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :]
    return cls_embedding.detach().cpu().numpy()

# Función para predecir la categoría
def predict_class(text):
    embedding = get_bert_embedding(text)
    pred_probs = modelo.predict(embedding)
    pred_class = int(np.argmax(pred_probs, axis=1)[0])
    return pred_class, label_to_topic.get(pred_class, "Desconocido")

# Ruta para procesar texto manual
@app.route('/predict-text', methods=['POST'])
def predict_text():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No se proporcionó texto"}), 400

    clase_idx, clase_nombre = predict_class(text)
    return jsonify({"category": clase_nombre})

# Ruta para procesar archivos .txt
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        clase_idx, clase_nombre = predict_class(content)
        return jsonify({"category": clase_nombre})

    return jsonify({"error": "Formato no soportado"}), 400

# Ruta para procesar URLs
@app.route('/process-url', methods=['POST'])
def process_url():
    data = request.json
    url = data.get("url", "")
    
    if not url:
        return jsonify({"error": "No se proporcionó una URL"}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        clase_idx, clase_nombre = predict_class(text)
        return jsonify({"category": clase_nombre})
    except Exception as e:
        return jsonify({"error": f"Error al procesar la URL: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
