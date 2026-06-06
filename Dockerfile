FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home appuser
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --upgrade pip && pip install --no-cache-dir .
USER appuser
EXPOSE 8010
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health').read()"
CMD ["uvicorn", "consumer_service.api:app", "--host", "0.0.0.0", "--port", "8010"]
