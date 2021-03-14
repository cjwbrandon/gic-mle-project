import requests
from bs4 import BeautifulSoup
import re
import time
import spacy
import en_core_web_sm
import pandas as pd


# Extract
#########
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
    """

    for i in range(retries):
        try:
            # Invoke GET request from url
            page = requests.get(url)
            page.raise_for_status()  # raise exceptions for http errors
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except Exception as e:
            if i < retries:
                print(f"Try ({i}) failed. Retrying in 5s...")
                time.sleep(5)
                continue

    # Initialise BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract out unwanted tags
    for script in soup(["script", "style", "aside"]):
        script.extract()

    return " ".join(re.split(r"[\n\t\s]+", soup.get_text()))


# Transform
###########
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
    return pd.DataFrame(
        [(X.text, X.label_) for X in doc.ents], columns=["text", "entity"]
    )
