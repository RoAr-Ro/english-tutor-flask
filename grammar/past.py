from verbos import verbos

def corregir_pasado(mensaje):

    palabras = mensaje.split()
    nueva_frase = []
    explicacion = None
    cambio = False

    for palabra in palabras:

        if palabra in verbos:
            nueva_frase.append(verbos[palabra])
            cambio = True

        elif palabra == "am":
            cambio = True
            continue

        else:
            nueva_frase.append(palabra)

    resultado = " ".join(nueva_frase)

    if cambio:
        explicacion = "Se detectó pasado (yesterday) y se corrigió el verbo."

    return resultado, explicacion