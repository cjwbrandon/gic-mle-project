from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
import re
import time
import spacy
import en_core_web_sm
import pandas as pd

from utils.db_utils import engine

# Get distinct entities extracted
def select_distinct_entities(engine=engine):
    """Pull all distinct entities extracted
    
    Parameters
    ----------
    engine : SQLAlchemy.engine
        engine
    
    Returns
    -------
    list
        List of all the distinct entity.
    """
    # Execute SQL query for all distinct entities
    with engine.connect() as conn:
        entities = conn.execute("SELECT DISTINCT(entity) entities FROM nlp.entities")
    entities = entities.fetchall()
    return [ent[0] for ent in entities]


def select_text_given_entity(entity, engine=engine):
    """Retrieve all texts assocaited with an entity.
    
    Parameters
    ----------
    entity : str
        entity to filter by
    engine : SQLAlchemy.engine
        engine
        
    Returns
    -------
    list
        List of text associated with the entity
        
    Raises
    ------
    AssertionException
        Input entity must be of type string
    AssertionException
        Input entity cannot be empty
    """
    assert type(entity) == str, "Input entity must be of type string."
    assert entity != "", "Input entity cannot be empty."

    # Convert search entry to upper since all entities are in upper case
    entity = entity.upper()

    # Execute SQL query for text filtered by input entity
    with engine.connect() as conn:
        text = conn.execute(f"SELECT text FROM nlp.entities WHERE entity = '{entity}'")
    text = text.fetchall()
    if text == []:
        raise HTTPException(status_code=404, detail="Entity not found.")

    return [t[0] for t in text]


# Scrape data from URL
def extract_text_body(url, retries=3):
    """Extract text body of a url
    
    Parameters
    ----------
    url : string
        URL to extract from
        
    Returns
    -------
    string
        Text body of the url

    Raises
    ------
    AssertionException
        Input URL must be of type string
    AssertionException
        Input URL cannot be empty
    """
    assert type(url) == str, "Input URL must be of type string."
    assert url != "", "Input URL cannot be empty."

    for i in range(retries):
        try:
            # Invoke GET request from url
            page = requests.get(url)
            page.raise_for_status()  # raise exceptions for http errors
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=404, detail="Unable to connect to the URL.")
        except Exception as e:
            if i < retries:
                print(f"Try ({i}) failed. Retrying in 1s...")
                time.sleep(1)
                continue
            else:
                raise HTTPException(
                    status_code=404, detail="Unable to connect to the URL."
                )

    # Initialise BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract out unwanted tags
    for script in soup(["script", "style", "aside"]):
        script.extract()

    return " ".join(re.split(r"[\n\t\s]+", soup.get_text()))


# Extract entities from text
def extract_entities_w_spacy(text):
    """Extract entities from input text using Spacy.
    
    Parameters
    ----------
    text : string
        text to extract from.
        
    Returns
    -------
    pandas.DataFrame
        Table of the texts and their entities.
        
    Raises
    ------
    AssertionException
        Input text must be of type string
    AssertionException
        Input text cannot be empty
    """
    assert type(text) == str, "Input text must be of type string."
    assert text != "", "Input text cannot be empty."

    nlp = en_core_web_sm.load()
    doc = nlp(text)
    entities = pd.DataFrame(
        [(X.text, X.label_) for X in doc.ents], columns=["text", "entity"]
    )
    return entities.drop_duplicates(["entity", "text"], keep="first")


# Load entities to database
def insert_entities_to_database(entities, engine=engine, retries=3):
    """Insert entities data to database
    
    Parameters
    ----------
    entities : pandas.DataFrame
        Table of entities and text
    engine : SQLAlchemy.engine
        engine
    """

    # Attempt to insert data to main table, on conflict, do nothing
    upsert_sql = """
INSERT INTO nlp.entities ("entity", "text")
SELECT "entity", "text"
FROM nlp.entities_temp
ON CONFLICT ("entity", "text")
DO NOTHING;
    """

    for i in range(retries):
        try:
            # Push table to a temporary table
            entities.to_sql(
                "entities_temp", engine, schema="nlp", if_exists="replace", index=False
            )

            # Execute upsert sql statement and remove temporary table after.
            conn = engine.connect()
            conn.execute(upsert_sql)
            conn.execute("DROP TABLE nlp.entities_temp")
        except Exception as e:
            if i < retries:
                print(f"Try ({i}) failed. Retrying in 1s...")
                time.sleep(1)
                continue
            else:
                raise HTTPException(
                    status_code=503, detail="Database service is unavailable."
                )
        finally:
            conn.close()

