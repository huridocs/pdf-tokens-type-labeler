from enum import Enum


class TaskMistakesType(Enum):
    CORRECT = "CORRECT"
    WRONG = "WRONG"
    MISSING = "MISSING"

    @staticmethod
    def contains(key: str):
        return key.upper() in [e.value for e in TaskMistakesType]
