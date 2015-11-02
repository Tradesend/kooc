import sys
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
                self.heap_dictionary[key].append(self.dictionary[key])
            else:
                self.heap_dictionary[key] = [self.dictionary[key]]
        self.dictionary[key] = mod

    def pop(self, key):
        if key in self.heap_dictionary:
            self.dictionary[key] = self.heap_dictionary[key].pop()
            if not len(self.heap_dictionary[key]):
                del self.heap_dictionary[key]
        else:
            self.dictionary.pop(key)

    def use(self, obj):
        if type(obj) in self.dictionary:
            return self.dictionary[type(obj)](obj)
        return True


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
    self.imported = kooc.Kooc().parse_file('{0}.kh'.format(self.value))
    ret = self.imported.search_in_tree(predicate)
    if ret is None:
        ret = node.Node.search_in_tree(self, predicate, parents)
    return ret


@meta.add_method(node.Node)
def kooc_resolution(self, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler = mangler.Mangler(),
                    parents: list = list()):
    global nm
    if not nm.use(self):
        return None
    return _kooc_resolution(self, ast, mangler.Mangler(), parents)


def identifier_mangling(identifier: str):
    new_mangler = mangler.Mangler(True)
    scopes = identifier.split('@')
    name = scopes.pop()
    for scope in scopes:
        new_mangler.container(scope)
    new_mangler.type_definition()
    return new_mangler.name(name).mangle()


@meta.add_method(cnorm.nodes.Decl)
def kooc_resolution(self: cnorm.nodes.Decl, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    res = node.Node.kooc_resolution(self, ast, _mangler, parents)
    if res is not None:
        if hasattr(res, '_ctype'):
            if res._ctype._storage == 0:
                _mangler.type(res._ctype._identifier)
                if hasattr(res._ctype, '_params'):
                    _mangler.callable().params(res._ctype._params)
            elif res._ctype._storage == 2 or res._ctype._storage == 1:
                _mangler.type_definition()
            if '@' in res._ctype._identifier:
                res._ctype._identifier = identifier_mangling(res._ctype._identifier)
        self._name = _mangler.name(self._name).mangle()
    return res


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
    return True


@meta.add_method(nodes.Namespace)
def kooc_resolution(self: nodes.Namespace, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    global nm
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    nm.push(cnorm.nodes.Decl, decl_modifier_in_namespace)
    _kooc_resolution(self, ast, new_mangler, parents)
    nm.pop(cnorm.nodes.Decl)
    return self.body


@meta.add_method(nodes.Defn)
def kooc_resolution(self: nodes.Defn, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    namespace = ast.search_in_tree(lambda namespace, parents: namespace if isinstance(namespace,
                                                                                      nodes.Namespace) and namespace.name == self.name and parents == parents else None)
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
    self.value = id_mangler.mangle()
    return self


def make_vtable(klass: nodes.Class, name: str, _mangler: mangler.Mangler):
    vtable_mangler = copy.copy(_mangler)
    res = cnorm.nodes.Decl('', cnorm.nodes.ComposedType('__5vtable' + name))
    res._ctype.fields = []
    res._ctype._specifier = 1
    for declaration in klass._ctype.fields:
        if type(declaration) is not nodes.Attribute and declaration.accessibility.virtual is True:
            _declaration_pointer = cnorm.nodes.Decl(
                vtable_mangler.name(declaration._name).type(declaration._ctype._identifier).params(
                    declaration._ctype._params).callable().mangle(),
                cnorm.nodes.PrimaryType(declaration._ctype._identifier))
            _declaration_pointer._ctype._decltype = cnorm.nodes.PointerType()
            _declaration_pointer._ctype._decltype._decltype = cnorm.nodes.ParenType(declaration._ctype._params)
            res._ctype.fields.append(_declaration_pointer)
    return res


@meta.add_method(nodes.Class)
def kooc_resolution(self: nodes.Class, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self._ctype._identifier)

    global nm
    nm.push(nodes.Destructor, lambda destructor: False)
    nm.push(nodes.Constructor, lambda destructor: False)
    nm.push(nodes.Method, lambda destructor: False)

    self._ctype._identifier = _mangler.name(self._ctype._identifier).type_definition().mangle()
    vtable = make_vtable(self, self._ctype._identifier, new_mangler)

    method_mangler = copy.copy(new_mangler)
    methods_declaration = []
    for method in self._ctype.fields:
        if type(method) is nodes.Method:
            method._name = method_mangler.name(method._name).callable().mangle()
            methods_declaration.append(method)

    self._ctype.fields = sub_resolution(self._ctype.fields, ast, new_mangler, parents)

    nm.pop(nodes.Destructor)
    nm.pop(nodes.Constructor)
    nm.pop(nodes.Method)

    return methods_declaration + [vtable, self]


def verify_parameters(l1: list, l2: list):
    for x in range(len(l1)):
        if l1[x]._ctype._identifier != l2[x]._ctype._identifier:
            return False
    return True


@meta.add_method(nodes.Impl)
def kooc_resolution(self: nodes.Impl, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    impl_mangler = copy.copy(_mangler)
    impl_mangler.enable()
    impl_mangler.container(self.name)

    klass = ast.search_in_tree(lambda klass, parents: klass if type(klass) is nodes.Class
                                                               and klass.class_name == self.name
                                                               and parents == parents else None,
                               parents)
    for methodImpl in self.body:
        methodDef = next((method for method in klass._ctype.fields if type(method) is nodes.Method
                          and method._name == methodImpl._name
                          and method._ctype._identifier == methodImpl._ctype._identifier
                          and len(method._ctype.params) == len(methodImpl._ctype.params)
                          and verify_parameters(method._ctype.params, methodImpl._ctype.params)), None)
        if methodDef is None:
            del methodImpl.body
            print("No matching definition for method: ", methodImpl.to_c(), "in class:", self.name, file=sys.stderr)
            exit(0)
        methodDef.defined = True
    return sub_resolution(self.body, ast, impl_mangler, parents)
