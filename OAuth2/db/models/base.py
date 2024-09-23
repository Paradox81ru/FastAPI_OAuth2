from copy import copy
from typing import Container
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm import AttributeState
from sqlalchemy.inspection import inspect


class Base(DeclarativeBase):
    def to_dict(self, *, exclude: list[str] = None):
        _exclude = copy(exclude) if exclude is not None else []
        _exclude.extend(('_sa_instance_state', ))
        mapper = inspect(self)
        # return mapper.dict
        fields = {}
        for field_name in mapper.dict:
            if field_name in _exclude:
                continue
            fields[field_name] = mapper.dict[field_name]
        return fields
    
    def __repr__(self) -> str:
        attrs = tuple(f"{field}={f'\'{value}\'' if isinstance(value, str) else value}" for field, value in self.to_dict().items())
        return f"{self.__class__.__name__}({', '.join(attrs)})"