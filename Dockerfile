FROM python:3.9.7-slim

WORKDIR /app

COPY src/ src/
COPY ["app.py", "requirements.txt",  "./"]

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install uvicorn==0.18.2 \
    && pip install --ignore-installed Flask==2.1.0

EXPOSE 9696

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9696"]