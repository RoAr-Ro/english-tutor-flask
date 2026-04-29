from core import corregir_frase

PREGUNTAS_NIVEL = [
    "Write a sentence in past using 'go'.",
    "Write a sentence in present using 'she'.",
    "Write a sentence in future using 'go'."
]

def evaluar_nivel(respuestas):

    score = 0

    for respuesta in respuestas:

        palabras = respuesta.lower().split()

        # validar estructura mínima: sujeto + verbo
        if len(palabras) >= 2 and palabras[0] in ["i", "you", "he", "she", "it", "we", "they"]:
            score += 1

    if score <= 1:
        return "beginner"
    elif score == 2:
        return "intermediate"
    else:
        return "advanced"