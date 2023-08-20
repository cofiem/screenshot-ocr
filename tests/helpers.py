import pathlib
from importlib import resources


def get_resource_path(end_path: str):
    full_path = resources.files("resources").joinpath(end_path)
    with resources.as_file(full_path) as file_path:
        result = normalise_path(file_path)
    return result


def normalise_path(path: pathlib.Path) -> pathlib.Path:
    if not path:
        return None
    return path.expanduser().resolve().absolute()
