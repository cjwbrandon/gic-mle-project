CREATE SCHEMA nlp

CREATE TABLE entities (
    "entity" text NOT NULL,
    "text" text NOT NULL,
    PRIMARY KEY ("entity", "text")
)
