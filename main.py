from fastapi import FastAPI
from lib import pseudo_random
from typing import List, Union

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
randomizer = pseudo_random.Stock()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items")
async def init_products(items: List[pseudo_random.Product]):
    randomizer.products = items

@app.get("/respawn")
async def back_to_defaults():
    global randomizer
    randomizer = pseudo_random.Stock()

@app.post("/settings")
async def set_settings(settings: pseudo_random.Settings):
    randomizer.calls_limit = settings.calls_limit
    randomizer.rare_per_limit = settings.rare_per_limit


@app.get("/spin")
async def spin() -> Union[pseudo_random.Response, dict]:
    try:
        product = randomizer.get_product()
    except Exception:
        return {}
    return {"position": product.name}
