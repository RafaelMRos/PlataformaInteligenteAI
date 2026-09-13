import os
import joblib

from services.preprocessing import preparar_dados


# ==========================================================
# Caminho do modelo
# ==========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "modelo",
    "random_forest_ai4i.pkl"
)


# ==========================================================
# Carregar modelo
# ==========================================================

dados_modelo = joblib.load(MODEL_PATH)

modelo = dados_modelo["modelo"]
features = dados_modelo["features"]
threshold = dados_modelo["threshold"]


# ==========================================================
# Realizar previsão
# ==========================================================

def realizar_previsao(dados):
    """
    Recebe os dados do veículo, realiza o preprocessing
    e executa a previsão utilizando o Random Forest.
    """

    # ------------------------------------------------------
    # 1. Preparar os dados
    # ------------------------------------------------------

    entrada = preparar_dados(dados)

    # ------------------------------------------------------
    # 2. Verificar as features
    # ------------------------------------------------------

    if list(entrada.columns) != list(features):
        raise ValueError(
            "As features de entrada não correspondem "
            "às features utilizadas no treinamento."
        )

    # ------------------------------------------------------
    # 3. Calcular probabilidade de falha
    # ------------------------------------------------------

    probabilidade_falha = modelo.predict_proba(entrada)[0][1]

    # ------------------------------------------------------
    # 4. Aplicar threshold
    # ------------------------------------------------------

    falha_predita = int(
        probabilidade_falha >= threshold
    )

    # ------------------------------------------------------
    # 5. Calcular Health Score
    # ------------------------------------------------------

    health_score = (1 - probabilidade_falha) * 100

    # ------------------------------------------------------
    # 6. Definir status
    # ------------------------------------------------------

    if health_score >= 70:
        status = "OPERACIONAL"

    elif health_score >= 40:
        status = "ATENÇÃO"

    else:
        status = "CRÍTICO"

    # ------------------------------------------------------
    # 7. Retornar resultado
    # ------------------------------------------------------

    return {
        "probabilidade_falha": round(
            float(probabilidade_falha), 4
        ),
        "health_score": round(
            float(health_score), 2
        ),
        "status": status,
        "falha_predita": falha_predita,
        "threshold": float(threshold)
    }