from dataclasses import dataclass


@dataclass
class GetTasksFilters:
    limit: int = 10
    offset: int = 0
