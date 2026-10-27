import pandas as pd


FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]"
]


def preparar_dados(dados):
    """
    Converte e valida os dados recebidos pela API para o formato
    esperado pelo modelo Random Forest.

    Em conformidade com sistemas críticos de emergência:
    - Nenhum valor default ou aproximado é assumido se o dado não existir.
    - Se qualquer dado obrigatório estiver ausente, nulo ou fora dos limites físicos,
      uma exceção ValueError é lançada imediatamente.
    """

    # 1. Verifica se os campos obrigatórios existem e não são nulos
    campos_obrigatorios = [
        "air_temperature",
        "process_temperature",
        "rpm",
        "torque"
    ]

    campos_faltantes = [
        campo for campo in campos_obrigatorios
        if campo not in dados or dados[campo] is None
    ]

    if campos_faltantes:
        raise ValueError(
            f"Campos obrigatórios ausentes ou nulos para telemetria crítica: {campos_faltantes}"
        )

    # 2. Conversão e validação numérica rigorosa
    try:
        air_temp = float(dados["air_temperature"])
        proc_temp = float(dados["process_temperature"])
        rpm = float(dados["rpm"])
        torque = float(dados["torque"])
    except (ValueError, TypeError) as erro:
        raise ValueError(
            f"Valores de telemetria inválidos (não numéricos): {erro}"
        )

    # 3. Validação de consistência física
    if air_temp <= 0 or proc_temp <= 0:
        raise ValueError(
            "Temperaturas devem ser expressas em Kelvin (> 0 K)."
        )

    if rpm <= 0:
        raise ValueError(
            "RPM deve ser maior que zero (motor deve estar em operação)."
        )

    if torque < 0:
        raise ValueError(
            "Torque não pode ser negativo."
        )

    entrada = pd.DataFrame([{
        "Air temperature [K]": air_temp,
        "Process temperature [K]": proc_temp,
        "Rotational speed [rpm]": rpm,
        "Torque [Nm]": torque
    }])

    # Garante exatamente a mesma ordem utilizada no treinamento
    entrada = entrada[FEATURES]

    return entrada
