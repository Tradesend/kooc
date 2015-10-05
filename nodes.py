from pyrser import parsing, meta


class Imp(parsing.Node):
    def __init__(self, value: str) -> object:
        self.value = value


@meta.add_method(Imp)
def to_c(self: Imp):
    return "#ifndef __{0}\n# define __{1}\n# include \"{2}.h\"\n#endif".format(
        self.value.replace('/', '_').replace('.', '_'), self.value.replace('.', '_').replace('/', '_'), self.value)
