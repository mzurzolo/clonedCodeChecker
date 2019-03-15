"""Dumping ground for functions not defined elsewhere."""


def cache_filename(path):
    """Turn absolute path into filename used in filecache."""
    # remove the first /, replace slashes with dots, add file extension
    # this: [1:] means "from the first element to the end."
    # list[1:10] would give me from the first element to the 9th
    # list[1:-1] would give me everything but the first and last element
    return path.replace("/", ".")[1:] + ".yaml"
