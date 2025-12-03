FROM python:3.11-slim

WORKDIR /app

# Install FastAPI + auth + DB support
RUN pip install --no-cache-dir \
    fastapi uvicorn[standard] \
    psycopg2-binary sqlalchemy \
    pydantic[email] python-jose[cryptography] passlib[bcrypt]

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
