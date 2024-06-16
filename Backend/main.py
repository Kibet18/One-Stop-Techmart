
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/products')
def get_products():
    return [{"name":"Inferno"}]