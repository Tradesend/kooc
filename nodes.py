from pyrser import parsing, meta
from cnorm import nodes


class Imp(parsing.Node):
    def __init__(self, value: str) -> object:
        self.value = value


class Namespace(nodes.BlockStmt):
    def __init__(self, name: str) -> object:
        super().__init__([])
        self.name = name


class Defn(nodes.BlockStmt):
    def __init__(self, name: str) -> object:
        nodes.BlockStmt.__init__(self, [])
        self.name = name


class Class(nodes.Decl):
    def __init__(self, name: str) -> object:
        nodes.Decl.__init__(self, '', nodes.ComposedType(name))
        self._ctype._specifier = 1
        self._ctype.fields = []
        self.class_name = name


class Impl(nodes.BlockStmt):
    def __init__(self, name: str) -> object:
        super().__init__([])
        self.name = name


class Access(parsing.Node):
    def __init__(self) -> object:
        self.get = "private"
        self.set = "private"


class Callable(parsing.Node):
    def __init__(self) -> object:
        self.virtual = False
        self.static = False
        self.access = "private"


class KoocId(nodes.Id):
    def __init__(self):
        nodes.Id.__init__(self, "")
        self.scope = []


class New(nodes.Func):
    def __init__(self, type, call_expr, params):
        nodes.Func.__init__(self, call_expr, params)
        self._type = type


class Delete(nodes.Func):
    def __init__(self, type, call_expr, params):
        super().__init__(call_expr, params)
        self._type = type


class Constructor(nodes.Decl):
    def __init__(self, declaration: nodes.Decl, accessibility: Access):
        super().__init__(declaration._name, declaration._ctype)
        self.accessibility = accessibility


class Destructor(nodes.Decl):
    def __init__(self, declaration: nodes.Decl, accessibility: Access):
        super().__init__(declaration._name, declaration._ctype)
        self.accessibility = accessibility


class Attribute(nodes.Decl):
    def __init__(self, declaration: nodes.Decl, accessibility: Access):
        super().__init__(declaration._name, declaration._ctype)
        self.accessibility = accessibility


class Method(nodes.Decl):
    def __init__(self, declaration: nodes.Decl, accessibility: Access):
        super().__init__(declaration._name, declaration._ctype)
        self.accessibility = accessibility


class MethodImplementation(nodes.Decl):
    def __init__(self, declaration: nodes.Decl):
        super().__init__(declaration._name, declaration._ctype)


class ConstructorImplementation(nodes.Decl):
    def __init__(self, declaration: nodes.Decl):
        super().__init__(declaration._name, declaration._ctype)


class DestructorImplementation(nodes.Decl):
    def __init__(self, declaration: nodes.Decl):
        super().__init__(declaration._name, declaration._ctype)


@meta.add_method(Imp)
def to_c(self: Imp):
    return "#ifndef __{0}\n# define __{1}\n# include \"{2}.h\"\n#endif\n" \
        .format(
        self.value.replace('/', '_').replace('.', '_'),
        self.value.replace('.', '_').replace('/', '_'),
        self.value)
