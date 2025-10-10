## Development Practices

- Start with minimal, lean implementations focused on proof-of-concept
- Prefer extending existing patterns over implementing from scratch
- Use defensive programming for data validation and external API calls
- Include structured logging with appropriate levels (debug, info, warn, error)
- Create focused, single-purpose functions and classes
- Use type hints and docstrings for public interfaces
- Write tests for data transformations and business logic
- Follow existing code patterns and architectural decisions
- Use `uv` for Python package management
- Prefer SQLMesh SQL models for data transformations over custom Python scripts

## Python & Data Engineering

- Use pandas for data manipulation when appropriate
- Follow PEP 8 style guidelines
- Use dataclasses or Pydantic models for structured data
- Implement proper error handling for database connections and API calls
- Use environment variables for configuration
- Validate data schemas at boundaries (API inputs/outputs, file imports)
- Write integration tests for database queries and external service calls

## Git Operations

- Use `git restore <filename>` to discard working directory changes
- Use `git reset --soft HEAD~1` to undo last commit while keeping changes staged
- Always create feature branches from `main` branch
- Write descriptive commit messages following conventional commits format
- Run tests and linting before committing changes

## External Resources & APIs

- Validate external API responses and handle rate limiting
- Use environment variables for API keys and sensitive configuration
- Implement retry logic with exponential backoff for external calls
- Cache external API responses when appropriate
- Document API dependencies and required permissions

## Communication & Documentation

- Use clear, technical language appropriate for data engineering context
- Include code examples in explanations when helpful
- Reference specific file paths and line numbers when discussing code
- Ask for clarification on data requirements and business logic
- Document data models, transformations, and API interfaces
- Use markdown formatting for structured responses

# Copilot Coding Agent Onboarding Instructions for OSO Repository

## Repository Overview

Open Source Observer (OSO) is a data engineering platform for integrating, replicating, and analyzing open source ecosystem data. The repository contains code and configuration for ingesting data from databases, GraphQL APIs, REST APIs, and files, orchestrated via Dagster pipelines. The main goals are to enable scalable data ingestion, transformation, and validation, with assets loaded into BigQuery for downstream analysis.

## Key Data Integration Patterns
- **Database Replication**: Replicate external databases into OSO datasets. See `warehouse/oso_dagster/assets/` and [database replication docs](https://docs.opensource.observer/docs/contribute-data/database).
- **GraphQL API Crawling**: Use Dagster assets to crawl and ingest data from GraphQL APIs. See [GraphQL API docs](https://docs.opensource.observer/docs/contribute-data/graphql-api).
- **REST API Crawling**: Use Dagster assets to crawl and ingest data from REST APIs. See [REST API docs](https://docs.opensource.observer/docs/contribute-data/rest-api).

## Writing Custom Dagster Assets
- **Location**: Place new assets in `warehouse/oso_dagster/assets/default/`.
- **Asset Types**: Use vanilla Dagster assets for unique sources, or asset factories for common patterns (see `warehouse/oso_dagster/factories/`).
- **Patterns**:
	- For BigQuery, use either the BigQuery resource (SQL orchestration) or BigQuery I/O Manager (DataFrame computation).
	- For GCS file ingestion, use asset factories (see `warehouse/oso_dagster/factories/gcs.py`).
	- For cacheable assets, use the `@cacheable_asset_factory` decorator and hydrate with Pydantic models.
- **Best Practices**:
	- Start with a simple asset and validate in production before abstracting into a factory.
	- Use structured logging and defensive programming for API/database calls.
	- Validate schemas at boundaries and write tests for business logic.
	- Reference [contribute-data/dagster docs](https://docs.opensource.observer/docs/contribute-data/dagster) for examples and advanced patterns.

## Build, Test, and Validation Instructions

### Environment Setup
- Always run `uv pip install -r requirements.txt` in Python subprojects before building or testing.
- For Node.js subprojects, always run `pnpm install` before building or testing.
- For Dagster, ensure Python 3.10+ and install dependencies in `warehouse/oso_dagster/`.

### Bootstrap & Build
- Python: `uv pip install -r requirements.txt` (in each Python subproject)
- Node.js: `pnpm install` (in each JS/TS subproject)
- Dagster: `uv pip install -r warehouse/oso_dagster/requirements.txt`

### Lint
- Python: `uv pip install ruff` then `ruff check .`
- Node.js: `pnpm lint` (where available)

### Test
- Python: `pytest` (in relevant subproject)
- Node.js: `pnpm test` or `pnpm vitest` (frontend)
- Dagster: `pytest warehouse/oso_dagster/`
- SQLMesh: `sqlmesh plan` and `sqlmesh apply` (for SQL models)

### Run
- Dagster: `dagster dev -f warehouse/oso_dagster/` (local dev server)
- Frontend: `pnpm dev` (in frontend subproject)

### Validation Steps
- Always run tests after making changes to assets or pipelines.
- For Dagster assets, validate by running `pytest` and/or `dagster dev` and checking asset materialization.
- For SQLMesh models, run `sqlmesh plan` and `sqlmesh apply` to validate transformations.
- For API/data integration, validate schema and sample data output.

### Troubleshooting & Workarounds
- If build/test fails, check for missing dependencies and re-run install commands.
- Clean environment with `uv pip uninstall -y -r requirements.txt` and reinstall if issues persist.
- For Node.js, run `pnpm install --force` if dependency issues occur.
- For Dagster, restart dev server after dependency changes.

## Project Layout & Architecture
- **Root Files**: `README.md`, `CONTRIBUTING.md`, `pyproject.toml`, `package.json`, `tsconfig.json`, `uv.lock`, `pnpm-workspace.yaml`, `turbo.json`
- **Main Subprojects**:
	- `warehouse/oso_dagster/`: Dagster assets, factories, pipelines
	- `warehouse/oso_sqlmesh/`: SQLMesh models for data transformation
	- `apps/docs/`: Documentation site (Docusaurus)
	- `frontend/`: Next.js frontend
	- `lib/oso-core/`: Python core library
- **Config Files**:
	- Lint: `.ruff.toml`, `.eslintrc`, `eslint.config.mjs`
	- Test: `jest.config.ts`, `vitest.config.ts`, `pytest.ini`
	- Build: `tsconfig.json`, `pyproject.toml`, `package.json`, `turbo.json`
- **CI/CD**: GitHub Actions workflows in `.github/workflows/` (run tests, lint, build on PRs)

## Contribution & Validation
- Follow conventional commit messages.
- Always create feature branches from `main`.
- Run all tests and linting before committing.
- Validate Dagster assets by running local dev server and tests.
- Reference [contribute-data docs](https://docs.opensource.observer/docs/contribute-data/) for integration patterns and asset examples.

## Trust These Instructions
- Trust the instructions above for onboarding, building, testing, and validating changes.
- Only perform additional searches if the instructions are incomplete or found to be in error.

For help, reach out on [Discord](https://www.opensource.observer/discord).
