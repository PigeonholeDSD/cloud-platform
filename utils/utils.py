# Author: Alex Xu
# Description: Utilities.

import json

def check_sign(sign: str) -> bool:
    """
    Check the signature of the request.
    """
    if (sign == "ticket"):
        return True
    return False

def get_sign() -> str:
    return "6bce5953a9506d6c14f2522fd6228afbee394da3"

class APIParseError(Exception):
    """
    A error raised when something goes wrong during the API parsing.
    """

    def __init__(self, msg, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self):
        return self.msg

class APIPropObject():
    """
    Describes an API property.

    It has three fields: `name`, `dtype` and `help`.
    """
    def __init__(self, name: str, dtype: type, help: str) -> None:
        self.name: str = name
        self.dtype: type = dtype
        self.help: str = help

class APIParser():
    """
    Parse data for REST APIs.

    Raises `APIParseError` if the data is not a valid JSON string or does not have some required properties.

    Returns `dict` always. 
    """
    def __init__(self) -> None:
        self.api_prop = []

    def add_prop(self, name: str, dtype: type, help: str = "") -> None:
        self.api_prop.append(APIPropObject(name, dtype, help))

    def parse(self, data: bytes) -> dict:
        try:
            parse_data = json.loads(data)
        except json.JSONDecodeError:
            raise APIParseError(msg="Invalid JSON string")
        if (not isinstance(parse_data, dict)):
            raise APIParseError(msg="Expecting a dictionary for API")
        key_list = parse_data.keys()
        dic = {}
        for item in self.api_prop:
            if (item.name not in key_list):
                raise APIParseError(msg="Expecting property '{}', but not found while parsing".format(item.name))
            if (not isinstance(parse_data[item.name], item.dtype)):
                raise APIParseError(msg="Expecting type {} for property '{}', but found type {}".format(item.dtype, item.name, type(parse_data[item.name])))
            dic[item.name] = parse_data[item.name]
        return dic
