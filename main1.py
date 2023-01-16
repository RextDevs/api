from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import json, os

app = FastAPI()
#http://127.0.0.1:8000/docs
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

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    with open("index.html", "r") as file:
        return file.read()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/pokemonapi/pokemon/{pokemon}")
async def get_pokemon(pokemon: str):
    #detectar si el valor es un numero
    if pokemon.isnumeric():
        with open(f"json/{pokemon}.json", "r") as file:
            pokemon = json.load(file)
            return pokemon
    else:
        with open("datos/pokemons.json", "r") as file:
            pokemons = json.load(file)
            pokemon = pokemons[pokemon]
            with open(pokemon["url"], "r") as file:
                pokemon = json.load(file)
                return pokemon

@app.post("/libro")
async def get_libro(libro: libro):
    return {"message": f"El libro {libro.titulo} insertado correctamente"}