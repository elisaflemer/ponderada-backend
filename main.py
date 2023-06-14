
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Body
from fastapi.responses import FileResponse, StreamingResponse
import os
from supabase import create_client, Client
import asyncio
import aiofiles
import time

app = FastAPI()

# URL e Chave de acesso
url: str = 'https://fcyxjwnvevvrghiyihkg.supabase.co'
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjeXhqd252ZXZ2cmdoaXlpaGtnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4Njc3MTYwOCwiZXhwIjoyMDAyMzQ3NjA4fQ.SEJlTDPEyJ1Uhrikd93X03U7hywEuE79KUaCrkm8j7o"
supabase: Client = create_client(url, key)
#Nome do bucket utilizado
bucket_name: str = "Rachaduras"
@app.get("/list")
async def list():
    # Lista todas as imagens do Bucket
    res = supabase.storage.from_(bucket_name).list()
    print(res)
    return res

@app.post("/upload")
def upload(content: UploadFile = fastapi.File(...)):
    with open(f"./recebidos/fire{time.time()}.png", 'wb') as f:
        dados = content.file.read()
        f.write(dados)
    return {"status": "ok"}