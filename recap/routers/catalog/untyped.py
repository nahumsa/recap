from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException

from recap.catalogs.abstract import AbstractCatalog
from recap.server import get_catalog

router = APIRouter(
    prefix="/catalog",
)


@router.get(
    "/{path:path}/metadata",
    response_model_exclude_defaults=True,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
def read_metadata(
    path: str,
    time: datetime | None = None,
    catalog: AbstractCatalog = Depends(get_catalog),
) -> dict[str, Any]:
    print(clean_path(path))
    metadata = catalog.read(clean_path(path), time)
    if metadata:
        return metadata
    raise HTTPException(status_code=404)


@router.patch("/{path:path}/metadata")
def patch_metadata(
    path: str,
    metadata: dict[str, Any] = Body(),
    catalog: AbstractCatalog = Depends(get_catalog),
):
    catalog.write(clean_path(path), metadata, True)


@router.put("/{path:path}/metadata")
def put_metadata(
    path: str,
    metadata: dict[str, Any] = Body(),
    catalog: AbstractCatalog = Depends(get_catalog),
):
    catalog.write(clean_path(path), metadata)


@router.get("/{path:path}/children")
def list_children(
    path: str,
    time: datetime | None = None,
    catalog: AbstractCatalog = Depends(get_catalog),
) -> list[str]:
    children = catalog.ls(clean_path(path), time)
    if children:
        return children
    raise HTTPException(status_code=404)


@router.delete("/{path:path}")
def remove_directory(
    path: str,
    catalog: AbstractCatalog = Depends(get_catalog),
):
    catalog.rm(clean_path(path))


@router.get("")
def query_search(
    query: str,
    time: datetime | None = None,
    catalog: AbstractCatalog = Depends(get_catalog),
) -> list[dict[str, Any]]:
    return catalog.search(query, time)


def clean_path(path: str) -> str:
    return str(PurePosixPath("/", path))
