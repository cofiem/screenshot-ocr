from importlib import resources


def get_resource_path(end_path: str):
    full_path = resources.files("resources").joinpath(end_path)
    with resources.as_file(full_path) as file_path:
        result = file_path.absolute()
    return result
