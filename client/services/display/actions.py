
"""
Display Actions
"""


SET_LINE = "@display/SET_LINE"
ADD_LINE = "@display/ADD_LINE"

CLEAR    = "@display/CLEAR"


def set_line(line):
    return {
        "type": SET_LINE,
        "payload": {
            "line": line,
        },
    }


def add_line(line):
    return {
        "type": ADD_LINE,
        "payload": {
            "line": line,
        },
    }



def clear():
    return {
        "type": CLEAR,
    }

