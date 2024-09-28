from typing import List

from datetime import datetime


class Explanation:
    def __init__(self, content: str, adapted_from: List[int]):
        self.__content = content
        self.__adapted_from = adapted_from
        self.__created_at = datetime.now()

    def get_content(self) -> str:
        return self.__content

    def get_adapted_from(self) -> list[int]:
        return self.__adapted_from

    def get_created_at(self) -> datetime:
        return self.__created_at
