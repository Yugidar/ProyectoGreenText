FROM python:3.12-slim

RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
USER appuser

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "print('ok')" || exit 1

CMD ["python", "mod.py"]
