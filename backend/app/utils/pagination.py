"""
app/utils/pagination.py
Reusable pagination query-param dependency.
"""

from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        limit: int = Query(default=20, ge=1, le=100),
        skip: int = Query(default=0, ge=0),
    ) -> None:
        self.limit = limit
        self.skip = skip
