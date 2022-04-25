# Author: Alex Xu
# Description: This file is used to provide database function prototype.

def add(username: str, password: str) -> bool:
    """
    Add an administrator account with the specified username and password. The strings must be non-empty, and the username must contain only `[A-Za-z0-9_]`.

    Returns `True` if succeed, `False` if the username existed.
    """
    pass

def check(username: str, password: str)-> bool:
    """
    Check if the given credential is a valid administrator account.

    Returns `True` if the credential is valid, `False` otherwise.
    """
    return True

def remove(username: str)-> None:
    """
    Removes the administrator with the specified username.

    Returns `None` always.
    """
    pass
