from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import PurePosixPath
from typing import Any, Generator, List


class AbstractCatalog(ABC):
    @abstractmethod
    def touch(
        self,
        path: PurePosixPath,
    ):
        raise NotImplementedError

    @abstractmethod
    def write(
        self,
        path: PurePosixPath,
        type: str,
        metadata: Any,
    ):
        raise NotImplementedError

    @abstractmethod
    def rm(
        self,
        path: PurePosixPath,
        type: str | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def ls(
        self,
        path: PurePosixPath,
    ) -> List[str] | None:
        raise NotImplementedError

    @abstractmethod
    def read(
        self,
        path: PurePosixPath,
    ) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> List[dict[str, Any]]:
        raise NotImplementedError

    @staticmethod
    @contextmanager
    @abstractmethod
    def open(**config) -> Generator['AbstractCatalog', None, None]:
        raise NotImplementedError
