from pyrser import parsing

class Imp(parsing.Node):
    def __init__(self, name: str) -> object:
        self.name = name
