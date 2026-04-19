import typing as t
from databases import Database
from typeforms_domain.application_service.ports.output.repository.uow import AbstractUnitOfWork
from typeforms_dataaccess.databases.databases_form_repository import DatabasesFormRepository


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

    async def commit(self):
        if self._transaction:
            await self._transaction.commit()
            self._transaction = None

    async def rollback(self):
        if self._transaction:
            await self._transaction.rollback()
            self._transaction = None
