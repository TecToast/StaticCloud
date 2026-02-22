import os
import hashlib
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Form
from fastapi.staticfiles import StaticFiles

UPLOAD_DIR = "/images"
UPLOAD_TOKEN = os.getenv("UPLOAD_TOKEN")
app = FastAPI()

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/i", StaticFiles(directory=UPLOAD_DIR), name="images")

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    authorization: str = Header(None),
    hash_length: int = Form(16)
):
    if authorization != f"Bearer {UPLOAD_TOKEN}":
        raise HTTPException(status_code=401)

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        raise HTTPException(status_code=400)

    file_hash = hashlib.sha256()
    file_content = await file.read()
    file_hash.update(file_content)
    hash_hex = file_hash.hexdigest()[:hash_length]

    unique_key = hash_hex + ext
    file_path = os.path.join(UPLOAD_DIR, unique_key)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

    return unique_key