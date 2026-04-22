import pytest

# importar función desde app.py
from app import app, corregir_frase   # importar la app Flask y función a testear

@pytest.fixture                 # indica que esto es recurso reutilizable para tests
def client():

    app.config["TESTING"] = True   # activar modo testing en Flask

    # crear cliente falso que simula navegador/app
    with app.test_client() as client:

        yield client   # entregar cliente al test que lo necesite



# test 1
def test_go_yesterday():
    assert corregir_frase("i go yesterday") == "Corrected: I went yesterday."


# test 2
def test_hello():
    assert corregir_frase("hello") == "Hello! How are you?"


# test 3
def test_fine():
    assert corregir_frase("i am fine") == "Good sentence!"

# test 4    
def test_eat_yesterday():
    assert corregir_frase("i eat pizza yesterday") == "Corrected: I ate pizza yesterday."

# test 5
def test_unknown_text():
    assert corregir_frase("good morning") == "You wrote: Good morning."
    
    
@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("i go yesterday", "Corrected: I went yesterday."),
        ("i eat pizza yesterday", "Corrected: I ate pizza yesterday."),
        ("i see Ana yesterday", "Corrected: I saw ana yesterday."),
    ]
)
def test_varios_verbos(entrada, esperado):
    assert corregir_frase(entrada) == esperado
    
    
def test_texto_vacio():
    assert corregir_frase("") == "Please write a sentence."


def test_solo_espacios():
    assert corregir_frase("   ") == "Please write a sentence."


def test_yesterday_sin_verbo():
    assert corregir_frase("party yesterday") == "Sentence in past detected."


def test_mayusculas():
    assert corregir_frase("I GO YESTERDAY") == "Corrected: I went yesterday."
    
def test_run_yesterday():
    assert corregir_frase("i run yesterday") == "Corrected: I ran yesterday."


def test_write_yesterday():
    assert corregir_frase("i write a letter yesterday") == "Corrected: I wrote a letter yesterday."
    
    
def test_texto_normal():
    assert corregir_frase("i like pizza") == "You wrote: I like pizza."
    

def test_api_corregir(client):   # test recibe cliente fixture

    # enviar petición POST a la ruta API
    response = client.post(

        "/api/corregir",   # endpoint a probar

        json={
            "mensaje": "i go yesterday"   # datos enviados en JSON
        }
    )

    # verificar código HTTP correcto
    assert response.status_code == 200

    # convertir respuesta JSON a diccionario Python
    data = response.get_json()

    # verificar contenido esperado
    assert data["respuesta"] == "Corrected: I went yesterday."
    
def test_api_error_sin_mensaje(client):

    # enviar JSON vacío
    response = client.post(
        "/api/corregir",
        json={}
    )

    # debe responder error cliente
    assert response.status_code == 400

    # leer json respuesta
    data = response.get_json()

    # validar mensaje error
    assert data["error"] == "mensaje requerido"