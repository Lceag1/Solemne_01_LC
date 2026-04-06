# Proyecto Solemne 1 Luis Cea
Aplicacion FastAPI que obtiene la hora oficial de Chile Continental por medio de Scrapping a https://www.horaoficial.cl/, exponiendo la información en formato Año-Mes-Día Hora:Minuto:Segundo.
### Estado del Pipeline (CI/CD)
[![Pipeline CI/CD](https://github.com/Lceag1/Solemne_01_LC/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Lceag1/Solemne_01_LC/actions)

### Para Ejecutar: 
```bash
docker run -p 8000:8000 luiscea1/solemne-api:latest