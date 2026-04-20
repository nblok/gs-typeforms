# API Coding Standards

This document defines the coding standards and architectural conventions for the `api/` backend application.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Package Structure](#package-structure)
3. [Domain Layer (`typeforms-domain/core`)](#domain-layer)
4. [Application Layer (`typeforms-domain/application_service`)](#application-layer)
5. [Data Access Layer (`typeforms-dataaccess`)](#data-access-layer)
6. [HTTP Layer (`rest-api`)](#http-layer)
7. [Dependency Injection](#dependency-injection)
8. [Naming Conventions](#naming-conventions)
9. [Code Style](#code-style)
10. [Logging](#logging)
11. [Testing](#testing)

---

## Architecture Overview

The backend follows Clean Architecture with Domain-Driven Design (DDD) tactical patterns. The dependency rule flows inward: nothing in an inner layer knows about outer layers.

```
┌─────────────────────────────────────────┐
│  HTTP Layer (rest-api)                  │  ← FastAPI routers, DI container
│  ┌───────────────────────────────────┐  │
│  │  Application Layer                │  │  ← App services, DTOs, ports
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Domain Layer               │  │  │  ← Entities, value objects, domain services
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│  Data Access Layer (typeforms-dataaccess)│  ← Repository/UoW implementations
└─────────────────────────────────────────┘
```

Dependency direction: `rest-api` → `typeforms-domain` → `common`; `typeforms-dataaccess` → `typeforms-domain`.

---

## Package Structure

The workspace has four packages with strict boundaries:

| Package | Path | Responsibility |
|---|---|---|
| `common` | `packages/common/` | Base DDD building blocks (`Entity`, `AggregateRoot`, `ValueObject`, `BaseId`) |
| `typeforms-domain` | `packages/typeforms-domain/` | Domain model and application services |
| `typeforms-dataaccess` | `packages/typeforms-dataaccess/` | Persistence implementations |
| `rest-api` | `apps/rest-api/` | FastAPI HTTP adapter and DI container |

Each package follows the `src/<package_name>/` source layout. Dev tooling (ruff, pytest, ty) is declared only in the root `api/pyproject.toml`.

**Dependency rules:**
- `common` has no project-level dependencies.
- `typeforms-domain` may depend on `common` and `pydantic`. It must not depend on `typeforms-dataaccess` or `rest-api`.
- `typeforms-dataaccess` may depend on `typeforms-domain`. It must not depend on `rest-api`.
- `rest-api` may depend on all packages.

---

## Domain Layer

Source: `packages/typeforms-domain/src/typeforms_domain/core/`

### Value Objects

Extend `ValueObject` (a frozen dataclass) from `common`. Equality is value-based; all fields must be hashable.

```python
# Frozen dataclass, equality by value
@dataclass(frozen=True)
class FieldDefinition(ValueObject):
    type: FieldType
    label: str
    description: str
    icon: str
    default_config: FieldConfig
```

For identifiers, extend `UUIDIdentifier` (which extends `BaseId[UUID]`). Create a dedicated class per aggregate — do not share ID types across aggregates.

```python
class FormId(UUIDIdentifier):
    pass

class FieldId(UUIDIdentifier):
    pass
```

### Entities

Extend `Entity[TId]` from `common`. Identity is based solely on the ID — do not override `__eq__` or `__hash__` in subclasses.

Use a `create()` class method as the factory for new instances (generates the UUID). Use a `from_dict()` class method for hydration from persistence.

```python
class Field(Entity[FieldId]):

    def __init__(self, field_id: FieldId, label: str, field_type: FieldType, order: int, required: bool):
        super().__init__(field_id)
        self.label = label
        ...

    @classmethod
    def create(cls, label: str, field_type: FieldType, order: int, required: bool = False) -> "Field":
        return cls(field_id=FieldId(value=uuid.uuid4()), ...)

    @classmethod
    def from_dict(cls, data: dict) -> "Field":
        return cls(field_id=FieldId(value=uuid.UUID(data["field_id"])), ...)
```

Only `AggregateRoot` subclasses are persisted as roots. Child entities (e.g. `Field`) are owned by and loaded through their aggregate.

### Aggregates

Aggregate roots extend `AggregateRoot[TId]`, which extends `Entity[TId]`. All mutation of child entities must go through the aggregate root.

```python
class Form(AggregateRoot[FormId]):
    ...
```

### Domain Services

Use `Protocol` for the interface and `Impl` suffix for the implementation, both in the same file under `core/service/`.

```python
class FieldDefinitionDomainService(t.Protocol):
    def get_field_definitions(self) -> list[FieldDefinition]: ...

class FieldDefinitionDomainServiceImpl(FieldDefinitionDomainService):
    def get_field_definitions(self) -> list[FieldDefinition]:
        return FIELD_DEFINITIONS
```

Domain services encapsulate business rules that do not naturally belong to a single entity. They must not depend on the application layer or repositories.

---

## Application Layer

Source: `packages/typeforms-domain/src/typeforms_domain/application_service/`

The application layer orchestrates domain objects and bridges the HTTP layer with the domain. It owns DTOs, port interfaces, and application service implementations.

### Input Ports (Application Service Interfaces)

Defined as `Protocol` classes under `ports/input/service/`. These are the contracts the HTTP layer depends on.

```python
# ports/input/service/form_application_service.py
class FormApplicationService(t.Protocol):
    async def create_form(self, create_form_command: CreateFormCommand) -> FormId: ...
```

### Output Ports (Repository and Unit of Work Interfaces)

Defined under `ports/output/repository/`. Repository interfaces use `Protocol`. The Unit of Work uses `ABC` with `abstractmethod` to enforce the async context manager contract.

```python
# ports/output/repository/form_repository.py
class FormRepository(t.Protocol):
    async def get(self, form_id: FormId) -> Form | None: ...
    async def save(self, form: Form) -> FormId: ...

# ports/output/repository/uow.py
class AbstractUnitOfWork(ABC):
    forms: FormRepository

    async def __aenter__(self) -> t.Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
```

### Application Service Implementations

Named `<Entity>ApplicationServiceImpl`. They implement the corresponding input port Protocol and receive dependencies via constructor injection.

Application services must:
- Accept and return DTOs, not domain entities.
- Use `async with self._uow` for all operations that require persistence.
- Delegate business rules to domain entities or domain services.
- Log at `INFO` level at the start of each method.

```python
class FormApplicationServiceImpl(FormApplicationService):

    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def create_form(self, create_form_command: CreateFormCommand) -> FormId:
        logger.info(f"Creating form: {create_form_command.model_dump()}")
        async with self._uow:
            form_id = await self._uow.forms.save(
                Form.create(
                    title=create_form_command.title,
                    fields=[field.model_dump() for field in create_form_command.fields],
                )
            )
        return form_id
```

### DTOs

All DTOs use `pydantic.BaseModel`. Place them in `dto/` grouped by domain area (e.g. `form_dtos.py`, `field_definition_dtos.py`).

**Commands** represent write operations:
- Name: `<Action><Entity>Command` (e.g. `CreateFormCommand`)
- Fields use the types required by the domain (e.g. `FieldType` enum, not raw strings)

**Response DTOs** represent read results:
- Name: `<Entity>ResponseDto`
- Use a `TypeAlias` for list responses: `FieldDefinitionResponsesDto: t.TypeAlias = list[FieldDefinitionResponseDto]`

**Discriminated unions** for polymorphic fields:
- Each variant has a `type: t.Literal[...]` field with a default value.
- Combine using `t.Annotated[t.Union[...], Field(discriminator="type")]`.

```python
class ShortTextConfigDto(BaseModel):
    type: t.Literal[FieldType.SHORT_TEXT] = FieldType.SHORT_TEXT
    placeholder: str
    max_length: int | None

FieldConfigDto = t.Annotated[
    t.Union[ShortTextConfigDto, LongTextConfigDto, ...],
    Field(discriminator="type"),
]
```

---

## Data Access Layer

Source: `packages/typeforms-dataaccess/src/typeforms_dataaccess/`

Implements the output port interfaces defined in `typeforms-domain`. Uses the `databases` library with the `aiosqlite` driver.

### Schema Definition

Define tables using `sqlalchemy.Table` (not ORM models) in `database.py`. Create a factory function `create_database(database_url, force_rollback)` that:
1. Declares schema with `sqlalchemy.MetaData` and `sqlalchemy.Table`.
2. Creates the schema synchronously via a sync engine.
3. Returns an async `databases.Database` instance.

```python
def create_database(database_url: str, force_rollback: bool = False) -> Database:
    metadata = sqlalchemy.MetaData()
    # ... table definitions ...
    sync_url = database_url.replace("sqlite+aiosqlite", "sqlite")
    engine = sqlalchemy.create_engine(sync_url, connect_args={"check_same_thread": False})
    metadata.create_all(engine)
    return databases.Database(database_url, force_rollback=force_rollback)
```

### Unit of Work Implementation

Named `Databases<Name>UnitOfWork`, implements `AbstractUnitOfWork`. Manage the database transaction in `__aenter__` / `__aexit__`. Commit on clean exit, rollback on exception. Repository instances are created in `__init__`.

```python
class DatabasesUnitOfWork(AbstractUnitOfWork):

    def __init__(self, db: Database):
        self._db = db
        self._transaction = None
        self.forms = DatabasesFormRepository(db)

    async def __aenter__(self) -> t.Self:
        self._transaction = self._db.transaction()
        await self._transaction.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
```

### Repository Implementation

Named `Databases<Entity>Repository`, implements the corresponding `Protocol` from `typeforms-domain`.

- Write raw SQL as module-level constants (uppercase names, e.g. `GET_QUERY_SQL`).
- Use named parameter binding (`:param_name`), never string interpolation.
- Use `ON CONFLICT ... DO UPDATE` (upsert) for `save()`.
- Reconstruct domain entities via `Entity.from_dict()`.
- Batch inserts for child entities via `execute_many()`.

```python
GET_QUERY_SQL = "SELECT id AS form_id, title, ... FROM form WHERE id = :id"

class DatabasesFormRepository(FormRepository):

    def __init__(self, db: Database):
        self._db = db

    async def get(self, form_id: FormId) -> Form | None:
        row = await self._db.fetch_one(GET_QUERY_SQL, {"id": str(form_id.value)})
        if row is None:
            return None
        return Form.from_dict(dict(row))

    async def save(self, form: Form) -> FormId:
        await self._db.execute(SAVE_INSERT_FORM_SQL, {"id": str(form.id.value), "title": form.title})
        if form.fields:
            await self._db.execute_many(SAVE_INSERT_FIELD_SQL, [...])
        return form.id
```

---

## HTTP Layer

Source: `apps/rest-api/src/rest_api/`

### App Factory

Define a `create_app() -> FastAPI` function in `rest_api/__init__.py`. It is responsible for:
1. Instantiating and configuring the DI container.
2. Wiring the container to router modules.
3. Defining the `lifespan` async context manager (connect/disconnect DB).
4. Including routers.

```python
def create_app() -> FastAPI:
    di_container = Container()
    di_container.config.database_url.from_env("DATABASE_URL")
    di_container.wire(modules=["rest_api.routers.form_routes", ...])

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        configure_logging()
        await di_container.db().connect()
        yield
        await di_container.db().disconnect()

    app = FastAPI(lifespan=lifespan)
    app.include_router(form_router)
    return app
```

### Routers

One file per resource under `routers/`, named `<resource>_routes.py`. Use `APIRouter` with a `prefix` and `tags`.

- Annotate each injected service with its input port Protocol type (not the implementation).
- Always apply `@inject` before `@router.<method>`.
- Pass command/query DTOs by name to application service methods.
- Specify `response_model` when returning a known DTO type.

```python
router = APIRouter(prefix="/forms", tags=["Forms"])

@router.post("/")
@inject
async def create_form(
    create_form_command: CreateFormCommand,
    form_application_service: t.Annotated[
        FormApplicationService,
        Depends(Provide[Container.form_application_service]),
    ],
):
    form_id = await form_application_service.create_form(create_form_command=create_form_command)
    return {"id": str(form_id.value)}
```

---

## Dependency Injection

Source: `apps/rest-api/src/rest_api/container.py`

Use a single `containers.DeclarativeContainer` subclass named `Container`.

| Provider | When to use |
|---|---|
| `providers.Configuration()` | External config (env vars) |
| `providers.Singleton(...)` | Stateful shared resources (e.g. `Database` connection) |
| `providers.Factory(...)` | Stateless services (new instance per injection) |

Wire the container by passing module path strings to `container.wire(modules=[...])`. Add every router module that uses `@inject`.

```python
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(create_database, config.database_url)
    unit_of_work = providers.Factory(DatabasesUnitOfWork, db=db)
    field_definition_domain_service = providers.Factory(FieldDefinitionDomainServiceImpl)
    form_application_service = providers.Factory(FormApplicationServiceImpl, uow=unit_of_work)
```

---

## Naming Conventions

| Component | Pattern | Example |
|---|---|---|
| Entity | Noun, singular | `Form`, `Field` |
| Aggregate root | Noun, singular (inherits `AggregateRoot`) | `Form` |
| Value object | Noun, no suffix | `FieldDefinition`, `FormId` |
| Domain ID | `<Entity>Id` | `FormId`, `FieldId` |
| Repository interface | `<Entity>Repository` | `FormRepository` |
| Application service interface | `<Entity>ApplicationService` | `FormApplicationService` |
| Domain service interface | `<Domain>DomainService` | `FieldDefinitionDomainService` |
| Implementation class | `<Interface>Impl` | `FormApplicationServiceImpl` |
| Data access implementation | `Databases<Interface>` | `DatabasesFormRepository`, `DatabasesUnitOfWork` |
| Command DTO | `<Action><Entity>Command` | `CreateFormCommand` |
| Response DTO | `<Entity>ResponseDto` | `FieldDefinitionResponseDto` |
| Config value object | `<Type>Config` | `ShortTextConfig`, `RatingConfig` |
| Enum | `PascalCase`, values `SCREAMING_SNAKE_CASE` | `FieldType.SHORT_TEXT` |
| Private instance fields | `_` prefix | `self._db`, `self._uow` |
| Router module | `<resource>_routes.py` | `form_routes.py` |
| SQL constants | `SCREAMING_SNAKE_CASE` | `GET_QUERY_SQL`, `SAVE_INSERT_FORM_SQL` |

---

## Code Style

- **Python**: 3.14+. Use `requires-python = ">=3.14"` in `pyproject.toml`.
- **Type hints**: Required on all public functions and methods.
- **Union syntax**: Use PEP 604 (`int | None`) not `Optional[int]`.
- **Typing import**: `import typing as t` — use `t.Protocol`, `t.Generic`, `t.TypeAlias`, etc.
- **Enums**: Use `StrEnum` for string-backed enumerations.
- **Frozen dataclasses**: Use `@dataclass(frozen=True)` for all value objects and config shapes.
- **f-strings**: Preferred over `.format()` or `%` formatting.
- **Walrus operator**: Use `:=` in conditionals to avoid redundant lookups.
- **Comments**: Avoid unless explaining a non-obvious constraint or invariant. No docstrings on obvious methods.
- **Formatting/linting**: `ruff check .` must pass. Run from `api/`.
- **Type checking**: `ty check` must pass. Run from `api/`.

---

## Logging

Use a per-module logger. Do not use the root logger.

```python
import logging
logger = logging.getLogger(__name__)
```

Log at the start of application service methods at `INFO` level, including relevant payload data:

```python
logger.info(f"Creating form: {create_form_command.model_dump()}")
logger.info(f"Getting field definition by type: {field_type.value}")
```

Logging is configured centrally in `rest_api/logging_config.py` using `rich.logging.RichHandler` for the console and a rotating file handler for persistence. Verbose third-party loggers (`databases`, `aiosqlite`) are suppressed to `WARNING`.

---

## Testing

Tests live under `tests/unit/` within each package, mirroring the source tree.

- Use pytest without custom plugins or base test classes.
- Group related tests in a class named `Test<Scenario>`.
- Name test methods `test_<condition>_<expected_result>`.
- Test domain objects directly — no mocking of internal collaborators. Mock at package boundaries only.
- Use `force_rollback=True` on the `Database` instance for integration tests to avoid polluting test state.

```python
class TestEntityEquality:
    def test_equal_when_same_id(self):
        assert ConcreteEntity(1) == ConcreteEntity(1)

    def test_not_equal_when_different_id(self):
        assert ConcreteEntity(1) != ConcreteEntity(2)
```