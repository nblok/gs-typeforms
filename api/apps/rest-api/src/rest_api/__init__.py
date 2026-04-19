from fastapi import FastAPI
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def root():
        return {"message": "Hello World"}

    return app

def main() -> None:
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
