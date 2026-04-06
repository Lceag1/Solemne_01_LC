from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock

# Creamos un cliente de pruebas basado en tu app
client = TestClient(app)


def test_read_root():
    # Prueba para la ruta raíz
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Servidor funcionando correctamente"}


# El decorador @patch intercepta la llamada a requests.get dentro de main.py
@patch("main.requests.get")
def test_get_shoa_time(mock_get):
    # 1. Configuramos el "doble de acción" (Mock)
    # Simulamos que el SHOA nos devolvió exactamente el texto que descubriste
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "20:32:16:05:04:2026:0"  # Un texto de prueba

    # Le decimos a mock_get que devuelva esta respuesta falsa
    mock_get.return_value = mock_response

    # 2. Hacemos la petición a nuestra API (creerá que contactó al SHOA real)
    response = client.get("/time")

    # 3. Verificamos que todo funcione
    assert response.status_code == 200

    data = response.json()
    assert "hora_oficial" in data
    assert len(data["hora_oficial"]) == 19
    assert "-" in data["hora_oficial"]
    assert ":" in data["hora_oficial"]
