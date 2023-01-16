from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import json, os

app = FastAPI()
#http://127.0.0.1:8000/docs //redoc
# python3 -m uvicorn main:app --reload

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class libro(BaseModel):
    titulo: str
    autor: str
    paginas: Optional[int]

@app.get("/")
async def root():
    return {"message": "Hello World"}

#Iniciar api Dead by Daylight
@app.get("/dbd/perks")
async def perks_general():
    return {"message": "Aqui te mostrara las opciones de perks"}

@app.get("/dbd/perks/{perk}")
async def perks(perk: str):
    if perk.isnumeric():
        with open("dbd/perks.json", "r") as file:
            perks = json.load(file)
            perk = perks[perk]
            return perk
    if not perk.isnumeric():
                encontrado = False
                with open("dbd/mapeo.json", "r", encoding="utf-8") as f:
                    mapeo = json.load(f)
                    for i in mapeo['perks']:
                        for j in mapeo['perks'][str(i)]['names']:
                            if mapeo['perks'][str(i)]['names'][j].lower() == perk:
                                perk = mapeo['perks'][str(i)]['id']
                                encontrado = True
                                break
                        if encontrado:
                            break
                if encontrado == False:
                    return {"message": "No se ha encontrado el perk"}
                with open("dbd/perks.json", "r") as file:
                    perks = json.load(file)
                    perk = perks[perk]
                    return perk