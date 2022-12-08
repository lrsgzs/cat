TAB_STRING = "    "
ERROR_STRING = """\033[31mError:
    File {{file}}
    {{code}}
{{error}}: {{text}}\033[0m
"""


class PyCodeClass(object):
    def __init__(self, py_code=""):
        self.py_code = py_code


class Functions(object):
    def __init__(self):
        self.functions = [
            "input", "int", "list", "float", "str",
            "repr", "exec", "eval", "isinstance", "exit",
            "output", "raise"
        ]
