from compiler import information
__author__ = 'collio_v'


class Error:
    def __init__(self, error: str):
        self.error = error

    def __repr__(self):
        return "kooc: " + information.File.name + ": " + self.error
