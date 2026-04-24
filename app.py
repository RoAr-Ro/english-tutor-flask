# venv\Scripts\python.exe app.py
# importa Flask, render_template y request
from verbos import VERBOS_IRREGULARES
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
        return "Please write a sentence.", None

    # respuestas especiales (se mantienen)
    if mensaje == "hello":
        return "Hello! How are you?", None

    if mensaje == "i am fine":
        return "Good sentence!", None

    # detectar tipo de tiempo
    tiempo = detectar_tiempo(mensaje)

    # lógica por tipo
    if tiempo == "past":

        resultado, explicacion = corregir_pasado(mensaje)

        # si no cambió nada → no encontró verbo
        if resultado == mensaje:
            return "Sentence in past detected.", None

    elif tiempo == "future":
        resultado, explicacion = corregir_futuro(mensaje)

    else:
        resultado, explicacion = corregir_presente(mensaje)

    # formatear salida
    resultado_formateado = formatear_frase(resultado)
    mensaje_formateado = formatear_frase(mensaje)

    
    if resultado_formateado == mensaje_formateado:
        return resultado_formateado, explicacion

    if explicacion:
        return resultado_formateado, explicacion

    if resultado_formateado == mensaje_formateado:
        return resultado_formateado, None

    return resultado_formateado, explicacion

# ruta principal de la aplicación
@app.route("/", methods=["GET", "POST"])
def home():

    # inicializa la variable explicacion para evitar errores si no hay POST
    explicacion = None

    # inicializa la respuesta vacía para evitar variable no definida
    respuesta = ""

    # verifica si el usuario envió el formulario (método POST)
    if request.method == "POST":

        # obtiene el texto que el usuario escribió en el input llamado "mensaje"
        mensaje = request.form["mensaje"]

        # llama a la función que corrige la frase y devuelve texto + explicación
        respuesta, explicacion = corregir_frase(mensaje)

        # agrega al historial lo que escribió el usuario
        historial.append(f"You: {mensaje}")

        # agrega al historial la respuesta del tutor
        historial.append(f"Tutor: {respuesta}")
        
        # limpia el historial para que solo tenga las últimas 10 entradas
        limpiar_historial(historial)
        
        # guarda el historial en almacenamiento (archivo o memoria persistente)
        guardar_historial(historial)

    # renderiza la plantilla HTML enviando respuesta, explicación e historial
    return render_template(
        "index.html",
        respuesta=respuesta,
        explicacion=explicacion,
        historial=historial
    )


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
    texto, explicacion = corregir_frase(mensaje)

    # devolver respuesta correcta
    return {
        "respuesta": texto,
        "explicacion": explicacion
    }


# ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)