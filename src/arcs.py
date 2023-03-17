def help():
    return """Arcs are a flexible design pattern for implementing custom functionality that can be hoatloaded into a spARK instance from a variety of sources. For more info use advhelp"""


def advhelp():
    return """Arcs are currently implemented in a rather primitive way using the importlib module. To add new arcs, create a function the a arcs.py file. Arguments are passed dynamically with *args so its on you to sort tyope conversion and other logic. The plan is replace this with an interface that allows for richer integrations and more sophisticated systems."""


def hotload():
    return "This is an example of a hot loadable script."


def echo(val: str):
    """Repeats the string back

    Args:
        val (str): the string to repeat

    Returns:
        string: the echo plus the original string
    """
    return f"ECHO {val}"


def add(*args):
    """Perorms integer addition

    Returns:
        int: the sum of all arguments
    """
    total = 0
    for n in args:
        total += int(n)
    return total
