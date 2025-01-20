from typing import Optional


def convert_string_to_type(value: str) -> Optional[type]:
    """
    Convert a string value to a type if it is a built-in type.

    Args:
        value (str): The string value to convert to a type.

    Returns:
        Optional[type]: The type if it is a built-in type, otherwise None.
    """
    if value in __builtins__:
        return __builtins__[value]
    return None
