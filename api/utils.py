from enum import IntEnum


class UserTypes(IntEnum):
    EMPLOYEE = 1
    RESTAURANT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
