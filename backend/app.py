from flask import Flask, request, jsonify
from flask_cors import CORS
from modelo import predict_class
from scraping import extract_text_from_url

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir peticiones desde el frontend

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    if "url" in data:
        text = extract_text_from_url(data["url"])
    elif "text" in data:
        text = data["text"]
    else:
        return jsonify({"error": "No se proporcionó texto o URL"}), 400

    if not text:
        return jsonify({"error": "No se pudo extraer texto"}), 400

    predicted_class = predict_class(text)
    return jsonify({"category": predicted_class})

if __name__ == "__main__":
    app.run(debug=True)
