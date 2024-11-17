from typing import Any, List
from abc import ABC, abstractmethod


class DataBase(ABC):
    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def put_item(self, item: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Any]:
        raise NotImplementedError
