from fastapi import APIRouter
from pydantic import BaseModel

from router.entities_helper import (
    extract_text_body,
    extract_entities_w_spacy,
    insert_entities_to_database,
)


class URL(BaseModel):
    url: str


router = APIRouter()


@router.post("/entities/extract/")
async def extract_entities(url: URL):
    url = url.dict().url

    # Attempt scraping of text body from url
    contents = extract_text_body(url.url)

    # Extract entities from text body
    entities = extract_entities_w_spacy(contents)

    # Insert data to database table
    insert_entities_to_database(entities)

    return {"message": f"The entities were successfully extracted from '{url.url}'."}
