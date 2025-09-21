from fastapi import FastAPI, UploadFile, File
from celery import Celery
import os, uuid

app = FastAPI(title="SlideForge AI API")
celery = Celery(__name__, broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))

@app.get("/health")
def health():
    return {"status": "ok"}

@celery.task
def ingest(file_path: str):
    # placeholder – calls whisper, llama, etc.
    return {"task": "ingested", "file": file_path}

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    uid = uuid.uuid4().hex
    path = f"/tmp/{uid}_{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    ingest.delay(path)
    return {"uid": uid, "message": "file queued"}