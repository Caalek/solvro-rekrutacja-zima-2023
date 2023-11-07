FROM python:3-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]    