import requests
from bs4 import BeautifulSoup
import re
import time


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
