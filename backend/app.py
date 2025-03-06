from flask import Flask, request, jsonify
from modelo import predict_class
from scraping import extract_text_from_url
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app = Flask(__name__)

# Endpoint para procesar texto ingresado manualmente
@app.route("/predict-text", methods=["POST"])
def predict_text():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No se proporcionó texto"}), 400
    category = predict_class(text)
    return jsonify({"category": category})

# Endpoint para procesar archivos .txt (se envían en un FormData)
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró archivo"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400
    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        category = predict_class(content)
        return jsonify({"category": category})
    return jsonify({"error": "Formato no soportado"}), 400

# Endpoint para procesar URLs
@app.route("/process-url", methods=["POST"])
def process_url():
    data = request.get_json()
    url = data.get("url", "")
    if not url:
        return jsonify({"error": "No se proporcionó una URL"}), 400
    try:
        # Se usa la función de scraping para extraer el texto
        text = extract_text_from_url(url)
        if not text:
            return jsonify({"error": "No se pudo extraer texto de la URL"}), 400
        category = predict_class(text)
        return jsonify({"category": category})
    except Exception as e:
        return jsonify({"error": f"Error al procesar la URL: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
