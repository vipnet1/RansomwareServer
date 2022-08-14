from fastapi import FastAPI
import backend

app = FastAPI()

# backend.generate_keys()
backend.read_keys()

@app.get("/")
def read_root():
    return 'Hello, Please GIVE MONEY'