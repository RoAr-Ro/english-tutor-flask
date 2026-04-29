from verbos import VERBOS_IRREGULARES
from flask import Flask, request, render_template, session
import json
import os
from grammar.detector import detectar_tiempo
from grammar.past import corregir_pasado
from grammar.present import corregir_presente
from grammar.future import corregir_futuro
from assessment import PREGUNTAS_NIVEL, evaluar_nivel
from core import corregir_frase
from tutor import obtener_ejercicio
from curriculum import CURRICULO
from flask import redirect
from core import corregir_frase, evaluar_respuesta

# crea la aplicación Flask
app = Flask(__name__)

# clave secreta necesaria para usar session (guardar datos del usuario)
app.secret_key = "clave_secreta"

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

# =========================
# PROGRESO USUARIO
# =========================

ARCHIVO_PROGRESO = "progreso.json"

# cargar progreso
def cargar_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# guardar progreso
def guardar_progreso(data):
    with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# =========================
# ESTADO ASSESSMENT
# =========================

respuestas_usuario = []
indice_pregunta = 0
modo_assessment = False

# =========================
# ESTADO TUTOR
# =========================

indice_ejercicio = 0
modo_tutor = False


# ruta principal de la aplicación
@app.route("/", methods=["GET", "POST"])
def home():
    
    # índice del ejercicio actual
    indice_ejercicio = session.get("indice_ejercicio", 0)
    
    # índice del tema actual (para avanzar entre temas)
    indice_tema = session.get("indice_tema", 0)
    
    # obtiene modo actual de la app
    modo = session.get("modo", "normal")
    
    # obtiene si hubo acierto en la respuesta anterior
    # pop lo usa una vez y lo borra automáticamente
    acierto = session.pop("acierto", False)

    # obtiene el nivel guardado del usuario (si existe)
    nivel = session.get("nivel")
    
    # cargar progreso guardado
    progreso = cargar_progreso()

    if "usuario_demo" in progreso:
        session["indice_tema"] = progreso["usuario_demo"].get("indice_tema", 0)
        session["indice_ejercicio"] = progreso["usuario_demo"].get("indice_ejercicio", 0)

    # inicializa la variable explicacion para evitar errores si no hay POST
    explicacion = None

    # inicializa la respuesta vacía para evitar variable no definida
    respuesta = ""
    
    # variables del tutor
    teoria = None
    ejercicio = None

    if modo == "tutor":

        subnivel = "beginner_1"
        temas = CURRICULO.get(subnivel, [])

        if temas:
            # evita que el índice se salga del rango
            if indice_tema >= len(temas):
                indice_tema = 0

            # selecciona el tema actual según el índice
            tema_actual = temas[indice_tema]

            # ✔ la teoría NO cambia
            teoria = tema_actual["teoria"]

            # 🔥 nueva lógica de ejercicios
            lista_ejercicios = tema_actual["ejercicios"]

            # si terminó todos los ejercicios del tema
            if indice_ejercicio >= len(lista_ejercicios):

                # avanzar al siguiente tema
                session["indice_tema"] = indice_tema + 1

                # reiniciar ejercicios desde 0
                session["indice_ejercicio"] = 0

                # recargar para mostrar nuevo tema
                return redirect("/")

            ejercicio_data = lista_ejercicios[indice_ejercicio]

            ejercicio = ejercicio_data["instruccion"]
    
    
    # verifica si el usuario envió el formulario (método POST)
    if request.method == "POST":

        # obtiene el texto que el usuario escribió en el input llamado "mensaje"
        mensaje = request.form["mensaje"]

        if modo == "tutor":

            subnivel = "beginner_1"
            temas = CURRICULO.get(subnivel, [])
            tema_actual = temas[0]

            # obtener respuesta esperada
            respuesta_esperada = lista_ejercicios[indice_ejercicio]["respuesta_esperada"]

            # evaluar
            correcto, texto_corregido = evaluar_respuesta(mensaje, respuesta_esperada)

            respuesta = texto_corregido

            if correcto:
                # guardar que acertó
                session["acierto"] = True

                # avanzar ejercicio
                session["indice_ejercicio"] = indice_ejercicio + 1
                
                # cargar progreso actual
                progreso = cargar_progreso()

                # usamos "usuario_demo" temporal (luego será login)
                progreso["usuario_demo"] = {
                    "nivel": nivel,
                    "indice_tema": session.get("indice_tema", 0),
                    "indice_ejercicio": session.get("indice_ejercicio", 0)
                }

                # guardar en archivo
                guardar_progreso(progreso)

                return redirect("/")
            else:
                explicacion = f"❌ Try again. Expected: {respuesta_esperada}"

        else:
            # modo normal
            respuesta, explicacion = corregir_frase(mensaje)
        
        # adapta el comportamiento según el nivel del usuario
        if explicacion is None:

            if nivel == "beginner":
                explicacion = "Try simple sentences: I eat, She goes, I went."

            elif nivel == "intermediate":
                explicacion = "Good. Try adding more detail to your sentence."

            elif nivel == "advanced":
                explicacion = "Correct. Try using more complex grammar (perfect tenses, connectors)."

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
        historial=historial,
        nivel=nivel,
        modo=modo,
        teoria=teoria,
        ejercicio=ejercicio,
        acierto=acierto
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


@app.route("/assessment")
def iniciar_assessment():
    global respuestas_usuario, indice_pregunta, modo_assessment

    respuestas_usuario = []
    indice_pregunta = 0
    modo_assessment = True

    return render_template(
        "assessment.html",
        pregunta=PREGUNTAS_NIVEL[indice_pregunta]
    )


@app.route("/assessment/responder", methods=["POST"])
def responder_assessment():
    global respuestas_usuario, indice_pregunta, modo_assessment

    # obtiene respuesta del usuario
    respuesta = request.form["mensaje"]

    # guarda respuesta
    respuestas_usuario.append(respuesta)

    # avanza a siguiente pregunta
    indice_pregunta += 1

    # si aún hay preguntas
    if indice_pregunta < len(PREGUNTAS_NIVEL):
        return render_template(
            "assessment.html",
            pregunta=PREGUNTAS_NIVEL[indice_pregunta]
        )

    # si terminó el assessment
    nivel = evaluar_nivel(respuestas_usuario)

    # guarda el nivel del usuario en la sesión
    session["nivel"] = nivel

    # desactiva modo assessment
    modo_assessment = False

    # activar modo tutor
    session["modo"] = "tutor"

    # redirigir a home (misma página principal)
    return redirect("/")
    

# ruta para iniciar tutor guiado
@app.route("/tutor")
def iniciar_tutor():
    
    # DEBUG: ver qué está cargando realmente
    print(CURRICULO)

    # obtiene nivel del usuario (por defecto beginner)
    nivel = session.get("nivel", "beginner")

    # por ahora siempre usamos beginner_1 (luego lo haremos dinámico)
    subnivel = "beginner_1"

    # obtiene lista de temas del currículo
    temas = CURRICULO.get(subnivel, [])

    # tomar primer tema
    if not temas:
        return "No curriculum found. Check curriculum.py"

    tema_actual = temas[0]

    # obtener teoría del tema
    teoria = tema_actual["teoria"]

    # obtener primer ejercicio
    ejercicio = tema_actual["ejercicios"][0]["instruccion"]

    # renderizar template del tutor
    return render_template(
        "tutor.html",
        teoria=teoria,
        ejercicio=ejercicio
    )
    
    
@app.route("/tutor/responder", methods=["POST"])
def responder_tutor():
    global indice_ejercicio, modo_tutor

    nivel = session.get("nivel", "beginner")

    respuesta_usuario = request.form["mensaje"]

    # corregir respuesta
    texto, explicacion = corregir_frase(respuesta_usuario)

    indice_ejercicio += 1

    siguiente = obtener_ejercicio(nivel, indice_ejercicio)

    return render_template(
        "tutor.html",
        ejercicio=siguiente,
        respuesta=texto,
        explicacion=explicacion
    )

# ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)