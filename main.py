from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="API Hora SHOA")


@app.get("/")
def read_root():
    return {"status": "Servidor funcionando correctamente"}


@app.get("/time")
def get_shoa_time():
    url = "http://www.horaoficial.cl/hora_server.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "http://www.horaoficial.cl/",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Respuesta viene como: "20:32:16:05:04:2026:0"
        # Formato:              HH:MM:SS:DD:MES:AAAA:?
        partes = response.text.strip().split(":")

        if len(partes) < 6:
            raise HTTPException(
                status_code=500,
                detail=f"Formato inesperado del servidor SHOA: '{response.text}'",
            )

        hora_utc = partes[0].zfill(2)
        minuto = partes[1].zfill(2)
        segundo = partes[2].zfill(2)
        dia = partes[3].zfill(2)
        mes = partes[4].zfill(2)
        anio = partes[5]

        # Convertimos UTC a Chile Continental (UTC-4 en verano, UTC-3 en invierno)
        # El sitio ya entrega la hora UTC, ajustamos -4 horas para Chile Continental
        hora_continental = (int(hora_utc) - 4) % 24

        hora_formateada = (
            f"{anio}-{mes}-{dia} {str(hora_continental).zfill(2)}:{minuto}:{segundo}"
        )

        return {"hora_oficial": hora_formateada}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error de red: {str(e)}")
