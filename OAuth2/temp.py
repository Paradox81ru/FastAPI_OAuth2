from enum import IntEnum

class MyEnum(IntEnum):
    @classmethod
    def get_names(cls):
        return tuple(val.name for val in cls)

    @classmethod
    def get_values(cls):
        return tuple(val.value for val in cls)
    
    @classmethod
    def get_items(cls):
        return {item.name: item.value for item in cls}


class UerStatus(MyEnum):
    DELETED = 1
    BLOCKED = 2
    ACTIVE = 3


def main():
    print(UerStatus.get_items())


if __name__ == '__main__':
    main()