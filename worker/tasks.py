from celery import Celery
import os
celery = Celery(__name__, broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))

@celery.task(bind=True)
def ingest(self, file_path: str):
    # TODO: plug in whisper, llama, etc.
    return {"status": "ingested", "path": file_path}