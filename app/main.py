from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from routers import entities

app = FastAPI()

app.include_router(entities.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
