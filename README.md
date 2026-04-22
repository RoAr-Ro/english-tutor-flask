# English Tutor with Flask

A beginner-friendly backend project built with Python, Flask, and Pytest.

This application helps correct simple English sentences, stores conversation history, and exposes a REST API for external use.

---

## Live Demo

https://english-tutor-flask.onrender.com

---

## Features

- Corrects simple past tense mistakes
- Web interface with Flask
- REST API endpoint
- JSON conversation history storage
- Automated tests with Pytest
- Modular project structure

---

## Example Corrections

Input: i go yesterday  
Output: I went yesterday.

Input: i see a movie yesterday  
Output: I saw a movie yesterday.

Input: i write a letter yesterday  
Output: I wrote a letter yesterday.

---

## Project Structure

english_tutor/

- app.py
- verbos.py
- historial.json
- test_app.py
- README.md
- templates/
  - index.html

---

## Installation

Create virtual environment:

python -m venv venv

Activate environment (Windows):

venv\Scripts\activate

Install dependencies:

pip install flask pytest

---

## Run the Project

python app.py

Open in browser:

http://127.0.0.1:5000

---

## Run Tests

pytest

---

## API Usage

Endpoint:

POST /api/corregir

Request:

{
  "mensaje": "i go yesterday"
}

Response:

{
  "respuesta": "Corrected: I went yesterday."
}

Error Example:

{
  "error": "mensaje requerido"
}

---

## Technologies Used

- Python
- Flask
- Pytest
- JSON
- HTML

---

## Learning Goals

- Python fundamentals
- Functions and modules
- Flask routes
- REST APIs
- Testing with Pytest
- Clean code and refactoring

---

## Author

Rocio Ruiz