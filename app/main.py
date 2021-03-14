from fastapi import FastAPI

from routers import entities

app = FastAPI()

app.include_router(entities.router)


@app.get("/health")
def health_check():
    return {"message": "Available"}
