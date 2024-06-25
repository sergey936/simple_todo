from typing import TypeVar, Generic

from pydantic import BaseModel


IT = TypeVar('IT')


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    limit: int
    offset: int
    items: IT
