import pytest

from routers.entities_helper import (
    select_text_given_entity,
    extract_text_body,
    extract_entities_w_spacy,
)


# Test cases for select_text_given_entity
def test_select_text_given_entity_invalid_entity_type():
    with pytest.raises(AssertionError):
        select_text_given_entity(1)
    with pytest.raises(AssertionError):
        select_text_given_entity(["abc"])


def test_select_text_given_entity_empty_entity():
    with pytest.raises(AssertionError):
        select_text_given_entity("")


# Test cases for extract_text_body
def test_extract_text_body_invalid_url_type():
    with pytest.raises(AssertionError):
        extract_text_body(1)
    with pytest.raises(AssertionError):
        extract_text_body(["abc"])


def test_extract_text_body_empty_url():
    with pytest.raises(AssertionError):
        extract_text_body("")


# Test cases for extract_entities_w_spacy
def test_extract_entities_w_spacy_invalid_text_type():
    with pytest.raises(AssertionError):
        extract_entities_w_spacy(1)
    with pytest.raises(AssertionError):
        extract_entities_w_spacy(["abc"])


def test_extract_entities_w_spacy_empty_text():
    with pytest.raises(AssertionError):
        extract_entities_w_spacy("")

