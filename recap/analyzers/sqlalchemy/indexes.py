import logging
from contextlib import contextmanager
from typing import Generator

import sqlalchemy

from recap.analyzers.abstract import AbstractAnalyzer, BaseMetadataModel
from recap.browsers.db import TablePath, ViewPath, create_browser

log = logging.getLogger(__name__)


class Index(BaseMetadataModel):
    columns: list[str]
    unique: bool


class Indexes(BaseMetadataModel):
    __root__: dict[str, Index] = {}


class TableIndexAnalyzer(AbstractAnalyzer):
    """
    Use SQLAlchemy to fetch index information for a table.
    """

    def __init__(self, engine: sqlalchemy.engine.Engine):
        self.engine = engine

    def analyze(
        self,
        path: TablePath | ViewPath,
    ) -> Indexes | None:
        """
        :param path: Fetch index information for a table at this path.
        :returns: Index information or None if the table has no indexes.
        """

        table = path.table if isinstance(path, TablePath) else path.view
        indexes = {}
        index_dicts = sqlalchemy.inspect(self.engine).get_indexes(
            table,
            path.schema_,
        )
        for index_dict in index_dicts:
            indexes[index_dict["name"]] = {
                "columns": index_dict.get("column_names", []),
                "unique": index_dict["unique"],
            }
        if indexes:
            return Indexes.parse_obj(indexes)
        return None


@contextmanager
def create_analyzer(
    **config,
) -> Generator["TableIndexAnalyzer", None, None]:
    with create_browser(**config) as browser:
        yield TableIndexAnalyzer(browser.engine)
