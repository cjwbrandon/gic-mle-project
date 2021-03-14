from fastapi import APIRouter
from pydantic import BaseModel

from router.entities_helper import extract_text_body, extract_entities_w_spacy


class URL(BaseModel):
    url: str


router = APIRouter()


@router.post("/entities/extract/")
async def extract_entities(url: URL):
    url = url.dict().url
    contents = extract_text_body(url.url)
    entities = extract_entities_w_spacy(contents)

    # TODO: Push entities to database
    return {"message": f"The entities were successfully extracted from '{url.url}'."}
