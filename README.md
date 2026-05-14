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
- **Inversion of Control (IoC)** (via Dishka).
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
- **Dishka** - Inversion of Control (IoC) container.
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
│   ├── __init__.py
│   ├── app.py                  # FastAPI app factory and setup
│   ├── config.py               # Application configuration
│   ├── health.py               # Health check logic
│   ├── logger.py               # Logging configuration
│   ├── main.py                 # FastAPI application entry point
│   ├── middlewares/            # Application middlewares
│   │   ├── __init__.py
│   │   ├── access_log_middleware.py # Access logging middleware
│   │   └── rate_limit_middleware.py
│   ├── modules/                # Feature modules (domain-driven)
│   │   └── <module_name>/      # Feature module (e.g., resources)
│   │       ├── __init__.py
│   │       ├── application/    # Application layer (use cases)
│   │       │   ├── __init__.py
│   │       │   └── use_cases/  # Use case implementations
│   │       │       ├── __init__.py
│   │       │       ├── create_*.py
│   │       │       ├── delete_*.py
│   │       │       ├── get_*.py
│   │       │       ├── list_*.py
│   │       │       └── update_*.py
│   │       ├── di.py           # Dependency injection configuration
│   │       ├── domain/         # Domain layer
│   │       │   ├── __init__.py
│   │       │   ├── collections.py
│   │       │   ├── entities.py
│   │       │   ├── enums.py
│   │       │   ├── error_codes.py
│   │       │   ├── exceptions.py
│   │       │   ├── interfaces/
│   │       │   │   ├── __init__.py
│   │       │   │   └── repositories.py
│   │       │   └── value_objects.py
│   │       ├── infrastructure/ # Infrastructure layer
│   │       │   ├── __init__.py
│   │       │   ├── instrumentation/
│   │       │   │   ├── __init__.py
│   │       │   │   └── use_cases/
│   │       │   │       ├── __init__.py
│   │       │   │       ├── create_*.py
│   │       │   │       ├── delete_*.py
│   │       │   │       ├── get_*.py
│   │       │   │       ├── list_*.py
│   │       │   │       └── update_*.py
│   │       │   └── persistence/ # Persistence implementations
│   │       │       ├── __init__.py
│   │       │       ├── admin.py
│   │       │       ├── models/
│   │       │       │   ├── __init__.py
│   │       │       │   ├── mock.py
│   │       │       │   └── sqlite.py
│   │       │       └── repositories/
│   │       │           ├── __init__.py
│   │       │           ├── mock.py
│   │       │           └── sqlite.py
│   │       └── presentation/   # Presentation layer (API)
│   │           ├── __init__.py
│   │           ├── api.py
│   │           └── dtos.py
│   └── shared/                 # Shared utilities and common code
│       ├── __init__.py
│       ├── application/
│       │   ├── __init__.py
│       │   ├── command_handler.py
│       │   └── instrumentation.py
│       ├── di.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── bases/
│       │   │   ├── __init__.py
│       │   │   ├── entity.py
│       │   │   ├── error.py
│       │   │   └── value_object.py
│       │   ├── error_codes.py
│       │   └── exceptions.py
│       ├── helpers/
│       │   ├── __init__.py
│       │   └── odata_helper.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   └── db.py
│       ├── presentation/
│       │   ├── __init__.py
│       │   ├── api.py
│       │   ├── dtos.py
│       │   ├── exception_handlers.py
│       │   └── responses.py
│       └── utils/
│           ├── __init__.py
│           └── uuid_tools.py
├── tests/                      # Tests directory
│   ├── __init__.py
│   ├── conftest.py             # Pytest global fixtures
│   ├── <module_name>/          # Module tests (e.g., resources)
│   │   ├── application/
│   │   │   ├── __init__.py
│   │   │   ├── test_create_*.py
│   │   │   ├── test_delete_*.py
│   │   │   ├── test_get_*.py
│   │   │   ├── test_list_*.py
│   │   │   └── test_update_*.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   └── test_*.py
│   │   ├── infrastructure/
│   │   │   ├── __init__.py
│   │   │   └── persistence/
│   │   │       ├── __init__.py
│   │   │       └── repositories/
│   │   │           ├── __init__.py
│   │   │           ├── conftest.py
│   │   │           └── test_*.py
│   │   └── presentation/
│   │       ├── __init__.py
│   │       ├── test_create_*.py
│   │       ├── test_delete_*.py
│   │       ├── test_get_*.py
│   │       ├── test_list_*.py
│   │       └── test_update_*.py
│   └── shared/
│       ├── __init__.py
│       └── presentation/
│           ├── __init__.py
│           └── api/
│               ├── __init__.py
│               └── test_health.py
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignored files
├── .python-version             # Python version for tooling
├── COMMITS.md                  # Git commit guidelines
├── LICENSE.md                  # Project license
├── README.md                   # Project documentation
├── api.http                    # Some HTTP requests for testing
├── pyproject.toml              # Project configuration and dependencies
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
DATABASE_URL=sqlite+aiosqlite:///./.test.db
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
