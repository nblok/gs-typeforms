import typing as t
from abc import ABC, abstractmethod

from typeforms_domain.application_service.ports.output.repository.form_repository import (
    FormRepository,
)


class AbstractUnitOfWork(ABC):
    forms: FormRepository

    async def __aenter__(self) -> t.Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Automatically roll back if an exception occurs."""
        await self.rollback()

    @abstractmethod
    async def commit(self):
        """Persist changes to the database."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        """Discard changes."""
        raise NotImplementedError
