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
    texto, explicacion = corregir_frase("")
    assert texto == "Please write a sentence."
    assert explicacion is None


def test_solo_espacios():
    texto, explicacion = corregir_frase("   ")
    assert texto == "Please write a sentence."
    assert explicacion is None

def test_unknown_text():
    texto, explicacion = corregir_frase("good morning")
    assert texto == "Good morning."
    assert explicacion is None


def test_texto_normal():
    texto, explicacion = corregir_frase("i like pizza")
    assert texto == "I like pizza."
    assert explicacion is None
    
    
# -------------------------
# RESPUESTAS FIJAS
# -------------------------

def test_hello():
    texto, explicacion = corregir_frase("hello")
    assert texto == "Hello! How are you?"
    assert explicacion is None


def test_fine():
    texto, explicacion = corregir_frase("i am fine")
    assert texto == "Good sentence!"
    assert explicacion is None
    
    
# -------------------------
# PASADO
# -------------------------

@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("i go yesterday", "I went yesterday."),
        ("i eat pizza yesterday", "I ate pizza yesterday."),
        ("i see Ana yesterday", "I saw ana yesterday."),
    ]
)
def test_pasado_varios(entrada, esperado):
    texto, explicacion = corregir_frase(entrada)
    assert texto == esperado
    assert explicacion is not None


def test_run_yesterday():
    texto, explicacion = corregir_frase("i run yesterday")
    assert texto == "I ran yesterday."
    assert explicacion is not None


def test_write_yesterday():
    texto, explicacion = corregir_frase("i write a letter yesterday")
    assert texto == "I wrote a letter yesterday."
    assert explicacion is not None


def test_yesterday_sin_verbo():
    texto, explicacion = corregir_frase("party yesterday")
    assert texto is not None
    assert explicacion is not None
    
    
# -------------------------
# PRESENTE
# -------------------------

def test_presente_he():
    texto, explicacion = corregir_frase("he go")
    assert texto == "He goes."
    assert explicacion is not None

def test_presente_she():
    texto, explicacion = corregir_frase("she eat")
    assert texto == "She eats."
    assert explicacion is not None

def test_presente_it():
    texto, explicacion = corregir_frase("it watch tv")
    assert texto == "It watches tv."
    assert explicacion is not None

def test_presente_i():
    texto, explicacion = corregir_frase("i go")
    assert texto == "I go."
    assert explicacion is None
    
    
# -------------------------
# FUTURO
# -------------------------

def test_futuro_i():
    texto, explicacion = corregir_frase("i go tomorrow")
    assert texto == "I will go tomorrow."
    assert explicacion is not None

def test_futuro_he():
    texto, explicacion = corregir_frase("he eat tomorrow")
    assert texto == "He will eat tomorrow."
    assert explicacion is not None

def test_futuro_already():
    texto, explicacion = corregir_frase("i will go tomorrow")
    assert texto == "I will go tomorrow."
    assert explicacion is not None
    
    
# -------------------------
# API
# -------------------------

def test_api_corregir(client):
    response = client.post("/api/corregir", json={"mensaje": "i go yesterday"})
    assert response.status_code == 200

    data = response.get_json()

    assert data["respuesta"] == "I went yesterday."
    assert data["explicacion"] is not None


def test_api_error_sin_mensaje(client):
    response = client.post("/api/corregir", json={})
    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "mensaje requerido"