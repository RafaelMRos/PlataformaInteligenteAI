from flask import Flask, request, jsonify
from flask_cors import CORS

from services.prediction_service import realizar_previsao


app = Flask(__name__)
CORS(app)


# ==========================================================
# Rota inicial
# ==========================================================

@app.route("/")
def home():
    return "API de Inteligência Artificial funcionando!"


# ==========================================================
# Endpoint de previsão
# ==========================================================

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():

    if request.method == "OPTIONS":
        return "", 200

    try:

        # Recebe JSON
        data = request.get_json()

        if not data:
            return jsonify({
                "erro": "Nenhum dado foi enviado"
            }), 400

        # Realiza previsão
        resultado = realizar_previsao(data)

        # Retorna resultado
        return jsonify(resultado), 200

    except ValueError as erro:

        return jsonify({
            "erro": str(erro)
        }), 400

    except Exception as erro:

        return jsonify({
            "erro": "Erro interno ao realizar previsão",
            "detalhes": str(erro)
        }), 500


# ==========================================================
# Inicialização
# ==========================================================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )