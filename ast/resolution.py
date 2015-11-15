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


@meta.add_method(cnorm.nodes.RootBlockStmt)
def search_in_tree(self, predicate: callable, parents: list = list()):
    return node.Node.search_in_tree(self, predicate, [])


@meta.add_method(node.Node)
def search_in_tree(self, predicate: callable, parents: list = list()):
    if predicate(self, parents):
        return self

    if type(self) in [nodes.Class, nodes.Impl, nodes.Namespace, nodes.Defn]:
        if hasattr(self, 'name'):
            parents.append(self.name)
        else:
            parents.append(self.class_name)

    for var in vars(self):
        _var = sub_search_in_tree(getattr(self, var), predicate, parents)
        if _var is not None:
            return _var

    if type(self) in [nodes.Class, nodes.Impl, nodes.Namespace, nodes.Defn]:
        parents.pop()
    return None


@meta.add_method(nodes.Imp)
def search_in_tree(self: nodes.Imp, predicate: callable, parents: list = list()):
    self.imported = kooc.Kooc().parse_file('{0}.kh'.format(self.value))
    ret = self.imported.search_in_tree(predicate)
    if ret is None:
        ret = node.Node.search_in_tree(self, predicate, [])
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
    parents.append(self.name)
    _kooc_resolution(self, ast, new_mangler, parents)
    parents.pop()
    nm.pop(cnorm.nodes.Decl)
    return self.body


@meta.add_method(nodes.Defn)
def kooc_resolution(self: nodes.Defn, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    namespace = ast.search_in_tree(lambda namespace, _parents: namespace if isinstance(namespace,
                                                                                       nodes.Namespace) and namespace.name == self.name and parents == _parents else None)
    self.body = [declaration for declaration in namespace.body if hasattr(declaration, '_assign_expr')] + self.body

    parents.append(self.name)
    array = sub_resolution(self.body, ast, new_mangler, parents)
    parents.pop()

    return array


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


def make_vtable(klass: nodes.Class, name: str, _mangler: mangler.Mangler, _this: cnorm.nodes.Decl, parents: list, ast):
    vtable_mangler = copy.deepcopy(_mangler)
    vtable_mangler.container(klass.class_name)
    res = cnorm.nodes.Decl('', cnorm.nodes.ComposedType('__6vtable' + name))
    res._ctype.fields = []
    res._ctype._specifier = 1
    for declaration in klass._ctype.fields:
        if type(declaration) is not nodes.Attribute and declaration.accessibility.virtual is True:
            _declaration_pointer = cnorm.nodes.Decl(
                vtable_mangler.name(declaration._name).type(declaration._ctype._identifier).params(
                    declaration._ctype._params).callable().mangle(),
                cnorm.nodes.PrimaryType(declaration._ctype._identifier))
            _declaration_pointer._ctype._decltype = cnorm.nodes.PointerType()
            _declaration_pointer._ctype._decltype._decltype = cnorm.nodes.ParenType(
                [_this] + declaration._ctype._params)
            res._ctype.fields.append(_declaration_pointer)
    if len(parents):
        self = parents[0]
        super_supers = []
        for parent_name in self.parents:
            _parent = ast.search_in_tree(lambda super, _parents:
                                             super if type(super) is nodes.Class
                                                      and super.class_name == parent_name.value
                                                      and _parents == parent_name.scope else None)
            if _parent is None:
                print("error: super class of " + self.class_name + " named " + '@'.join(parent_name.scope + [parent_name.value]) + " doesn't exist", file=sys.stderr)
                exit(-1)
            super_supers.append(_parent)
        _super_this = cnorm.nodes.Decl('', cnorm.nodes.PrimaryType(_mangler.name(klass.class_name).type_definition().mangle()))
        res._ctype.fields += make_vtable(parents[0], _mangler.class_definition().name(klass.class_name).mangle(), _mangler, _super_this, super_supers, ast)[0]._ctype.fields
    _typedef = cnorm.nodes.Decl('__6vtable' + _mangler.type_definition().name(klass.class_name).mangle(),
                                cnorm.nodes.ComposedType(res._ctype._identifier))
    _typedef._ctype._decltype = cnorm.nodes.PointerType()
    _typedef._ctype._specifier = 1
    _typedef._ctype._storage = 2

    return [res, _typedef]


@meta.add_method(nodes.Class)
def kooc_resolution(self: nodes.Class, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    new_mangler.container(self._ctype._identifier)

    global nm
    nm.push(nodes.Destructor, lambda destructor: False)
    nm.push(nodes.Constructor, lambda destructor: False)
    nm.push(nodes.Method, lambda destructor: False)

    supers = []
    for parent_name in self.parents:
        _parent = ast.search_in_tree(lambda super, _parents:
                                         super if type(super) is nodes.Class
                                                  and super.class_name == parent_name.value
                                                  and _parents == parent_name.scope else None)
        if _parent is None:
            print("error: super class of " + self.class_name + " named " + '@'.join(parent_name.scope + [parent_name.value]) + " doesn't exist", file=sys.stderr)
            exit(-1)
        supers.append(_parent)

    self._ctype._identifier = _mangler.name(self._ctype._identifier).class_definition().mangle()
    _this = cnorm.nodes.Decl('', cnorm.nodes.PrimaryType(_mangler.type_definition().mangle()))
    vtable = make_vtable(self, self._ctype._identifier, _mangler, _this, supers, ast)

    _typedef = cnorm.nodes.Decl(_mangler.type_definition().mangle(), cnorm.nodes.ComposedType(self._ctype._identifier))
    _typedef._ctype._decltype = cnorm.nodes.PointerType()
    _typedef._ctype._specifier = 1
    _typedef._ctype._storage = 2

    method_mangler = copy.copy(new_mangler)
    methods_declaration = []
    for method in self._ctype.fields:
        if type(method) is nodes.Method:
            method._ctype._params = [_this] + method._ctype._params
            if method.accessibility.virtual is True:
                virtual = copy.deepcopy(method)
                method_mangler._symtype = "__7virtual"
                virtual._name = method_mangler.name(method._name).params(virtual._ctype._params).mangle()
                methods_declaration.append(virtual)
            method._name = method_mangler.name(method._name).callable().params(method._ctype._params).mangle()
            methods_declaration.append(method)
        elif type(method) is nodes.Constructor:
            newer = copy.deepcopy(method)
            method._ctype._params = [_this, cnorm.nodes.Decl('', cnorm.nodes.PrimaryType(
                vtable[1]._name))] + method._ctype._params
            method._name = method_mangler.name(method._name).callable().params(method._ctype._params).mangle()
            newer._name = method_mangler.name("new").params(newer._ctype._params).mangle()
            newer._ctype._identifier = _typedef._name;
            methods_declaration.append(method)
            methods_declaration.append(newer)
        elif type(method) is nodes.Destructor:
            newer = copy.deepcopy(method)
            method._ctype._params = [_this] + method._ctype._params
            if method.accessibility.virtual is True:
                virtual = copy.deepcopy(method)
                method_mangler._symtype = "__7virtual"
                virtual._name = method_mangler.name(method._name).mangle()
                methods_declaration.append(virtual)
            method._name = method_mangler.name(method._name).callable().params(method._ctype._params).mangle()
            newer._name = method_mangler.name("delete").mangle()
            methods_declaration.append(method)
            methods_declaration.append(newer)

    self._ctype.fields = sub_resolution(self._ctype.fields, ast, new_mangler, parents)
    for _super in reversed(supers):
        res = copy.deepcopy(_super).kooc_resolution(ast, _mangler, parents)
        self._ctype.fields = res[-1]._ctype.fields + self._ctype.fields
        self._ctype.fields.insert(0, cnorm.nodes.Decl('__6vtable__' + str(len(_super.class_name)) + _super.class_name, cnorm.nodes.PrimaryType(res[1]._ctype._identifier)))
    nm.pop(nodes.Destructor)
    nm.pop(nodes.Constructor)
    nm.pop(nodes.Method)

    return [_typedef, vtable[1]] + methods_declaration + [vtable[0]] + [self]


def verify_parameters(l1: list, l2: list):
    for x in range(len(l1)):
        if l1[x]._ctype._identifier != l2[x]._ctype._identifier:
            return False
    return True


def construct_delete_operator(methodDef: nodes.Destructor, methodImpl: nodes.DestructorImplementation,
                              _this: cnorm.nodes.Decl,
                              impl_mangler: mangler.Mangler):
    new_operator_mangler = copy.copy(impl_mangler)
    ret = cnorm.nodes.Decl('delete', copy.deepcopy(methodImpl._ctype))
    ret._ctype._identifier = _this._ctype._identifier
    new_gen = kooc.Kooc()
    ret.body = kooc.Kooc().parse("""
        void delete() {
            """ + new_operator_mangler.name(methodDef._name).callable().type('void').params(
        methodImpl._ctype._params).mangle() + "({0})".format(
        ', '.join([decl._name for decl in methodImpl._ctype._params])
    ) + """;
        free(this);
        free(((void*)this - sizeof(void*)));
        }
    """).body[0].body
    return ret


def construct_new_operator(methodDef: nodes.Constructor, methodImpl: nodes.ConstructorImplementation,
                           _this: cnorm.nodes.Decl,
                           impl_mangler: mangler.Mangler):
    new_operator_mangler = copy.copy(impl_mangler)
    ret = cnorm.nodes.Decl('new', copy.deepcopy(methodDef._ctype))
    ret._ctype._identifier = _this._ctype._identifier
    new_gen = kooc.Kooc()
    ret.body = kooc.Kooc().parse("""
        int new() {
            int this;
            int vtable;
            this = sizeof(void*) + malloc(sizeof(void*) + sizeof(*this));
            vtable = ((void*)this) - sizeof(void*);
            vtable = malloc(sizeof(*vtable));
            """ + new_operator_mangler.name(methodDef._name).callable().type('void').params(
        methodImpl._ctype._params).mangle() + "({0})".format(
        ', '.join([decl._name for decl in methodImpl._ctype._params])
    ) + """;
            return this;
        }
    """).body[0].body
    ret.body.body[0]._ctype._identifier = _this._ctype._identifier
    ret.body.body[1]._ctype._identifier = '__6vtable' + _this._ctype._identifier
    return ret


def fill_constructor(constructor: nodes.ConstructorImplementation, klass: nodes.Class,
                     vtable_init_mangler: mangler.Mangler, _this, _override_table: dict):
    inner_vtable_init_for_virtuality = [virtual for virtual in klass._ctype.fields if
                                        type(virtual) is nodes.Method and
                                        virtual.accessibility.virtual is True]
    inner_vtable_init_for_virtuality_stringified = '\n'.join(["vtable->{0} = &{1};".format(
        vtable_init_mangler.callable().params([_this] + virtual._ctype._params).type(
            virtual._ctype._identifier).name(virtual._name).mangle(),
        vtable_init_mangler.virtual().params([_this] + virtual._ctype._params).name(virtual._name).type(
            virtual._ctype._identifier).mangle()
    ) for virtual in inner_vtable_init_for_virtuality])

    for key, methods in _override_table.items():
        if key is 0:
            inner_vtable_init_for_virtuality_stringified += '\n'.join(["vtable->{0} = &{1};".format(
                vtable_init_mangler.callable().params([_this] + override._ctype._params).type(
                    override._ctype._identifier).name(override._name).mangle(),
                vtable_init_mangler.callable().params([_this] + override._ctype._params).name(override._name).type(
                    override._ctype._identifier).mangle()
            ) for override in methods])
        else:
            inner_vtable_init_for_virtuality_stringified += '\n'.join(["this->parent_{2}_vtable.{0} = &{1};".format(
                vtable_init_mangler.callable().params([_this] + override._ctype._params).type(
                    override._ctype._identifier).name(override._name).mangle(),
                vtable_init_mangler.virtual().params([_this] + override._ctype._params).name(override._name).type(
                    override._ctype._identifier).mangle(), key
            ) for override in methods])

    constructor.body.body = kooc.Kooc().parse("int main() {" + inner_vtable_init_for_virtuality_stringified + "}").body[
                                0].body.body + constructor.body.body
    pass


def generate_override_table(self: nodes.Impl, klass: nodes.Class, ast, methods_pair: dict):
    _override_table = {}
    supers = []
    for parent_name in klass.parents:
        supers.append(ast.search_in_tree(lambda __super, _parents:
                                         __super if type(__super) is nodes.Class
                                                    and __super.class_name == parent_name.value
                                                    and _parents == parent_name.scope else None))
    for methodImpl in self.body:
        if methods_pair[methodImpl._name].accessibility.override is True:
            for it, _super in enumerate(supers):
                for methodDef in _super._ctype.fields:
                    if it not in _override_table:
                        _override_table[it] = []
                    _override_table[it].append(methodImpl)
    return _override_table


@meta.add_method(nodes.MethodImplementation)
def kooc_resolution(self: nodes.MethodImplementation, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler,
                    parents: list):
    if hasattr(self, 'virtual'):
        self._name = _mangler.virtual().name(self._name).mangle()
        _callable = (kooc.Kooc().parse("""int main() {
            int vtable = ((void*)this) - 8;
            return (double)(vtable->""" + _mangler.callable().mangle() + """)(""" + ', '.join(
            [p._name for p in self._ctype._params]) + """);
        }""")).body[0]
        _callable._name = _mangler.callable().mangle()
        _callable._ctype._params = self._ctype._params
        _callable._ctype._identifier = self._ctype._identifier
        _callable.body.body[1].expr.params[0]._identifier = self._ctype._identifier
        _callable.body.body[0]._ctype._identifier = '__6vtable' + self._ctype._params[0]._ctype._identifier
        return [self, _callable]
    else:
        self._name = _mangler.callable().name(self._name).mangle()
        return self


@meta.add_method(nodes.DestructorImplementation)
def kooc_resolution(self: nodes.MethodImplementation, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler,
                    parents: list):
    if hasattr(self, 'virtual'):
        self._name = _mangler.virtual().name(self._name).mangle()
        _callable = (kooc.Kooc().parse("""int main() {
            int vtable = ((void*)this) - 8;
            return (double)(vtable->""" + _mangler.callable().mangle() + """)(""" + ', '.join(
            [p._name for p in self._ctype._params]) + """);
        }""")).body[0]
        _callable._name = _mangler.callable().mangle()
        _callable._ctype._params = self._ctype._params
        _callable._ctype._identifier = self._ctype._identifier
        _callable.body.body[1].expr.params[0]._identifier = self._ctype._identifier
        _callable.body.body[0]._ctype._identifier = '__6vtable' + self._ctype._params[0]._ctype._identifier
        return [self, _callable]
    else:
        self._name = _mangler.callable().name(self._name).mangle()
        return self


@meta.add_method(nodes.Impl)
def kooc_resolution(self: nodes.Impl, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    impl_mangler = copy.copy(_mangler)
    impl_mangler.enable()

    klass = ast.search_in_tree(lambda klass, _parents: klass if type(klass) is nodes.Class
                                                                and klass.class_name == self.name
                                                                and parents == _parents else None)

    if klass is None:
        print("error: klass implementation: ", self.name, " doesn't match any declaration", file=sys.stderr)
        exit(0)

    _this = cnorm.nodes.Decl('this', cnorm.nodes.PrimaryType(
        impl_mangler.name(klass._ctype._identifier).type_definition().mangle()))
    _vtable = cnorm.nodes.Decl('vtable', cnorm.nodes.PrimaryType(
        '__6vtable' + impl_mangler.name(klass._ctype._identifier).type_definition().mangle()))

    methods_pair = {}
    for pos, methodImpl in enumerate(self.body):
        methodDef = None
        if type(methodImpl) is nodes.MethodImplementation:
            methodDef = next((method for method in klass._ctype.fields if (type(method) is nodes.Method)
                              and method._name == methodImpl._name
                              and method._ctype._identifier == methodImpl._ctype._identifier
                              and len(method._ctype.params) == len(methodImpl._ctype.params)
                              and verify_parameters(method._ctype.params, methodImpl._ctype.params)), None)
        elif type(methodImpl) is nodes.ConstructorImplementation:
            methodDef = next((method for method in klass._ctype.fields if (type(method) is nodes.Constructor)
                              and method._name == methodImpl._name
                              and method._ctype._identifier == methodImpl._ctype._identifier
                              and len(method._ctype.params) == len(methodImpl._ctype.params)
                              and verify_parameters(method._ctype.params, methodImpl._ctype.params)), None)
        elif type(methodImpl) is nodes.DestructorImplementation:
            methodDef = next((method for method in klass._ctype.fields if (type(method) is nodes.Destructor)))

        if methodDef is None:
            del methodImpl.body
            print("error: No matching definition for method: ", str(methodImpl.to_c()).strip('\n'), "in class: ",
                  self.name,
                  file=sys.stderr)
            exit(0)

        methods_pair[methodImpl._name] = methodDef

    _override_table = generate_override_table(self, klass, ast, methods_pair)

    generated_function = []
    impl_mangler.container(self.name)

    for pos, methodImpl in enumerate(self.body):
        methodImpl._ctype._params.insert(0, _this)

        if type(methods_pair[methodImpl._name]) is nodes.Constructor:
            methodImpl._ctype._params.insert(1, _vtable)
            generated_function.append(
                construct_new_operator(methods_pair[methodImpl._name], methodImpl, _this, impl_mangler))
            fill_constructor(methodImpl, klass, copy.copy(impl_mangler), _this, _override_table)
        if type(methods_pair[methodImpl._name]) is nodes.Destructor:
            methodImpl._ctype._params.insert(1, _vtable)
            generated_function.append(
                construct_delete_operator(methods_pair[methodImpl._name], methodImpl, _this, impl_mangler))
        if type(methods_pair[methodImpl._name]) is nodes.Method and (methods_pair[
                                                                         methodImpl._name].accessibility.virtual is True):
            methodImpl.virtual = True
        if type(methods_pair[methodImpl._name]) is nodes.Destructor and (methods_pair[
                                                                             methodImpl._name].accessibility.virtual is True):
            methodImpl.virtual = True

        methods_pair[methodImpl._name].defined = True

    for method in klass._ctype.fields:
        if not hasattr(method, 'defined') or method.defined is not True:
            if type(method) is nodes.Constructor:
                print("error: cons", str(method.to_c()).split("void cons")[1].strip('\n'),
                      " declared but not defined in class: ", self.name, sep='', file=sys.stderr)
                exit(0)
            elif type(method) is nodes.Destructor:
                print("error: dest", str(method.to_c()).split("void dest")[1].strip('\n'),
                      " declared but not defined in class: ", self.name, sep='', file=sys.stderr)
                exit(0)
            elif type(method) is nodes.Method:
                print("warning: undefined method: ", str(method.to_c()).strip('\n'), " in class: ",
                      self.name, file=sys.stderr)

    return sub_resolution(self.body + generated_function, ast, impl_mangler, parents)


@meta.add_method(nodes.New)
def kooc_resolution(self: nodes.New, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    new_mangler = copy.copy(_mangler)
    for name in self._type.split('@'):
        new_mangler.container(name)
    new_mangler.enable()
    self.call_expr.value = new_mangler.name('new').callable().mangle()
    return self


@meta.add_method(nodes.Delete)
def kooc_resolution(self: nodes.New, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    new_mangler = copy.copy(_mangler)
    for name in self._type.split('@'):
        new_mangler.container(name)
    new_mangler.enable()
    self.call_expr.value = new_mangler.name('delete').callable().mangle()
    return self


@meta.add_method(nodes.Call)
def kooc_resolution(self: nodes.New, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    new_mangler = copy.copy(_mangler)
    new_mangler.enable()
    for name in self._type.split('@')[:-2]:
        new_mangler.container(name)
    cast = cnorm.nodes.Cast(cnorm.nodes.Raw('()'),
                            [cnorm.nodes.PrimaryType(
                                new_mangler.name(self._type.split('@')[-2]).type_definition().mangle()),
                             self.params[0]])
    self.params[0] = cast
    for name in self._type.split('@')[:-1]:
        new_mangler.container(name)
    self.call_expr.value = new_mangler.name(self._type.split('@')[-1]).callable().mangle()
    return self


@meta.add_method(nodes.Set)
def kooc_resolution(self: nodes.New, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    new_mangler = copy.copy(_mangler)
    for name in self._type.split('@')[:-1]:
        new_mangler.container(name)
    new_mangler.enable()

    attribute = ast.search_in_tree(lambda attribute, _parents: attribute if type(attribute) is nodes.Attribute
                                                                            and attribute._name ==
                                                                                self._type.split('@')[-1]
                                                                            and _parents == self._type.split('@')[
                                                                                            :-1] else None)
    if attribute is None:
        print("error: no attribute: ", self._type.split('@')[-1], " declared in class:",
              '@'.join(self._type.split('@')[:-1]), file=sys.stderr)
        exit(-1)

    if attribute.accessibility.set == 'private' and parents != self._type.split('@')[:-1]:
        print("error: access to attribute: ", self._type.split('@')[-1], " declared in class:",
              '@'.join(self._type.split('@')[:-1]), " which is private", file=sys.stderr)

    self.expr.params[0].params[0].value = new_mangler.name(self._type.split('@')[-1]).variable().mangle()
    return self


@meta.add_method(nodes.Get)
def kooc_resolution(self: nodes.New, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler, parents: list):
    new_mangler = copy.copy(_mangler)
    for name in self._type.split('@')[:-1]:
        new_mangler.container(name)
    new_mangler.enable()

    attribute = ast.search_in_tree(lambda attribute, _parents: attribute if type(attribute) is nodes.Attribute
                                                                            and attribute._name ==
                                                                                self._type.split('@')[-1]
                                                                            and _parents == self._type.split('@')[
                                                                                            :-1] else None)
    if attribute is None:
        print("error: no attribute: ", self._type.split('@')[-1], " declared in class:",
              '@'.join(self._type.split('@')[:-1]), file=sys.stderr)
        exit(-1)

    if attribute.accessibility.get == 'private' and parents != self._type.split('@')[:-1]:
        print("error: access to attribute: ", self._type.split('@')[-1], " declared in class:",
              '@'.join(self._type.split('@')[:-1]), " which is private", file=sys.stderr)
        exit(-1)

    self.expr.params[0].value = new_mangler.name(self._type.split('@')[-1]).variable().mangle()
    return self
