# ejercicios por nivel
EJERCICIOS = {
    "beginner": [
        "Write a sentence using 'I eat'.",
        "Write a sentence using 'She goes'."
    ],
    "intermediate": [
        "Write a sentence in past using 'go'.",
        "Write a sentence in future using 'eat'."
    ],
    "advanced": [
        "Write a sentence using present perfect (have + past participle).",
        "Write a sentence using past perfect."
    ]
}


# obtiene ejercicio según nivel e índice
def obtener_ejercicio(nivel, indice):
    lista = EJERCICIOS.get(nivel, [])
    
    if indice < len(lista):
        return lista[indice]
    
    return None