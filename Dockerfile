FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend app code
COPY backend/app /app/app
COPY backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PYTHONPATH=/app

CMD ["/app/start.sh"]
