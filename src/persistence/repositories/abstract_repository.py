from typing import TypeVar, Optional, List, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    @abstractmethod
    def add(self, obj: T) -> None: ...

    @abstractmethod
    def update(self, obj: T) -> None: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...

    @abstractmethod
    def get(self, id: str) -> Optional[T]: ...

    @abstractmethod
    def list_all(self) -> List[T]: ...
