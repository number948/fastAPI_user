from fastapi import FastAPI, HTTPException
from models.user import User
import asyncpg


DATABASE_URL = "postgresql://ash:probandoapis@127.0.0.1/users"


app = FastAPI()

users = [
    {
        "id": 1,
        "name": "victor",
        "age": 10,
        "city": "Santiago"
    },
    {
        "id": 2,
        "name": "Andrea",
        "age": 20,
        "city": "Londres"
    }

]


# print(len(products))

@app.get("/")
def message():
    return {"Hello": "World"}


@app.get("/users")
def get_products():
    return users


@app.get("/users/{id}")
def get_product_by_id(id: int):
    return list(filter(lambda item: item["id"] == id, users))


@app.get("/users/{stock}")
async def say_hello(stock: int):
    return list(filter(lambda item: item["stock"] == stock, users))


@app.post("/users")
def post_producto(user: User):
    users.append(user)
    return users


@app.delete("/users/{post_id}")
def delete_producto(post_id: int):
    # crear una especie de restriccion para que no puedan ingresar post_id que no existan
    for index, product in enumerate(users):
        if product["id"] == post_id:
            users.pop(index)
        return {"message": "Post eliminado"}
    raise HTTPException(status_code=400, detail="Índice fuera de rango")


@app.put("/users/{post_id}")
def put_product(post_id: int, new_value: User):
    for index, product in enumerate(users):
        if product["id"] == post_id:
            users[index]["id"] = new_value.id
            users[index]["name"] = new_value.name
            users[index]["price"] = new_value.price
            users[index]["stock"] = new_value.stock
            return {"message": "Post actualizado"}
    raise HTTPException(status_code=400, detail="Índice fuera de rango")
