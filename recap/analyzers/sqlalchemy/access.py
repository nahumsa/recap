import logging
from contextlib import contextmanager
from typing import Any, Generator

import sqlalchemy

from recap.analyzers.abstract import AbstractAnalyzer, BaseMetadataModel
from recap.browsers.db import TablePath, ViewPath, create_browser

log = logging.getLogger(__name__)


class UserAccess(BaseMetadataModel):
    privileges: list[str]
    read: bool
    write: bool


class Access(BaseMetadataModel):
    __root__: dict[str, UserAccess] = {}


class TableAccessAnalyzer(AbstractAnalyzer):
    """
    Fetches table access information from
    `information_schema.role_table_grants`.
    """

    def __init__(self, engine: sqlalchemy.engine.Engine):
        self.engine = engine

    def analyze(
        self,
        path: TablePath | ViewPath,
    ) -> Access | None:
        """
        :param path: Fetch access information for a table or view at this path.
        :returns: User and privilege information. None if the analyzer is
            unable to analyze the table or view.
        """

        table = path.table if isinstance(path, TablePath) else path.view
        with self.engine.connect() as conn:
            results = {}
            try:
                rows = conn.execute(
                    "SELECT * FROM information_schema.role_table_grants "
                    "WHERE table_schema = %s AND table_name = %s",
                    path.schema_,
                    table,
                )
                for row in rows.all():
                    privilege_type = row["privilege_type"]
                    user_grants: dict[str, Any] = results.get(
                        row["grantee"],
                        {
                            "privileges": [],
                            "read": False,
                            "write": False,
                        },
                    )
                    user_grants["privileges"].append(privilege_type)
                    if privilege_type == "SELECT":
                        user_grants["read"] = True
                    if privilege_type in ["INSERT", "UPDATE", "DELETE", "TRUNCATE"]:
                        user_grants["write"] = True
                    results[row["grantee"]] = user_grants
            except Exception as e:
                # TODO probably need a more tightly bound exception here
                # We probably don't have access to the information_schema, so
                # skip it.
                log.debug(
                    "Unable to fetch access for path=%s",
                    path,
                    exc_info=e,
                )
            if results:
                return Access.parse_obj(results)
            return None


@contextmanager
def create_analyzer(**config) -> Generator["TableAccessAnalyzer", None, None]:
    with create_browser(**config) as browser:
        yield TableAccessAnalyzer(browser.engine)
