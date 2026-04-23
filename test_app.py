import pytest
from app import app, corregir_frase


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

# -------------------------
# GENERAL
# -------------------------

def test_texto_vacio():
    assert corregir_frase("") == "Please write a sentence."

def test_solo_espacios():
    assert corregir_frase("   ") == "Please write a sentence."

def test_unknown_text():
    assert corregir_frase("good morning") == "You wrote: Good morning."

def test_texto_normal():
    assert corregir_frase("i like pizza") == "You wrote: I like pizza."
    
    
# -------------------------
# RESPUESTAS FIJAS
# -------------------------

def test_hello():
    assert corregir_frase("hello") == "Hello! How are you?"

def test_fine():
    assert corregir_frase("i am fine") == "Good sentence!"
    
    
# -------------------------
# PASADO
# -------------------------

@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("i go yesterday", "Corrected: I went yesterday."),
        ("i eat pizza yesterday", "Corrected: I ate pizza yesterday."),
        ("i see Ana yesterday", "Corrected: I saw ana yesterday."),
    ]
)
def test_pasado_varios(entrada, esperado):
    resultado = corregir_frase(entrada)
    assert esperado in resultado
    assert "Explanation:" in resultado


def test_run_yesterday():
    resultado = corregir_frase("i run yesterday")
    assert "Corrected: I ran yesterday." in resultado
    assert "Explanation:" in resultado


def test_write_yesterday():
    resultado = corregir_frase("i write a letter yesterday")
    assert "Corrected: I wrote a letter yesterday." in resultado
    assert "Explanation:" in resultado


def test_yesterday_sin_verbo():
    assert corregir_frase("party yesterday") == "Sentence in past detected."
    
    
# -------------------------
# PRESENTE
# -------------------------

def test_presente_he():
    resultado = corregir_frase("he go")
    assert "Corrected: He goes." in resultado
    assert "Explanation:" in resultado

def test_presente_she():
    resultado = corregir_frase("she eat")
    assert "Corrected: She eats." in resultado
    assert "Explanation:" in resultado

def test_presente_it():
    resultado = corregir_frase("it watch tv")
    assert "Corrected: It watches tv." in resultado
    assert "Explanation:" in resultado

def test_presente_i():
    assert corregir_frase("i go") == "You wrote: I go."
    
    
# -------------------------
# FUTURO
# -------------------------

def test_futuro_i():
    resultado = corregir_frase("i go tomorrow")
    assert "Corrected: I will go tomorrow." in resultado
    assert "Explanation:" in resultado

def test_futuro_he():
    resultado = corregir_frase("he eat tomorrow")
    assert "Corrected: He will eat tomorrow." in resultado
    assert "Explanation:" in resultado

def test_futuro_already():
    assert corregir_frase("i will go tomorrow") == "You wrote: I will go tomorrow."
    
    
# -------------------------
# API
# -------------------------

def test_api_corregir(client):
    response = client.post("/api/corregir", json={"mensaje": "i go yesterday"})
    assert response.status_code == 200

    data = response.get_json()

    assert "Corrected: I went yesterday." in data["respuesta"]
    assert "Explanation:" in data["respuesta"]


def test_api_error_sin_mensaje(client):
    response = client.post("/api/corregir", json={})
    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "mensaje requerido"