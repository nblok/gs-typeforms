import uvicorn

from fastapi import FastAPI

from rest_api.routers.field_definition_routes import router as field_definition_router
from rest_api.container import Container


def create_app() -> FastAPI:
    di_container = Container()
    di_container.wire(modules=["rest_api.routers.field_definition_routes"])

    app = FastAPI()
    app.container = di_container
    app.include_router(field_definition_router)

    @app.get("/")
    async def root():
        return {"message": "Welcome to Typeforms API!"}

    return app


def main() -> None:
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
