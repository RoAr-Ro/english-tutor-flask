# =====================================
# CURRICULUM DEL TUTOR
# =====================================

# estructura:
# nivel → subnivel → lista de temas
# cada tema tiene:
# - nombre
# - teoría
# - ejercicios

CURRICULO = {

    # =========================
    # BEGINNER NIVEL 1
    # =========================
    "beginner_1": [

        {
            # nombre del tema
            "tema": "present_simple_basic",

            # teoría corta
            "teoria": "Use 's' with he, she, it. Example: He eats, She runs.",

            # ejercicios guiados
            "ejercicios": [

                # ejercicio 1
                {
                    "instruccion": "Write a sentence using 'he eat'",
                    "respuesta_esperada": "he eats"
                },

                # ejercicio 2
                {
                    "instruccion": "Write a sentence using 'she go'",
                    "respuesta_esperada": "she goes"
                }

            ]
        },
        
        {
            "tema": "questions_basic",
            "teoria": "Use 'does' for he/she/it questions. Example: Does he eat?",
            "ejercicios": [
                {
                    "instruccion": "Write a question using 'he eat'",
                    "respuesta_esperada": "does he eat"
                }
            ]
        }

    ]

}