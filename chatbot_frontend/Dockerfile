FROM python:3.11-slim
LABEL authors="Ney de Oliveira <neyoliveira.data@gmail.com"

WORKDIR /app

COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

COPY . /app

CMD ["sh", "entrypoint.sh"]