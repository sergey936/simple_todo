from pydantic import BaseModel

from infra.repositories.filters.tasks import (
    GetTasksFilters as GetTaskInfraFilters,
)


class GetTasksFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetTaskInfraFilters(limit=self.limit, offset=self.offset)
