from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from routers.entities_helper import (
    select_distinct_entities,
    select_text_given_entity,
    extract_text_body,
    extract_entities_w_spacy,
    insert_entities_to_database,
)


# Request Body Models
class URL(BaseModel):
    url: str

    class Config:
        schema_extra = {"example": {"url": "https://www.gic.com.sg/"}}


# Response Models
class Entities(BaseModel):
    entities: List[str]


class EntityText(BaseModel):
    entity: str
    texts: List[str]


class Message(BaseModel):
    message: str


class Detail(BaseModel):
    detail: str


router = APIRouter(prefix="/entities")


@router.get(
    "/",
    response_model=Entities,
    responses={
        200: {
            "description": "All unique entities extracted.",
            "content": {
                "application/json": {"example": {"entities": ["entity_1", "entity_2"]}}
            },
        }
    },
)
async def get_entities():
    return {"entities": select_distinct_entities()}


@router.get(
    "/{entity}",
    response_model=EntityText,
    responses={
        200: {
            "description": "A list of text with a provided entity.",
            "content": {
                "application/json": {
                    "example": {"entity": "entity_1", "texts": ["text_1", "text_2"]}
                }
            },
        },
        404: {
            "model": Detail,
            "description": "Entity not found.",
            "content": {
                "application/json": {"example": {"detail": "Entity not found."}}
            },
        },
    },
)
async def get_entity_texts(entity: str):
    return {"entity": entity, "texts": select_text_given_entity(entity)}


@router.post(
    "/extract/",
    response_model=Message,
    responses={
        200: {
            "description": "Successfully extracted.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "The entities were successfully extracted 'URL'."
                    }
                }
            },
        },
        404: {
            "model": Detail,
            "description": "Invalid URL or unable to connect to URL.",
            "content": {
                "application/json": {
                    "example": {"detail": "Unable to connect to the URL."}
                }
            },
        },
        503: {
            "model": Detail,
            "description": "Database unavailable.",
            "content": {
                "application/json": {
                    "example": {"detail": "Database service is unavailable."}
                }
            },
        },
    },
)
async def extract_entities(url: URL):
    # Attempt scraping of text body from url
    contents = extract_text_body(url.url)

    # Extract entities from text body
    entities = extract_entities_w_spacy(contents)

    # Insert data to database table
    insert_entities_to_database(entities)

    return {"message": f"The entities were successfully extracted from '{url.url}'."}
