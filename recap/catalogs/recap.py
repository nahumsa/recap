from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator

import httpx

from recap.server import DEFAULT_URL

from .abstract import AbstractCatalog


class RecapCatalog(AbstractCatalog):
    """
    The Recap catalog makes HTTP requests to Recap's REST API. You can enable
    RecapCatalog in your settings.toml with:

    ```toml
    [catalog]
    plugin = "recap"
    url = "http://localhost:8000"
    ```

    The Recap catalog enables different systems to share the same metadata
    when they all talk to the same Recap server.
    """

    def __init__(
        self,
        client: httpx.Client,
    ):
        self.client = client

    def touch(
        self,
        path: str,
    ):
        self.write(path, {})

    def write(
        self,
        path: str,
        metadata: dict[str, Any],
        patch: bool = True,
    ):
        method = self.client.patch if patch else self.client.put
        response = method(
            f"/catalog{path}/metadata",
            json=metadata,
        )
        response.raise_for_status()

    def rm(
        self,
        path: str,
    ):
        self.client.delete(f"/catalog{path}").raise_for_status()

    def ls(
        self,
        path: str,
        time: datetime | None = None,
    ) -> list[str] | None:
        params: dict[str, Any] = {}
        if time:
            params["time"] = time.isoformat()
        response = self.client.get(f"/catalog{path}/children", params=params)
        if response.status_code == httpx.codes.OK:
            return response.json()
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()

    def read(
        self,
        path: str,
        time: datetime | None = None,
    ) -> dict[str, Any] | None:
        params: dict[str, Any] = {}
        if time:
            params["time"] = time.isoformat()
        response = self.client.get(f"/catalog{path}/metadata", params=params)
        if response.status_code == httpx.codes.OK:
            return response.json()
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()

    def search(
        self,
        query: str,
        time: datetime | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"query": query}
        if time:
            params["time"] = time.isoformat()
        return self.client.get("/catalog", params=params).json()


@contextmanager
def create_catalog(
    url: str | None = None,
    **_,
) -> Generator["RecapCatalog", None, None]:
    with httpx.Client(base_url=url or DEFAULT_URL) as client:
        yield RecapCatalog(client)
