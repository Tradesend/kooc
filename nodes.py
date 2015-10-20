from pyrser import parsing, meta
from cnorm import nodes


class Imp(parsing.Node):
    def __init__(self, value: str) -> object:
        self.value = value


class Nmspce(nodes.BlockStmt):
    def __init__(self, name: str) -> object:
        nodes.BlockStmt.__init__(self, [])
        self.types = {}
        self.name = name

class Defn(nodes.BlockStmt):
    def __init__(self, name: str) -> object:
        nodes.BlockStmt.__init__(self, [])
        self.types = {}
        self.name = name

@meta.add_method(Imp)
def to_c(self: Imp):
    return "#ifndef __{0}\n# define __{1}\n# include \"{2}.h\"\n#endif\n"\
        .format(
        self.value.replace('/', '_').replace('.', '_'),
        self.value.replace('.', '_').replace('/', '_'),
        self.value)
