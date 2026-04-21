import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rest_api.logging_config import configure_logging
from rest_api.routers.field_definition_routes import router as field_definition_router
from rest_api.routers.form_routes import router as form_router
from rest_api.routers.response_routes import router as response_router
from rest_api.container import Container


def create_app() -> FastAPI:
    di_container = Container()
    di_container.wire(
        modules=[
            "rest_api.routers.field_definition_routes",
            "rest_api.routers.form_routes",
            "rest_api.routers.response_routes",
        ]
    )

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        configure_logging(di_container.settings().LOG_FILE)
        await di_container.db().connect()
        yield
        await di_container.db().disconnect()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(field_definition_router)
    app.include_router(form_router)
    app.include_router(response_router)

    @app.get("/")
    async def root():
        return {"message": "Welcome to Typeforms API!!!"}

    return app


def main() -> None:
    uvicorn.run(
        "rest_api:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True
    )
