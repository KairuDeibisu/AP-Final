

def StringBuilder(*args, delimiter: str = " ") -> str:
    """
    Convert args to string with delimiter between each item.
    """
    string_args = [str(arg) for arg in args]
    return delimiter.join(string_args)
