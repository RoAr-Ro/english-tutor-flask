def detectar_tiempo(mensaje):

    if "yesterday" in mensaje:
        return "past"

    elif "tomorrow" in mensaje:
        return "future"

    return "present"