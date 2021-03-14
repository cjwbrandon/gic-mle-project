# gic-mle-project

# Setup
- Docker - https://docs.docker.com/engine/install/
- Docker Compose for dev - https://docs.docker.com/compose/install/

# Usage
- Dev
  - Run `docker-compose up --build`

# Folder Structure
- `/app` - Store application-related code.
  - `/routers` - Store all routers in the API.
  - `/scripts` - Store all shell script mainly used to set up app requirements
  - `/utils` - Store all utilities
  - `main.py` - FastAPI Application
- `/configs` - Store configurations
- `/dependencies` - Store dependencies files
- `/postgres_init` - Files to initialise database (DDL scripts)
- `/scripts` - Store all shell script mainly used to set up environment
- `docker-compose.yml` - Set up docker containers for development environment
- `Dockerfile` - Docker file for FastAPI application