
from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
from models.brand import Brand
from models.user import User
from models.order import Order
from models.product import Product
from database import create_tables

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Initialize the database tables
create_tables()

# Brand Endpoints
@app.post("/brands/", response_model=dict)
def create_brand_endpoint(brand: Brand):
    return brand.save().to_dict()

@app.get("/brands/", response_model=List[dict])
def get_brands_endpoint():
    return Brand.find_all()

@app.put("/brands/{id}", response_model=dict)
def update_brand_endpoint(id: int, brand: Brand):
    updated_brand = Brand.find_one(id)
    if updated_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated_brand.update(brand).to_dict()

@app.delete("/brands/{id}", response_model=dict)
def delete_brand_endpoint(id: int):
    brand = Brand.find_one(id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand.delete().to_dict()

# User Endpoints
@app.post("/users/", response_model=dict)
def create_user_endpoint(user: User):
    return user.save().to_dict()

@app.get("/users/", response_model=List[dict])
def get_users_endpoint():
    return User.find_all()

@app.put("/users/{id}", response_model=dict)
def update_user_endpoint(id: int, user: User):
    updated_user = User.find_one(id)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user.update(user).to_dict()

@app.delete("/users/{id}", response_model=dict)
def delete_user_endpoint(id: int):
    user = User.find_one(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.delete().to_dict()

# Order Endpoints
@app.post("/orders/", response_model=dict)
def create_order_endpoint(order: Order):
    return order.save().to_dict()

@app.get("/orders/", response_model=List[dict])
def get_orders_endpoint():
    return Order.find_all()

@app.put("/orders/{id}", response_model=dict)
def update_order_endpoint(id: int, order: Order):
    updated_order = Order.find_one(id)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order.update(order).to_dict()

@app.delete("/orders/{id}", response_model=dict)
def delete_order_endpoint(id: int):
    order = Order.find_one(id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.delete().to_dict()

# Product Endpoints
@app.post("/products/", response_model=dict)
def create_product_endpoint(name: str, description: str, cost: int, image: UploadFile = File(...)):
    product = Product(name=name, description=description, cost=cost, image=image.file.read())
    return product.save().to_dict()

@app.get("/products/", response_model=List[dict])
def get_products_endpoint():
    return Product.find_all()

@app.put("/products/{id}", response_model=dict)
def update_product_endpoint(id: int, name: str, description: str, cost: int, image: UploadFile = File(...)):
    updated_product = Product.find_one(id)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product.name = name
    updated_product.description = description
    updated_product.cost = cost
    updated_product.image = image.file.read()
    return updated_product.update().to_dict()

@app.delete("/products/{id}", response_model=dict)
def delete_product_endpoint(id: int):
    product = Product.find_one(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.delete().to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8828)