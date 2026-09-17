import pandas as pd


FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Type_L",
    "Type_M"
]


def preparar_dados(dados):
    """
    Converte os dados recebidos pela API para o formato
    esperado pelo modelo Random Forest.
    """

    # Verifica se os campos obrigatórios existem
    campos_obrigatorios = [
        "air_temperature",
        "process_temperature",
        "rpm",
        "torque",
        "tool_wear",
        "type"
    ]

    campos_faltantes = [
        campo for campo in campos_obrigatorios
        if campo not in dados
    ]

    if campos_faltantes:
        raise ValueError(
            f"Campos obrigatórios ausentes: {campos_faltantes}"
        )

    tipo = dados["type"].upper()

    # O modelo foi treinado com Type como One-Hot Encoding
    if tipo not in ["L", "M"]:
        raise ValueError(
            "O campo 'type' deve ser 'L' ou 'M'."
        )

    entrada = pd.DataFrame([{
        "Air temperature [K]": dados["air_temperature"],
        "Process temperature [K]": dados["process_temperature"],
        "Rotational speed [rpm]": dados["rpm"],
        "Torque [Nm]": dados["torque"],
        "Tool wear [min]": dados["tool_wear"],

        # Equivalente ao pd.get_dummies(..., drop_first=True)
        "Type_L": 1 if tipo == "L" else 0,
        "Type_M": 1 if tipo == "M" else 0
    }])

    # Garante exatamente a mesma ordem utilizada no treinamento
    entrada = entrada[FEATURES]

    return entrada