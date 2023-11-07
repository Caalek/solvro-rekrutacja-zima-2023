# Solvro Rekrutacja Zima 2023 - Backend
System przydzielający zadania developerom wykonany na rekrutację do KN Solvro napisany w Pythonie przy użyciu FastAPI i SQLAlchemy (SQLite jako backend)

## Jak odpalić
1. Klonujemy repo i wchodzimy do folderu
```
git clone https://github.com/Caalek/solvro-rekrutacja-zima-2023
cd
```
2. Pobieramy `pip`em niezbędne paczki:
```
pip install -r requirements.txt
```
3. Odpalamy używając:
```
uvicorn app.main:app --reload
```
4. Aplikacja będzie dostępna na `http://localhost:8000`. Na `http://localhost:8000/docs` będzie automatycznie wygenerowana przez FastAPI interaktywna dokumentacja, w której można sprawdzić działanie API.

## Jak odpalić w dockerze
1. Pobieramy plik `docker-compose.yml`
```
wget https://raw.githubusercontent.com/Caalek/solvro-rekrutacja-zima-2023/main/docker-compose.yml
```
2. Odpalamy
```
docker compose up -d
```
