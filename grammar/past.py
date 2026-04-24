from verbos import VERBOS_IRREGULARES

# función para conjugar verbo regular en pasado
def pasado_regular(verbo):

    # si termina en "e" → solo añadir "d"
    if verbo.endswith("e"):
        return verbo + "d"

    # si termina en "y"
    elif verbo.endswith("y"):

        # vocal antes de la y → solo añadir "ed"
        if len(verbo) > 1 and verbo[-2] in "aeiou":
            return verbo + "ed"

        # consonante + y → cambiar a "ied"
        return verbo[:-1] + "ied"

    # caso general
    return verbo + "ed"

def corregir_pasado(mensaje):

    palabras = mensaje.split()
    nueva_frase = []
    explicacion = None
    cambio = False

    for i, palabra in enumerate(palabras):

        # si es el verbo (segunda palabra)
        if i == 1:

            # verbo irregular
            if palabra in VERBOS_IRREGULARES:
                nueva_frase.append(VERBOS_IRREGULARES[palabra])
                cambio = True

            # verbo regular
            else:
                nueva_frase.append(pasado_regular(palabra))
                cambio = True

        # caso especial "am"
        elif palabra == "am":
            cambio = True
            continue

        else:
            nueva_frase.append(palabra)

    resultado = " ".join(nueva_frase)

    if cambio:
        explicacion = "Se detectó pasado (yesterday) y se corrigió el verbo."

    return resultado, explicacion