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

from fastapi.encoders import jsonable_encoder

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
def get_user(id: int):
    try:
        with get_database() as db:
            result = db.query(User).filter(User.id == id).first()
            json_result = jsonable_encoder(result)
        return JSONResponse({"Response": json_result})

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}, {id}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


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


@app.delete("/users/{id}")
def delete_producto(id: int):
    try:
        with get_database() as db:
            result = db.query(User).filter(User.id == id)
            if result is None:
                raise HTTPException(status_code=500, detail=f"User doesnt exist {id}")
            else:
                result.delete(synchronize_session=False)
                db.commit()
                return JSONResponse({"Response": f"user deleted {id}"})

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}, {id}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.put("/users")
def put_user(user: UserDTO, id: int):
    try:
        with get_database() as db:
            result = db.query(User).filter(User.id == id)

            if result is None:
                raise HTTPException(status_code=500, detail=f"User doesnt exist {id}")
            else:
                result.update(user.dict(), synchronize_session=False)
                db.commit()
            return result.first()

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {str(e)}, {id}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

