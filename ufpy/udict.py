from typing import Generic, Iterator, overload, TypeVar

from . import set_items_for_several_keys
from .cmp import cmp_generator
from .i import i_generator
from .utils import get_items_for_several_keys

__all__ = (
    'UDict',
)

KT = TypeVar('KT')
VT = TypeVar('VT')

@cmp_generator
@i_generator
class UDict(Generic[KT, VT]):
    @overload
    def __init__(self, dictionary: dict[KT, VT]): ...
    @overload
    def __init__(self, dictionary: dict[KT, VT], *, default: VT): ...
    @overload
    def __init__(self, **kwargs: VT): ...
    @overload
    def __init__(self, *, default: VT, **kwargs: VT): ...
    def __init__(self, dictionary = None, *, default = None, **kwargs):
        self.__dict = dictionary if dictionary is not None else kwargs
        self.__default = default
    
    # dictionary
    @property
    def dictionary(self) -> dict[KT, VT]:
        return self.__dict
    
    @dictionary.setter
    def dictionary(self, value: "dict[KT, VT] | UDict"):
        if isinstance(value, UDict):
            value = value.dictionary
        self.__dict = value
    
    # default
    @property
    def default(self) -> VT:
        return self.__default
    
    @default.setter
    def default(self, value: VT):
        self.__default = value
    
    # Reverse
    def reverse(self) -> "UDict[KT, VT]":
        keys, values = list(self.__dict.keys())[::-1], list(self.__dict.values())[::-1]
        self.__dict = dict(list(zip(keys, values)))
        return UDict(self.__dict)
    
    def __neg__(self) -> "UDict[KT, VT]":
        d = self
        return d.reverse()

    # Get items
    def __get_keys_from_slice_or_int(self, key: KT | int | slice) -> list[KT]:
        if isinstance(key, int) and key not in self.__dict:
            return [list(self.__dict.keys())[key - 1]]
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self) + 1)
            indexes = list(range(start, stop + 1, step))
            return [list(self.__dict.keys())[i - 1] for i in indexes]
        return [key]
    
    def __getitem__(self, key: KT | int | slice) -> "UDict[KT, VT] | VT":
        keys = self.__get_keys_from_slice_or_int(key)

        l = get_items_for_several_keys(self.__dict, keys, self.__default)
        return l if len(l) > 1 else l[0]

    def __setitem__(self, key: KT | int | slice, value: VT | list[VT]):
        keys = self.__get_keys_from_slice_or_int(key)
        values = [value] if not isinstance(value, list) else value

        self.__dict = set_items_for_several_keys(self.__dict, keys, values)


    # TODO: make __delitem__()
    # def __delitem__(self, key: KT | int | slice): ...

    # TODO: make __getattr__()
    # def __getattr__(self, name: str): ...

    # TODO: make __getattr__()
    # def __setattr__(self, name: str, value: VT): ...

    # TODO: make __delattr__()
    # def __delattr__(self, name: str): ...

    # Len, iterator and reversed version
    def __len__(self) -> int:
        return len(self.__dict.keys())
    
    def __iter__(self) -> Iterator[tuple[KT, VT]]:
        res = []
        
        for k, v in self.__dict.items():
            res.append((k, v))
        
        return iter(res)
    
    def __reversed__(self) -> 'UDict': ...
    
    # Booleans
    def __contains__(self, item: tuple[KT, VT] | KT) -> bool: ...
    
    # Transform to other types
    def __repr__(self) -> str:
        return f'''u{self.__dict}'''
    
    # Comparing
    def __cmp__(self, other: "dict[KT, VT] | UDict") -> int:
        return len(self) - len(other)
    
    def __eq__(self, other: "dict[KT, VT] | UDict") -> bool:
        if isinstance(other, UDict):
            other = other.dictionary
        return self.__dict == other
    
    # Math operations
    def __add__(self, other: "dict[KT, VT] | UDict") -> "UDict":
        new_dict = self.__dict
        
        if isinstance(other, UDict):
            other = other.dictionary
        
        for k, v in other.items():
            new_dict[k] = v
        return UDict(new_dict)
    
    def __sub__(self, other: "dict[KT, VT] | UDict") -> "UDict":
        new_dict = self.__dict
        
        if isinstance(other, UDict):
            other = other.dictionary
        
        for k, v in other.items():
            if new_dict.get(k) == v:
                del new_dict[k]
        return UDict(new_dict)
    
    def __mul__(self, other: "dict[KT, float | int] | UDict[KT, float | int] | float | int") -> "UDict":
        new_dict = self.__dict
        
        if isinstance(other, UDict):
            other = other.dictionary
        if isinstance(other, (int, float)):
            other = dict([(k, other) for k in new_dict.keys()])
        
        for k, v in other.items():
            new_dict[k] *= v
        
        return UDict(new_dict)

    def __truediv__(self, other: "dict[KT, float | int] | UDict[KT, float | int] | float | int") -> "UDict":
        new_dict = self.__dict
        
        if isinstance(other, UDict):
            other = other.dictionary
        if isinstance(other, (int, float)):
            other = dict([(k, other) for k in new_dict.keys()])
        
        for k, v in other.items():
            new_dict[k] /= v
        
        return UDict(new_dict)
