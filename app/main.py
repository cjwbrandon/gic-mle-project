from fastapi import FastAPI
from pydantic import BaseModel


from routers import entities

app = FastAPI()

app.include_router(entities.router)


class Message(BaseModel):
    message: str


@app.get(
    "/health",
    response_model=Message,
    responses={
        200: {
            "description": "Successful.",
            "content": {"application/json": {"example": {"message": "Available."}}},
        }
    },
)
def health_check():
    return {"message": "Available"}
