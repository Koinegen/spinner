from fastapi import FastAPI
from lib import pseudo_random
from typing import List, Union

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://tilda.cc",
    "https://tilda.cc",
    "https://vfomka.ru",
    "https://vfomka.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
randomizer = pseudo_random.Stock()
token = None


@app.post("/set_auth")
async def root(a_token: str):
    global token
    if token:
        return {"message": "already set"}
    else:
        token = a_token
        return {"message": "set"}

@app.post('/get_all')
async def get_current_dict(a_token: str):
    if a_token == token:
        return randomizer.products
    else:
        return {"message": "invalid token"}


@app.post("/items")
async def init_products(items: List[pseudo_random.Product], a_token: str):
    if a_token == token:
        randomizer.products = items
        return
    else:
        return {"message": "invalid token"}


@app.post("/respawn")
async def back_to_defaults(a_token: str):
    if a_token == token:
        global randomizer
        randomizer = pseudo_random.Stock()
        return
    else:
        return {"message": "invalid token"}


@app.post("/settings")
async def set_settings(settings: pseudo_random.Settings, a_token: str):
    if a_token == token:
        randomizer.calls_limit = settings.calls_limit
        randomizer.rare_per_limit = settings.rare_per_limit
        return
    else:
        return {"message": "invalid token"}


@app.get("/spin")
async def spin() -> Union[pseudo_random.Response, dict]:
    try:
        product = randomizer.get_product()
    except Exception:
        return {}
    return {"position": product.name}
