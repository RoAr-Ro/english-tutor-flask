def corregir_presente(mensaje):

    palabras = mensaje.split()

    if len(palabras) < 2:
        return mensaje, None

    sujeto = palabras[0]
    verbo = palabras[1]

    tercera_persona = ["he", "she", "it"]

    if sujeto in tercera_persona:

        if not verbo.endswith("s"):

            if verbo.endswith(("o", "ch", "sh", "x", "s")):
                verbo_correcto = verbo + "es"
                explicacion = f"'{sujeto}' requiere verbo terminado en 'es'."
            else:
                verbo_correcto = verbo + "s"
                explicacion = f"'{sujeto}' requiere verbo en tercera persona (+s)."

            palabras[1] = verbo_correcto

            return " ".join(palabras), explicacion

    return mensaje, None