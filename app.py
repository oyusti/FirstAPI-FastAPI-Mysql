from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="FastAPI con MySQL",
    description="Mi primer API con FastAPI y MySQL",
    version="0.1",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones relacionadas con los usuarios"
        }
    ]
)

app.include_router(user)

