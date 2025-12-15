# Base Clean Architecture FastAPI-based API

This is a base project for FastAPI-based APIs implementing clean architecture
patterns for maintainable and testable code.

Feel free to use it as a starting point for your own projects.

## 🏗️ Architecture

This project follows the **Clean Architecture** pattern, with the following
layers:

- **Domain Layer**: Core business logic and entities.
- **Application Layer**: Use cases and application services.
- **Infrastructure Layer**: External dependencies and integrations.

The project is structured around **modules** (vertical slices), with each
module having its own directory containing all the necessary layers.

It also implements other patterns and practices, such as:

- **Builder Pattern** for entity creation.
- **Dependency Injection** (via Lagom).
- **Data Transfer Objects** (DTOs) for request and response payloads.
- **Value Objects** for data validation.
- **Result Pattern** for handling operation outcomes.
- **Repository Pattern** for data access.
- **Collections** for enhanced filtering and sorting.
- **Instrumentation** for logging and monitoring use cases.
- **OData V4 Query** for filtering and sorting data.
- **Correlation ID** for request tracing.

## 🚀 Technology Stack

These are some of the main technologies used in this project:

- **FastAPI** - Web framework for building APIs.
- **SQLAdmin** - Admin interface for database management.
- **SQLActive** - ActiveRecord pattern for database operations.
- **SQLite** - Database (via aiosqlite for async operations).
- **Lagom** - Dependency injection container.
- **Pydantic** - Data validation and settings management.
- **Orjson** - Fast JSON serialization.
- **Uvloop** - High-performance event loop.
- **Structlog** - Structured logging.
- **Validators** - Data validation.
- **OData V4 Query** - OData query parsing.
- **ASGI Correlation ID** - Requests correlation with unique IDs.
- **Ruff** - Linter and code formatter.
- **Pytest** - Testing framework.

## 📁 Project Structure

```
.
├── src/                        # Source code
│   ├── api/                    # API-related code
│   │   ├── middlewares/        # Application middlewares
│   │   │   └── access_log_middleware.py # Access logging middleware
│   │   ├── config.py           # Application configuration
│   │   └── health.py           # Health check logic
│   ├── modules/                # Feature modules (domain-driven)
│   │   └── resources/          # Resources feature module
│   │       ├── application/    # Application layer (use cases)
│   │       │   └── use_cases/  # Use case implementations
│   │       │       ├── create_resource.py
│   │       │       ├── delete_resource.py
│   │       │       ├── get_resource.py
│   │       │       ├── list_resources.py
│   │       │       └── update_resource.py
│   │       ├── domain/         # Domain layer
│   │       │   ├── entities.py         # Domain entities
│   │       │   ├── error_codes.py      # Domain-specific error codes
│   │       │   ├── exceptions.py       # Domain-specific exceptions
│   │       │   ├── value_objects.py    # Value objects
│   │       │   ├── collections.py      # Domain collections
│   │       │   └── interfaces/         # Repository interfaces
│   │       │       └── repositories.py
│   │       ├── infrastructure/ # Infrastructure layer
│   │       │   ├── instrumentation/ # Use case instrumentation/decorators
│   │       │   │   └── use_cases/
│   │       │   │       ├── create_resource.py
│   │       │   │       ├── delete_resource.py
│   │       │   │       ├── get_resource.py
│   │       │   │       ├── list_resources.py
│   │       │   │       └── update_resource.py
│   │       │   └── persistence/ # Persistence implementations
│   │       │       ├── admin.py        # SQLAdmin view for resources
│   │       │       ├── models/         # Database models
│   │       │       │   ├── mock.py     # Mock models for testing
│   │       │       │   └── sqlite.py   # SQLite database models
│   │       │       └── repositories/   # Repository implementations
│   │       │           ├── mock.py     # Mock repository for testing
│   │       │           └── sqlite.py   # SQLite repository implementation
│   │       ├── presentation/   # Presentation layer (API)
│   │       │   ├── api.py      # Resource API endpoints
│   │       │   └── dtos.py     # Data transfer objects
│   │       └── di.py           # Dependency injection configuration
│   ├── shared/                 # Shared utilities and common code
│   │   ├── application/        # Shared application layer
│   │   │   └── interfaces/     # Shared interfaces
│   │   │       ├── base.py     # Base interfaces
│   │   │       └── instrumentation.py # Instrumentation interfaces
│   │   ├── domain/             # Shared domain layer
│   │   │   ├── bases/          # Base classes
│   │   │   │   ├── entity.py   # Entity base class
│   │   │   │   └── value_object.py # Value object base class
│   │   │   ├── error_codes.py  # Shared error codes
│   │   │   └── exceptions.py   # Shared exception classes
│   │   ├── helpers/            # Shared helper functions
│   │   │   └── odata_helper.py # OData query helper
│   │   ├── infrastructure/     # Shared infrastructure
│   │   │   └── db.py           # Database connection utilities
│   │   ├── presentation/       # Shared presentation layer
│   │   │   ├── api.py          # Shared API routes (e.g., health check)
│   │   │   ├── dtos.py         # Base DTO classes
│   │   │   └── responses.py    # Response utilities
│   │   └── utils/              # Shared utility functions
│   │       └── uuid_tools.py   # UUID utility functions
│   ├── logger.py               # Logging configuration
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Tests directory
│   ├── conftest.py             # Pytest global fixtures
│   ├── resources/              # Resource module tests
│   │   ├── application/        # Application layer tests
│   │   │   ├── test_create_resource.py
│   │   │   ├── test_delete_resource.py
│   │   │   ├── test_get_resource.py
│   │   │   ├── test_list_resources.py
│   │   │   └── test_update_resource.py
│   │   ├── domain/             # Domain layer tests
│   │   │   ├── conftest.py
│   │   │   └── test_collections.py
│   │   ├── infrastructure/     # Infrastructure layer tests
│   │   │   └── persistence/    # Persistence layer tests
│   │   │       └── repositories/ # Repository tests
│   │   │           └── test_sqlite_resource_repository.py
│   │   └── presentation/       # Presentation layer tests
│   │       ├── test_create_resource.py
│   │       ├── test_delete_resource.py
│   │       ├── test_get_resource.py
│   │       ├── test_list_resources.py
│   │       └── test_update_resource.py
│   └── shared/                 # Shared tests
│       └── presentation/       # Shared presentation tests
│           └── api/            # API tests
│               └── test_health.py # Health endpoint tests
├── .env.example                # Environment variables template
├── api.http                    # Some HTTP requests for testing
├── COMMITS.md                  # Git commit guidelines
├── LICENSE.md                  # Project license
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # Project documentation
├── ruff.toml                   # Ruff linter configuration
└── uv.lock                     # UV dependency lock file
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- uv

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```

### Running the Application

Run the application with:
```bash
uv run main.py
```

The API will be available at `http://$DOMAIN_NAME:$PORT/`.

Replace `$DOMAIN_NAME` and `$PORT` with the domain name or IP address of the
server and the port number you configured in the `.env` file respectively
(see the configuration section below).

## 🔧 Configuration

Copy the `.env.example` file to `.env` and update the settings as needed.

```bash
cp .env.example .env
```

Example `.env` file:

```dotenv
ENV=dev
PORT=8000
DEBUG=True
DATABASE_URL=sqlite+aiosqlite:///./test.db
MAX_RECORDS_PER_PAGE=100
LOGS_PATH=./.logs/app.log
```

### Database

- **Development**: SQLite database.
- **Connection**: Configured via `DATABASE_URL` setting.
- **Migrations**: Automatic table creation on startup.

## 📚 API Documentation

- **Swagger UI**: `http://$DOMAIN_NAME:$PORT/docs`
- **ReDoc**: `http://$DOMAIN_NAME:$PORT/redoc`

Replace `$PORT` with the port number you configured in the `.env` file.

## ⚙️ Admin Interface

- **Admin**: `http://$DOMAIN_NAME:$PORT/admin`

## 🧪 Testing & Linting

Run tests with pytest:
```bash
uv run -m pytest
```

Run linting with ruff:
```bash
uv run -m ruff check .
```

## 📋 Available Endpoints

### Health Check
- `GET /health` - Application health status.
- `GET /ping` - Same as `/health`.

### Resources
- Resource endpoints are available under the `/resources` prefix.

## 🏛️ Clean Architecture Benefits

This project structure provides:

- **Testability**: Easy to unit test business logic.
- **Maintainability**: Clear separation of concerns.
- **Flexibility**: Easy to swap implementations (e.g., database providers).
- **Independence**: Domain logic independent of frameworks.

## 🤝 Contributing

1. Check the [commits guidelines](COMMITS.md).
2. Follow the existing architecture patterns.
3. Add tests for new functionality using `pytest`.
4. Use type hints throughout.
5. Run linting with `ruff` before committing.

## 📄 License

This project is licensed under the [MIT License](LICENSE.md).
