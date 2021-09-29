import typing

__all__ = ["find"]


T = typing.TypeVar("T")


def find(iterable: typing.Iterable[T], predicate: typing.Callable[[T], bool]):
    for i in iterable:
        if predicate(i):
            return i
