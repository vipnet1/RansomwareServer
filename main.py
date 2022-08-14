from turtle import back
from fastapi import FastAPI, Request
import backend

app = FastAPI()

# backend.generate_keys()
backend.read_keys()

@app.post("/")
async def decript_fernet_key(request: Request):
    key: bytes = await request.body()
    return backend.decript_fernet_key(key)