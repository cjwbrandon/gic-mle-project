# gic-mle-project

# Deploy
[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
- Note: Incomplete -> My database is currently running as a separate docker container.

# Setup
- Docker - https://docs.docker.com/engine/install/
- Docker Compose for dev - https://docs.docker.com/compose/install/

# Usage
- Dev
  - Run `docker-compose up --build`
- Test
  - Run `docker build --file Dockerfile.test -t nlp_app_test .`
  - Run `docker run nlp_app_test`

# OpenAPI Documentation
For this project, I've used FastAPI built-in OpenAPI specification support. You can visit the OpenAPI specification at the path `/docs`.

# Folder Structure
- `/app` - Store application-related code.
  - `/routers` - Store all routers in the API.
    - `/tests/` - All routers test cases done using PyTest.
  - `/scripts` - Store all shell script mainly used to set up app requirements
  - `/utils` - Store all utilities
  - `main.py` - FastAPI Application
- `/configs` - Store configurations
- `/dependencies` - Store dependencies files
- `/postgres_init` - Files to initialise database (DDL scripts)
- `/scripts` - Store all shell script mainly used to set up environment
- `docker-compose.yml` - Set up docker containers for development environment
- `Dockerfile` - Docker file for FastAPI application
- `Dockerfile.test` - Docker file to run PyTest test cases for the application.