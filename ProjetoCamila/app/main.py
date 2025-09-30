#projeto feito por: samuka-ang

from fastapi import FastAPI
from app.controllers import router as dados_router

app = FastAPI()

app.include_router(dados_router)

@app.get("/")
def read_root():
    return {"message": "Api Camila"}
