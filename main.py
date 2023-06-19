# Importa bibliotecas necessárias
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Body
from fastapi.responses import FileResponse, StreamingResponse
import os
from supabase import create_client, Client
import asyncio
import aiofiles
import time

# Cria servidor
app = FastAPI()

# Dados para conexão com o supabase
url: str = 'https://fcyxjwnvevvrghiyihkg.supabase.co'
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjeXhqd252ZXZ2cmdoaXlpaGtnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4Njc3MTYwOCwiZXhwIjoyMDAyMzQ3NjA4fQ.SEJlTDPEyJ1Uhrikd93X03U7hywEuE79KUaCrkm8j7o"
supabase: Client = create_client(url, key)
bucket_name: str = "Rachaduras"

# Rota GET para visualizar itens no bucket
@app.get("/list")
async def list():
    # Lista todas as imagens do Bucket
    res = supabase.storage.from_(bucket_name).list()
    return res

# Rota POST para salvar imagem no 'recebidos' e também no Supabase
@app.post("/upload")
def upload(content: UploadFile = fastapi.File(...)):

    # Cria nome do arquivo como imagem png
    filename = f'pic{time.time()}.png'

    # Salva imagem nos recebidos
    with open(f"recebidos/{filename}", 'wb') as f:
        dados = content.file.read()
        f.write(dados)

    # Abre imagem dos recebidos e envia para o Supabase, adicionando o timestamp ao nome do arquivo
    with open(os.path.join("./recebidos", filename), 'rb+') as f:
        dados = f.read()
        res = supabase.storage.from_(bucket_name).upload(f"{time.time()}_{filename}", dados)
        print(res)
        
    return {"status": "ok"}
