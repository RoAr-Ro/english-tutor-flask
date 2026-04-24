from verbos import VERBOS_IRREGULARES, VERBOS_BASE

def corregir_futuro(mensaje):

    # separar palabras
    palabras = mensaje.split()

    # si ya tiene "will"
    if "will" in palabras:
        return mensaje, "La frase ya está en futuro."

    nueva_frase = []
    cambio = False

    # recorrer con índice
    for i, palabra in enumerate(palabras):

        if i == 1:
            nueva_frase.append("will")

            # si el verbo está en pasado irregular → convertir a base
            if palabra in VERBOS_BASE:
                nueva_frase.append(VERBOS_BASE[palabra])
            else:
                nueva_frase.append(palabra)

            cambio = True

        else:
            nueva_frase.append(palabra)

    resultado = " ".join(nueva_frase)

    if cambio:

        # explicación base
        explicacion = "Se detectó futuro y se añadió 'will'."

        # si se corrigió verbo de pasado a base
        if any(p in VERBOS_BASE for p in palabras):
            explicacion += " Además, se corrigió el verbo a su forma base."

        return resultado, explicacion

    return mensaje, None