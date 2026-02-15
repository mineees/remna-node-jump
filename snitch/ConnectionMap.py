from json import dumps

from Connection import Connection


class ConnectionMap:
    def __init__(self):
        self.__map: dict = {}

    def get(self) -> dict:
        return self.__map

    def add(self, connection: Connection) -> None:
        self.__map[connection.ip] = connection

    def delete(self, identifier: str) -> None:
        del self.__map[identifier]

    def exists(self, identifier: str) -> bool:
        return identifier in self.__map

    def serialize(self) -> list:
        return [connection.serialize() for connection in self.to_list()]

    def to_list(self) -> list:
        return list(self.__map.values())

    def to_str(self) -> str:
        return dumps(self.serialize())
