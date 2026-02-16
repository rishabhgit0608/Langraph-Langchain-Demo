from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
