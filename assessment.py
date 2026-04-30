from core import corregir_frase
import json
import os

PREGUNTAS_NIVEL = [
    "Write a sentence in past using 'go'.",
    "Write a sentence in present using 'she'.",
    "Write a sentence in future using 'go'."
]


from core import corregir_frase
from grammar.detector import detectar_tiempo

def evaluar_nivel(respuestas):

    score = 0

    for i, respuesta in enumerate(respuestas):

        respuesta = respuesta.lower().strip()

        # ------------------------
        # VALIDAR ESTRUCTURA
        # ------------------------

        palabras = respuesta.split()
        SUJETOS = ["i", "you", "he", "she", "it", "we", "they"]

        estructura_valida = (
            len(palabras) >= 2 and palabras[0] in SUJETOS
        )

        # ------------------------
        # VALIDAR TIEMPO
        # ------------------------

        tiempo_correcto = False

        # ------------------------
        # VALIDACIÓN MÁS ROBUSTA
        # ------------------------

        if i == 0:  # past
            if "went" in respuesta:
                tiempo_correcto = True

        elif i == 1:  # present
            if "she" in respuesta and "goes" in respuesta:
                tiempo_correcto = True

        elif i == 2:  # future
            if "will" in respuesta and "go" in respuesta:
                tiempo_correcto = True

        # ------------------------
        # VALIDAR SI YA ESTABA BIEN
        # ------------------------

        texto_corregido, _ = corregir_frase(respuesta)

        # normalizar ambos textos de forma consistente
        usuario = respuesta.lower().strip()
        corregido = texto_corregido.lower().replace(".", "").strip()

        # permitir pequeñas diferencias (punto final)
        sin_correccion = corregido.startswith(usuario)
        
        # ------------------------
        # SCORE FINAL POR RESPUESTA
        # ------------------------

        if estructura_valida and tiempo_correcto and sin_correccion:
            score += 1

    # ------------------------
    # CLASIFICACIÓN
    # ------------------------

    if score == 0:
        return "beginner"
    elif score == 1:
        return "beginner"
    elif score == 2:
        return "intermediate"
    else:
        return "advanced"
    

ARCHIVO_LOG = "assessment_log.json"

def guardar_log_assessment(preguntas, respuestas, nivel):

    log = []

    # cargar logs existentes
    if os.path.exists(ARCHIVO_LOG):
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
            log = json.load(f)

    # construir entrada nueva
    registro = {
        "preguntas": preguntas,
        "respuestas": respuestas,
        "nivel": nivel
    }

    # añadir al historial
    log.append(registro)

    # guardar archivo
    with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=4, ensure_ascii=False)