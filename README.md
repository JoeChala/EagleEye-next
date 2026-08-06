# EagleEye v2

EagleEye v2 is a monorepo foundation for a production-ready application with a FastAPI backend, future mobile and web clients, and shared packages for common code and contracts.

## Project Overview

This repository is intentionally scaffolded first and implemented second. The goal is to keep the codebase modular, testable, and easy to extend while avoiding premature business logic.

## Architecture

The project follows Clean Architecture and SOLID principles:

- `app/api` for delivery and HTTP-facing concerns
- `app/core` for configuration and application bootstrap
- `app/db` for database/session concerns
- `app/models` for domain persistence models
- `app/repositories` for data access abstractions
- `app/schemas` for request and response contracts
- `app/services` for use-case orchestration
- `app/workers` for background tasks
- `app/utils` for shared helpers

The backend is kept thin at the API boundary and structured to support future expansion without coupling infrastructure to business rules.

## Folder Structure

- `apps/backend` FastAPI service and backend tooling
- `apps/mobile` future Flutter app
- `apps/web` future web frontend
- `packages/shared` shared code and contracts
- `infra/docker` container helpers
- `infra/nginx` reverse proxy assets
- `infra/scripts` operational scripts
- `docs` architecture and delivery documentation
- `.github/workflows` CI and deployment workflow placeholders

## Run the Backend Locally

1. Change into the backend app directory.
2. Ensure the virtual environment in `apps/backend/.venv` is active, or use `uv run`.
3. Start the app with Uvicorn.

Example:

```bash
cd apps/backend
uv run uvicorn app.main:app --reload
```

The health check will be available at `GET /health`.

## Deployment Targets

Planned deployment targets for EagleEye v2 are:

- Railway for backend hosting and managed services
- Vercel for web frontend deployment

Those delivery pipelines will be added after the foundation and module boundaries are in place.

