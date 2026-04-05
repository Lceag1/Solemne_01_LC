from fastapi.testclient import TestClient
from main import app

# Creamos un cliente de pruebas basado en tu app
client = TestClient(app)


def test_read_root():
    # Prueba para la ruta raíz
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Servidor funcionando correctamente"}


def test_get_shoa_time():
    # Prueba para tu ruta de la hora
    response = client.get("/time")

    # 1. Verificamos que el servidor responda OK (200)
    assert response.status_code == 200

    # 2. Obtenemos el JSON de respuesta
    data = response.json()

    # 3. Verificamos que la llave "hora_oficial" exista en el JSON
    assert "hora_oficial" in data

    # 4. Verificamos que el formato cumpla con la rúbrica (19 caracteres)
    # Ejemplo: "2026-04-05 20:32:16" tiene exactamente 19 caracteres de largo
    assert len(data["hora_oficial"]) == 19

    # 5. Verificamos que el formato contenga el guion del año-mes-día
    assert "-" in data["hora_oficial"]

    # 6. Verificamos que el formato contenga los dos puntos de la hora
    assert ":" in data["hora_oficial"]
