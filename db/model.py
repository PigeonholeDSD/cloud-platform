# Author: Alex Xu
# Description: This file is used to provide database function prototype.

def getBase() -> str:
    """
    Get the path of the base model.

    Returns an absolute path if set, `None` otherwise.
    """
    pass

def setBase(path: str) -> None:
    """
    Set the path of the base model. Must be an absolute path.

    Returns `None` always.
    """
    pass
