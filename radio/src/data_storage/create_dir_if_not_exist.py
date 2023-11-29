import os


def create_dir_if_not_exists(path: str):
    try:
        original_umask = os.umask(0)
        os.makedirs(path, 0o777, exist_ok=True)
    finally:
        os.umask(original_umask)
