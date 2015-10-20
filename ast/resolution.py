from pyrser import meta
from pyrser.parsing import node
from compiler import mangler
import copy
import cnorm
import nodes
import kooc


class NodeModification:
    def __init__(self):
        self.dictionary = {}
        self.heap_dictionary = {}

    def push(self, key, mod):
        if key in self.dictionary:
            if key in self.heap_dictionary:
                self.heap_dictionary[key].append(mod)
            else:
                self.heap_dictionary[key] = [mod]
        self.dictionary[key] = mod

    def pop(self, key):
        if key in self.heap_dictionary:
            self.dictionary[key] = self.heap_dictionary[key].pop()
        else:
            self.dictionary.pop(key)

    def use(self, obj):
        if type(obj) in self.dictionary:
            self.dictionary[type(obj)](obj)


nm = NodeModification()


def sub_resolution(var, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler, parents):
    if isinstance(var, node.Node):
        return var.kooc_resolution(ast, mangler, parents)
    elif isinstance(var, dict):
        return {_key: _var for _key, _var in var.items() if not sub_resolution(_var, ast, mangler, parents)}
    elif isinstance(var, str):
        return var
    elif hasattr(var, '__iter__'):
        bod = []
        for _var in var:
            __var = sub_resolution(_var, ast, mangler, parents)
            if isinstance(__var, list):
                bod = bod + __var
            elif not (__var is None):
                bod.append(__var)
        return bod
    return var


def _kooc_resolution(self, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler, parents):
    dellist = []
    parents.append(self)
    for var in vars(self):
        if getattr(self, var) is not None:
            _var = sub_resolution(getattr(self, var), ast, mangler, parents)
            if _var is None:
                dellist.append(var)
            else:
                setattr(self, var, _var)
    for _del in dellist:
        delattr(self, _del)
    parents.pop()
    return self


def sub_search_in_tree(var, predicate: callable, parents: list):
    if isinstance(var, node.Node):
        return var.search_in_tree(predicate, parents)
    elif isinstance(var, str):
        return None
    elif hasattr(var, '__iter__'):
        for _var in var:
            __var = sub_search_in_tree(_var, predicate, parents)
            if __var is not None:
                return __var
    return None


@meta.add_method(node.Node)
def search_in_tree(self, predicate: callable, parents: list = list()):
    if predicate(self, parents):
        return self
    parents.append(self)
    for var in vars(self):
        _var = sub_search_in_tree(getattr(self, var), predicate, parents)
        if _var is not None:
            return _var
    parents.pop()
    return None


@meta.add_method(nodes.Imp)
def search_in_tree(self: nodes.Imp, predicate: callable, parents: list):
    if not hasattr(self, 'imported'):
        self.imported = kooc.Kooc().parse_file('{0}.kh'.format(self.value))
    ret = self.imported.search_in_tree(predicate)
    if ret is None:
        ret = node.Node.search_in_tree(self, predicate, parents)
    return ret


@meta.add_method(node.Node)
def kooc_resolution(self, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler = mangler.Mangler(),
                    parents: list = list()):
    global nm
    nm.use(self)
    if hasattr(self, '_name'):
        self._name = _mangler.name(self._name).mangle("container", "name")
    return _kooc_resolution(self, ast, mangler.Mangler(), parents)


@meta.add_method(cnorm.nodes.BlockStmt)
def kooc_resolution(self, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler = mangler.Mangler(),
                    parents: list = list()):
    dellist = []
    for var in vars(self):
        if getattr(self, var) is not None:
            _var = sub_resolution(getattr(self, var), ast, _mangler, parents)
            if _var is None:
                dellist.append(var)
            else:
                setattr(self, var, _var)
    for _del in dellist:
        delattr(self, _del)
    return self


def decl_modifier_in_namespace(decl_node: cnorm.nodes.Decl):
    if hasattr(decl_node, '_ctype') and type(
            decl_node._ctype) is cnorm.nodes.PrimaryType and decl_node._ctype._storage is 0:
        decl_node._ctype._storage = 4
        if hasattr(decl_node, '_assign_expr'):
            del decl_node._assign_expr


@meta.add_method(nodes.Nmspce)
def kooc_resolution(self: nodes.Nmspce, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    global nm
    nm.push(cnorm.nodes.Decl, decl_modifier_in_namespace)
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    _kooc_resolution(self, ast, new_mangler, parents)
    return self.body


@meta.add_method(nodes.Defn)
def kooc_resolution(self: nodes.Defn, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    namespace = ast.search_in_tree(lambda namespace, parents: namespace if isinstance(namespace,
                                                                                      nodes.Nmspce) and namespace.name == self.name and parents == parents else None)
    self.body = namespace.body + self.body
    _kooc_resolution(self, ast, new_mangler, parents)
    return self.body


@meta.add_method(nodes.KoocId)
def kooc_resolution(self: nodes.KoocId, ast: cnorm.nodes.BlockStmt, _manger: mangler.Mangler, parents):
    if len(self.scope) == 0:
        return self
    id_mangler = mangler.Mangler(True)
    id_mangler.name(self.value)
    for container in self.scope:
        id_mangler.container(container)
    self.value = id_mangler.mangle("container", "name")
    return self
