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
    
        # separar palabras de la frase
    palabras = mensaje.split()

    # lista de sujetos válidos
    SUJETOS = ["i", "you", "he", "she", "it", "we", "they"]

    # validar estructura básica: sujeto + verbo
    if len(palabras) < 2 or palabras[0] not in SUJETOS:
        return formatear_frase(mensaje), "structure"

    if mensaje == "":
        return "Please write a sentence.", "system"

    if mensaje == "hello":
        return "Hello! How are you?", "system"

    if mensaje == "i am fine":
        return "Good sentence!", "system"

    # detectar tiempo
    tiempo = detectar_tiempo(mensaje)

    # aplicar corrección según tiempo
    if tiempo == "past":
        resultado, explicacion = corregir_pasado(mensaje)

    elif tiempo == "future":
        resultado, explicacion = corregir_futuro(mensaje)

    else:
        resultado, explicacion = corregir_presente(mensaje)

    # formatear
    resultado_formateado = formatear_frase(resultado)
    mensaje_formateado = formatear_frase(mensaje)

    # si no hubo cambios → devolver con explicación si existe
    if resultado_formateado == mensaje_formateado:
        return resultado_formateado, explicacion

    # si hubo cambios
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