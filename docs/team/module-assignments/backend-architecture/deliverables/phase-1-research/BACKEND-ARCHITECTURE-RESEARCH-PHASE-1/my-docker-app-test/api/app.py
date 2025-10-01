from fastapi import FastAPI, Depends
import psycopg2, os, redis

app = FastAPI()

db_url = os.getenv("DATABASE_URL")
r = redis.Redis.from_url(os.getenv("REDIS_URL"))

@app.get("/")
def health():
    return {"status": "ok"}