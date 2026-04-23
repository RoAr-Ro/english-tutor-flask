# importa Flask, render_template y request
from verbos import verbos
from flask import Flask, request, render_template
import json
import os
from grammar.detector import detectar_tiempo
from grammar.past import corregir_pasado
from grammar.present import corregir_presente
from grammar.future import corregir_futuro

# crea la aplicación
app = Flask(__name__)

# nombre archivo historial
ARCHIVO = "historial.json"

# cargar historial desde json
def cargar_historial():

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []


# guardar historial en json
def guardar_historial(historial):

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=4)


# dejar solo últimos 10 mensajes
def limpiar_historial(historial):

    del historial[:-10]
    

# cargar historial si existe
historial = cargar_historial()

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

    # caso vacío
    if mensaje == "":
        return "Please write a sentence."

    # respuestas especiales (se mantienen)
    if mensaje == "hello":
        return "Hello! How are you?"

    if mensaje == "i am fine":
        return "Good sentence!"

    # detectar tipo de tiempo
    tiempo = detectar_tiempo(mensaje)

    # lógica por tipo
    if tiempo == "past":

        resultado, explicacion = corregir_pasado(mensaje)

        # si no cambió nada → no encontró verbo
        if resultado == mensaje:
            return "Sentence in past detected."

    elif tiempo == "future":
        resultado, explicacion = corregir_futuro(mensaje)

    else:
        resultado, explicacion = corregir_presente(mensaje)

    # formatear salida
    resultado_formateado = formatear_frase(resultado)
    mensaje_formateado = formatear_frase(mensaje)

    # si no hubo cambios
    if resultado_formateado == mensaje_formateado:
        return f"You wrote: {resultado_formateado}"

    # si sí hubo corrección
    if resultado_formateado == mensaje_formateado:
        return f"You wrote: {resultado_formateado}"

    if explicacion:
        return f"Corrected: {resultado_formateado}\nExplanation: {explicacion}"

    return f"Corrected: {resultado_formateado}"

# ruta principal
# acepta GET (abrir página) y POST (enviar formulario)
@app.route("/", methods=["GET", "POST"])
def home():

    # variable vacía al inicio
    respuesta = ""

    # si el usuario envió formulario
    if request.method == "POST":

        # obtener texto escrito por usuario
        mensaje = request.form["mensaje"]

        # llamar función correctora
        respuesta = corregir_frase(mensaje)

        # guardar historial
        historial.append(f"You: {mensaje}")
        historial.append(f"Tutor: {respuesta}")
        
        # conservar solo últimas 10 entradas
        limpiar_historial(historial)
        
        guardar_historial(historial)

        # enviar historial al HTML
    return render_template("index.html", respuesta=respuesta, historial=historial)


@app.route("/api/corregir", methods=["POST"])
def api_corregir():

    # leer JSON enviado
    data = request.get_json()

    # si no vino nada o no existe campo mensaje
    if not data or "mensaje" not in data:

        # devolver error + código 400
        return {
            "error": "mensaje requerido"
        }, 400

    # sacar mensaje recibido
    mensaje = data["mensaje"]

    # usar lógica existente
    respuesta = corregir_frase(mensaje)

    # devolver respuesta correcta
    return {
        "respuesta": respuesta
    }


# ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)