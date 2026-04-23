from verbos import verbos

def corregir_futuro(mensaje):

    palabras = mensaje.split()

    if "will" in palabras:
        return mensaje, None

    nueva_frase = []
    cambio = False

    for palabra in palabras:

        if palabra in verbos:
            nueva_frase.append("will")
            nueva_frase.append(palabra)
            cambio = True

        else:
            nueva_frase.append(palabra)

    resultado = " ".join(nueva_frase)

    if cambio:
        explicacion = "Se detectó futuro (tomorrow) y se añadió 'will'."
        return resultado, explicacion

    return mensaje, None