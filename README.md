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
- **Uvloop** - High-performance event loop.
- **Structlog** - Structured logging.
- **OData V4 Query** - OData query parsing.
- **ASGI Correlation ID** - Requests correlation with unique IDs.
- **Ruff** - Linter and code formatter.
- **Pytest** - Testing framework.

## 📁 Project Structure

```
.
├── src/                        # Source code
│   ├── core/                   # Core application logic
│   │   ├── middlewares/        # Application middlewares
│   │   │   ├── access_log_middleware.py
│   │   │   ├── rate_limit_middleware.py
│   │   │   └── security_headers_middleware.py
│   │   ├── app.py                  # FastAPI app factory and setup
│   │   ├── config.py               # Application configuration
│   │   ├── exception_handlers.py   # Exception handlers for the app
│   │   ├── health.py               # Health check logic
│   │   └── logger.py               # Logging configuration
│   ├── modules/                # Feature modules (domain-driven)
│   │   └── <module_name>/      # Feature module (e.g., resources)
│   │       ├── application/    # Application layer (use cases)
│   │       │   └── use_cases/  # Use case implementations
│   │       │       ├── create_*.py
│   │       │       ├── delete_*.py
│   │       │       ├── get_*.py
│   │       │       ├── list_*.py
│   │       │       └── update_*.py
│   │       ├── domain/         # Domain layer
│   │       │   ├── interfaces/ # Domain interfaces (repositories, services)
│   │       │   ├── collections.py
│   │       │   ├── entities.py
│   │       │   ├── enums.py
│   │       │   ├── error_codes.py
│   │       │   ├── exceptions.py
│   │       │   └── value_objects.py
│   │       ├── infrastructure/ # Infrastructure layer
│   │       │   ├── instrumentation/
│   │       │   │   └── use_cases.py
│   │       │   └── persistence/ # Persistence implementations
│   │       │       ├── models/
│   │       │       │   ├── mock.py
│   │       │       │   └── sqlite.py
│   │       │       ├── repositories/
│   │       │       │   ├── mock.py
│   │       │       │   └── sqlite.py
│   │       │       └── admin.py
│   │       ├── presentation/   # Presentation layer (API)
│   │       │   ├── api.py
│   │       │   └── dtos.py
│   │       └── di.py           # Dependency injection configuration
│   ├── shared/                 # Shared utilities and common code
│   │   ├── application/
│   │   │   ├── interfaces/
│   │   │   │   └── command_handler.py
│   │   │   └── instrumentation.py
│   │   ├── domain/
│   │   │   ├── bases/
│   │   │   │   ├── collection.py
│   │   │   │   ├── entity.py
│   │   │   │   ├── error.py
│   │   │   │   └── value_object.py
│   │   │   ├── error_codes.py
│   │   │   └── exceptions.py
│   │   ├── helpers/
│   │   │   └── odata_helper.py
│   │   ├── infrastructure/
│   │   │   └── db.py
│   │   ├── presentation/
│   │   │   ├── api.py
│   │   │   ├── dtos.py
│   │   │   └── responses.py
│   │   ├── utils/
│   │   │   ├── rfc_9457.py
│   │   │   └── uuid_tools.py
│   │   └── di.py
│   └── main.py                 # Application entry point
├── tests/                      # Tests directory
│   ├── <module_name>/          # Module tests (e.g., resources)
│   │   ├── application/
│   │   │   ├── test_create_*.py
│   │   │   ├── test_delete_*.py
│   │   │   ├── test_get_*.py
│   │   │   ├── test_list_*.py
│   │   │   └── test_update_*.py
│   │   ├── domain/
│   │   │   ├── conftest.py
│   │   │   └── test_*.py
│   │   ├── infrastructure/
│   │   │   └── persistence/
│   │   │       └── repositories/
│   │   │           ├── conftest.py
│   │   │           └── test_*.py
│   │   └── presentation/
│   │       ├── conftest.py
│   │       ├── test_create_*.py
│   │       ├── test_delete_*.py
│   │       ├── test_get_*.py
│   │       ├── test_list_*.py
│   │       ├── test_partial_update_*.py
│   │       └── test_update_*.py
│   ├── shared/
│   │   └── presentation/
│   │       └── test_health.py
│   └── conftest.py             # Pytest global fixtures
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignored files
├── .python-version             # Python version for tooling
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

- Python 3.13+
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
