# Hexagon Architecture API

A FastAPI-based API project implementing clean architecture (hexagonal architecture) patterns for maintainable and testable code.

## 🏗️ Architecture

This project follows the **Hexagonal Architecture** (Ports and Adapters) pattern, providing:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and application services
- **Infrastructure Layer**: External adapters (database, web framework)
- **Dependency Injection**: Using Lagom for clean dependency management

## 🚀 Technology Stack

- **FastAPI** 0.116+ - Modern, fast web framework for building APIs
- **SQLActive** - Lightweight SQL toolkit for database operations
- **SQLite** - Database (via aiosqlite for async operations)
- **Lagom** - Dependency injection container
- **Pydantic** - Data validation and settings management
- **ORJSON** - Fast JSON serialization
- **Uvloop** - High-performance event loop

## 📁 Project Structure

```
src/
├── main.py                 # FastAPI application entry point
├── shared/                 # Shared utilities and common code
│   └── api.py             # Shared API routes (health check)
└── resources/             # Resources domain module
    ├── api.py             # Resource API endpoints
    ├── di.py              # Dependency injection configuration
    ├── domain/            # Domain layer
    │   └── repositories/  # Repository interfaces
    └── infrastructure/    # Infrastructure layer
        ├── models/        # Database models
        └── repositories/  # Repository implementations
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

### Running the Application

For development:
```bash
fastapi dev src/main.py
```

For production:
```bash
fastapi run src/main.py
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Documentation

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

## 🔧 Configuration

The application uses environment-based configuration. Key settings are managed in `src/shared/settings.py`.

### Database

- **Development**: SQLite database
- **Connection**: Configured via `DATABASE_URL` setting
- **Migrations**: Automatic table creation on startup

## 📋 Available Endpoints

### Health Check
- `GET /health` - Application health status

### Resources
- Resource endpoints are available under the `/resources` prefix

## 🏛️ Clean Architecture Benefits

This project structure provides:

- **Testability**: Easy to unit test business logic
- **Maintainability**: Clear separation of concerns
- **Flexibility**: Easy to swap implementations (e.g., database providers)
- **Independence**: Domain logic independent of frameworks

## 🤝 Contributing

1. Follow the existing architecture patterns
2. Add tests for new functionality
3. Use type hints throughout
4. Run linting with `ruff` before committing

## 📄 License

This project is a base template for FastAPI applications with clean architecture.
