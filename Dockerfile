FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -m -u 1000 appuser
COPY main.py .
RUN chown -R appuser:appuser /app
RUN mkdir -p /images && chown -R appuser:appuser /images
USER appuser
VOLUME ["/images"]
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]