# Author: Alex Xu
# Description: This file is used to provide database function prototype.
import uuid

class Device():
    """
    Class Device
    ```
    db.device.Device.banned: bool
    ```

    Indicate if the device is banned from the cloud services.

    Defaults to `False`.

    ```
    db.device.Device.email: str
    ```

    The device's contact email, if exists. Support at least 254 characters, `ValueError` should be raised if exceeded.

    Defaults to `None`.

    ```
    db.device.Device.model: str
    ```

    The path of the device's model file, if exists. Must be an absolute path.

    On assignment, it's expected to copy the file specified into the database, rather than just changing the path. When `None` is assigned, delete the model.

    Defaults to `None`.

    ```

    db.device.Device.calibration: str
    ```

    The path of the device's calibration data directory, if exists, with some `.csv` motion data files named with the motion recorded. Must be an absolute path.

    On assignment, it's expected to copy the files in the directory specified into the database, rather than just changing the path. When `None` is assigned, delete the data.

    Defaults to `None`.
    """

    def __init__(self) -> None:
        self.id: uuid.UUID = None
        self.banned: bool = False
        self.email: str|None = None
        self.model: str|None = None
        self.calibration: str|None = None

def get(uuid: str|uuid.UUID, create: bool=False) -> Device:
    """
    Get the `db.device.Device` object of the device with a specified UUID. The UUID must be a valid UUIDv4.

    If the `create` is set to `True`, the device entry is created and returned if not found.

    Returns a `db.device.Device` instance if the device is found or created, `None` otherwise.
    """
    new_device = Device()
    new_device.id = uuid.UUID(str(uuid))
    new_device.banned = False
    new_device.email = "123@qq.com"
    new_device.model = "./app.py"
    new_device.calibration = "/"
    return new_device

def remove(uuid: str)-> None:
    """
    Delete everything about the device with the specified UUID.

    Returns `None` always.
    """
    pass
