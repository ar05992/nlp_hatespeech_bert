FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install spacy
RUN python3 -m spacy download en_core_web_lg

COPY . /app

EXPOSE 8000