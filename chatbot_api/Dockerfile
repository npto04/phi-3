# chatbot_api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

COPY app/ /app

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]