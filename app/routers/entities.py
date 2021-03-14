from fastapi import APIRouter
from pydantic import BaseModel

from routers.entities_helper import (
    select_distinct_entities,
    extract_text_body,
    extract_entities_w_spacy,
    insert_entities_to_database,
)


class URL(BaseModel):
    url: str


router = APIRouter(prefix="/entities")


@router.get("/")
def get_entities():
    return {"entities": select_distinct_entities()}


@router.post("/extract/")
async def extract_entities(url: URL):
    # Attempt scraping of text body from url
    contents = extract_text_body(url.url)

    # Extract entities from text body
    entities = extract_entities_w_spacy(contents)

    # Insert data to database table
    insert_entities_to_database(entities)

    return {"message": f"The entities were successfully extracted from '{url.url}'."}
