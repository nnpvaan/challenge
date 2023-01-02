from typing import Union


class ServerErrorException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class ItemDoesNotExistErrorException(Exception):
    def __init__(self, item: str, item_id: Union[str, int]):
        self.item = item
        self.item_id = item_id

    def __str__(self):
        return f"{self.item} with id: {self.item_id} does not exist"