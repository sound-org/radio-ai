import os


def create_dir_if_not_exists(path: str):
    """
    Create a directory if it does not already exist.

    Args:
        path (str): The path of the directory to be created.

    Returns:
        None
    """
    try:
        original_umask = os.umask(0)
        os.makedirs(path, 0o777, exist_ok=True)
    finally:
        os.umask(original_umask)
