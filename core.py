from grammar.detector import detectar_tiempo
from grammar.past import corregir_pasado
from grammar.present import corregir_presente
from grammar.future import corregir_futuro


# función para mejorar presentación de frases
def formatear_frase(texto):

    # primera letra mayúscula
    texto = texto.capitalize()

    # agregar punto final si no existe
    if not texto.endswith("."):
        texto += "."

    return texto


# función principal que coordina todo
def corregir_frase(mensaje):

    # normalizar texto
    mensaje = mensaje.lower().strip()

    # ------------------------
    # CASOS ESPECIALES
    # ------------------------

    if mensaje == "":
        return "Please write a sentence.", None

    if mensaje == "hello":
        return "Hello! How are you?", None

    if mensaje == "i am fine":
        return "Good sentence!", None

    # ------------------------
    # DETECTAR TIEMPO
    # ------------------------

    tiempo = detectar_tiempo(mensaje)

    palabras = mensaje.split()
    SUJETOS = ["i", "you", "he", "she", "it", "we", "they"]

    # caso especial: pasado sin estructura
    if tiempo == "past" and (len(palabras) < 2 or palabras[0] not in SUJETOS):
        return formatear_frase(mensaje), "Past detected but sentence structure is incorrect."

    # validación normal
    if len(palabras) < 2 or palabras[0] not in SUJETOS:
        return formatear_frase(mensaje), None

    # ------------------------
    # CORRECCIÓN POR TIEMPO
    # ------------------------

    if tiempo == "past":
        resultado, explicacion = corregir_pasado(mensaje)

    elif tiempo == "future":
        resultado, explicacion = corregir_futuro(mensaje)

    else:
        resultado, explicacion = corregir_presente(mensaje)

    # ------------------------
    # FORMATEO
    # ------------------------

    resultado_formateado = formatear_frase(resultado)
    mensaje_formateado = formatear_frase(mensaje)

    # ------------------------
    # SIN CAMBIOS
    # ------------------------

    if resultado_formateado == mensaje_formateado:

        if "will" in mensaje:
            return resultado_formateado, "Already correct future."

        return resultado_formateado, None

    # ------------------------
    # CON CAMBIOS
    # ------------------------

    return resultado_formateado, explicacion


# =====================================
# EVALUAR RESPUESTA DEL TUTOR
# =====================================

def evaluar_respuesta(respuesta_usuario, respuesta_esperada):

    # corregir (solo para mostrar después)
    texto_corregido, _ = corregir_frase(respuesta_usuario)

    # 🔥 usar texto ORIGINAL para evaluar
    usuario = respuesta_usuario.lower().strip()
    esperado = respuesta_esperada.lower().strip()

    # validar coincidencia más estricta
    if usuario == esperado:
        return True, texto_corregido

    return False, texto_corregido