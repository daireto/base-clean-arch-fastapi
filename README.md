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

The project is structured around **features** (vertical slices), with each
feature having its own directory containing all the necessary layers.

It also implements other patterns and practices, such as:

- **Dependency Injection** (via Lagom).
- **Data Transfer Objects** (DTOs) for request and response payloads.
- **Value Objects** for data validation.
- **Result Pattern** for handling operation outcomes.

## 🚀 Technology Stack

These are some of the main technologies used in this project:

- **FastAPI** - Web framework for building APIs.
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
src/
├── core/                       # Core API configuration and utilities
│   ├── config.py               # Application configuration
│   ├── health.py               # Health check logic
│   ├── logger.py               # Logging configuration
│   ├── responses.py            # Response utilities
│   └── middlewares/            # Application middlewares
│       └── access_log.py       # Access logging middleware
├── features/                   # Feature modules (domain-driven)
│   └── resources/              # Resources feature module
│       ├── application/        # Application layer (use cases)
│       │   ├── use_cases/      # Use case implementations
│       │   │   ├── create_resource.py
│       │   │   ├── delete_resource.py
│       │   │   ├── get_resource.py
│       │   │   ├── list_resources.py
│       │   │   └── update_resource.py
│       │   └── instrumentation/  # Use case instrumentation/decorators
│       │       ├── create_resource.py
│       │       ├── delete_resource.py
│       │       ├── get_resource.py
│       │       ├── list_resources.py
│       │       └── update_resource.py
│       ├── domain/             # Domain layer
│       │   ├── entities.py     # Domain entities
│       │   ├── error_codes.py  # Domain error codes
│       │   ├── errors.py       # Domain-specific errors
│       │   ├── value_objects.py # Value objects
│       │   └── interfaces/     # Repository interfaces
│       │       └── repositories.py
│       ├── infrastructure/     # Infrastructure layer
│       │   └── persistence/    # Persistence implementations
│       │       ├── models/     # Database models
│       │       │   ├── mock.py # Mock models for testing
│       │       │   └── sqlite.py # SQLite database models
│       │       └── repositories/ # Repository implementations
│       │           ├── mock.py # Mock repository for testing
│       │           └── sqlite.py # SQLite repository implementation
│       ├── presentation/       # Presentation layer (API)
│       │   ├── api.py          # Resource API endpoints
│       │   └── dtos.py         # Data transfer objects
│       ├── tests/              # Feature tests
│       │   ├── application/    # Application layer tests
│       │   ├── infrastructure/ # Infrastructure layer tests
│       │   └── presentation/   # Presentation layer tests
│       └── di.py               # Dependency injection configuration
├── shared/                     # Shared utilities and common code
│   ├── application/            # Shared application layer
│   │   └── interfaces/         # Shared interfaces
│   │       └── base.py         # Base interfaces
│   ├── domain/                 # Shared domain layer
│   │   ├── entity.py           # Entity base class
│   │   ├── error_codes.py      # Shared error codes
│   │   ├── errors.py           # Shared error classes
│   │   ├── result.py           # Result type for operations
│   │   └── value_object.py     # Value object base class
│   ├── infrastructure/         # Shared infrastructure
│   │   └── db.py               # Database connection utilities
│   ├── presentation/           # Shared presentation layer
│   │   ├── api.py              # Shared API routes (e.g., health check)
│   │   ├── dto.py              # Base DTO class
│   │   ├── exception_mapper.py # Exception to response mapping
│   │   └── http_exception_handler.py # HTTP exception handling
│   ├── tests/                  # Shared tests
│   │   └── presentation/       # Shared presentation tests
│   │       └── api/            # API tests
│   └── utils.py                # Shared utility functions
└── main.py                     # FastAPI application entry point
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

The API will be available at `http://127.0.0.1:$PORT/`. Replace `$PORT` with the
port number you configured in the `.env` file (see the configuration section below).

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

- **Swagger UI**: `http://127.0.0.1:$PORT/docs`
- **ReDoc**: `http://127.0.0.1:$PORT/redoc`

Replace `$PORT` with the port number you configured in the `.env` file.

## 🧪 Testing

Run tests with pytest:
```bash
uv run -m pytest
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

1. Check the [commits guidelines](docs/COMMITS.md).
2. Follow the existing architecture patterns.
3. Add tests for new functionality.
4. Use type hints throughout.
5. Run linting with `ruff` before committing.

## 📄 License

This project is licensed under the [MIT License](LICENSE.md).
