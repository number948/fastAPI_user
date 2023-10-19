import logging

from alembic.config import Config
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import insert
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.dependencies import get_database
from app.models.user import User
from alembic.command import upgrade

from app.user_dto import UserDTO

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError


load_dotenv()

app = FastAPI()


def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", get_settings().assemble_db_connection())
        upgrade(alembic_cfg, "head")
    except Exception as e:
        logging.error(f"Error: {e}")


@app.on_event("startup")
async def startup_event():
    run_migrations()


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
def post_producto(user: UserDTO):
    try:
        with get_database() as db:
            insert_if_not_exist_email_stmt = insert(User).values(
                name=user.name,
                age=user.age,
                city=user.city
            ).on_conflict_do_nothing()

            db.execute(insert_if_not_exist_email_stmt)
            db.commit()
            logging.info(f"User name {user.name} saved")

        return JSONResponse({"Response": "Successful"})
    except IntegrityError as e:
        logging.exception(f"Error in save user: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error: The user {user.name} already exists")

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.delete("/users/{post_id}")
def delete_producto(post_id: int):
    # crear una especie de restriccion para que no puedan ingresar post_id que no existan
    for index, product in enumerate(users):
       if product["id"] == post_id:
            users.pop(index)
       return {"message": "Post eliminado"}
    raise HTTPException(status_code=400, detail="Índice fuera de rango")



# @app.put("/users/{post_id}")
# def put_product(post_id: int, new_value: UserDTO):
#     for index, product in enumerate(users):
#         if product["id"] == post_id:
#             users[index]["id"] = new_value.id
#             users[index]["name"] = new_value.name
#             users[index]["price"] = new_value.price
#             users[index]["stock"] = new_value.stock
#             return {"message": "Post actualizado"}
#     raise HTTPException(status_code=400, detail="Índice fuera de rango")
