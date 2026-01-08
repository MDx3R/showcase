from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from .session_factory import ISessionFactory


@dataclass
class Transaction:
    session: AsyncSession
    nesting_level: int = 0

    def should_commit(self) -> bool:
        return self.nesting_level == 0

    def enter(self) -> None:
        self.nesting_level += 1

    def exit(self) -> None:
        self.nesting_level -= 1


class UnitOfWork:
    """Minimal UnitOfWork managing AsyncSession lifecycle and nesting."""

    def __init__(self, session_factory: ISessionFactory) -> None:
        self.session_factory = session_factory
        self._current_transaction: ContextVar[Transaction | None] = ContextVar(
            "_current_transaction", default=None
        )

    async def commit(self) -> None:
        session = self._get_session()
        if not session.is_active:
            await self.rollback()
            raise ValueError("Session is inactive")
        await session.commit()

    async def rollback(self) -> None:
        session = self._get_session()
        await session.rollback()

    async def close(self) -> None:
        session = self._get_session()
        await session.close()

    async def __aenter__(self) -> UnitOfWork:
        if not self._transaction_exists():
            tx = self._create_transaction()
            self._set_transaction(tx)
        else:
            tx = self._get_transaction()
            tx.enter()
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception] | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._finalize_transaction(exc_type is not None)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager to obtain the current session or create a temporary one."""
        if self._transaction_exists():
            yield self._get_session()
            return

        async with self as uow:
            yield uow._get_session()

    async def _finalize_transaction(self, has_error: bool) -> None:
        if not self._transaction_exists():
            return

        tx = self._get_transaction()
        if has_error:
            await self.rollback()
        elif tx.should_commit():
            await self.commit()

        if tx.should_commit():
            await self.close()
            self._reset_session()
        else:
            tx.exit()

    def _get_session(self) -> AsyncSession:
        return self._get_transaction().session

    def _get_transaction(self) -> Transaction:
        tx = self._current_transaction.get()
        if tx is None:
            raise ValueError("Transaction not found")
        return tx

    def _transaction_exists(self) -> bool:
        return self._current_transaction.get() is not None

    def _create_transaction(self) -> Transaction:
        session = self.session_factory.create()
        return Transaction(session, 0)

    def _set_transaction(self, session: Transaction) -> None:
        self._current_transaction.set(session)

    def _reset_session(self) -> None:
        self._current_transaction.set(None)
