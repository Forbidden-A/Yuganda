import typing
from asyncio import get_running_loop
from functools import wraps
from io import TextIOWrapper


def get_resource(name: str, mode: str = "r") -> TextIOWrapper:
    return open(f"yuganda/resources/{name}")


async def use_resource_async(
    name: str, callback: typing.Callable[TextIOWrapper, typing.Any], mode: str = "r"
) -> typing.Any:
    @wraps(callback)
    def wrapper():
        with get_resource(name, mode) as fp:
            return callback(fp)

    return await get_running_loop().run_in_executor(wrapper())
