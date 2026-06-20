# ddd-ecommerce

E-commerce API built with Domain-Driven Design principles using Python and FastAPI.

## Architecture

The project is structured around four bounded contexts:

- **Catalog** — products, categories, pricing
- **Orders** — cart, checkout, order lifecycle
- **Payments** — payment processing, refunds
- **Identity** — users, authentication, roles

Each context follows a layered DDD structure:

```
src/
├── domain/          # Entities, value objects, aggregates, domain events
├── application/     # Use cases, application services, DTOs
├── infrastructure/  # Repositories, ORM models, external adapters
└── api/             # FastAPI routes, request/response schemas
```

## Domain Model

### Orders Bounded Context

```
Order (Aggregate Root)
├── OrderItem (Entity)
├── ShippingAddress (Value Object)
└── OrderStatus (Enum)
```

`Order` enforces all business invariants: minimum order amount, maximum items per order, valid status transitions.

## Stack

- Python 3.12
- FastAPI 0.110
- SQLAlchemy 2.0 (async)
- PostgreSQL 16
- Pydantic v2

## Getting Started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn src.api.main:app --reload
```

## Running Tests

```bash
pytest tests/ -v
```
