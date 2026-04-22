# importa Flask, render_template y request
from verbos import verbos
from flask import Flask, request, render_template
import json
import os

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

# función que corrige frases
def corregir_frase(mensaje):

    # convierte texto a minúsculas
    mensaje = mensaje.lower()
    
    # quita espacios al inicio y al final de la frase
    mensaje = mensaje.strip()

    # verifica si el mensaje está vacío
    if mensaje == "":
        return "Please write a sentence."

    # si escribió yesterday
    if "yesterday" in mensaje:

        # revisar verbos
        for presente, pasado in verbos.items():

            if presente in mensaje:

                # separar frase en palabras
                palabras = mensaje.split()

                # recorrer posiciones
                for i in range(len(palabras)):

                    # si palabra exacta coincide
                    if palabras[i] == presente:
                        palabras[i] = pasado

                # unir frase

                frase_corregida = " ".join(palabras)

                frase_corregida = formatear_frase(frase_corregida)

                return f"Corrected: {frase_corregida}"

        return "Sentence in past detected."

    elif mensaje == "hello":
        return "Hello! How are you?"

    elif mensaje == "i am fine":
        return "Good sentence!"

    else:
        mensaje = formatear_frase(mensaje)

        return f"You wrote: {mensaje}"

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