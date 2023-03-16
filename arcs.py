def help():
    return """Arcs are a flexible design pattern for implementing custom functionality that can be hoatloaded into a spARK instance from a variety of sources. For more info use advhelp"""
def advhelp():
    return """Arcs are currently implemented in a rather primitive way using the importlib module. To add new arcs, create a function the a arcs.py file. Arguments are passed with *args"""
def hotload():
    return "This is an example of a hot loadable script."
def echo(val):
    return f"ECHO {val}"
def add(a, b):
    return int(a) + int(b)