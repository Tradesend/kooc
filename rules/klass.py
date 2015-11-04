import cnorm
import sys
from pyrser import grammar, meta, parsing
from compiler import error
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes

Accessibility = [
    "public", "private", "protected", "internal"
]


class Klass(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
            declaration = [
                "@class" __scope__:current_block  id:class_name #create_class(_, class_name, current_block)
                '(' ')'
                '{' [ inner_class | ctor | dtor ]* "};" #end_class_definition(_)
            ]
            ctor = [
                __scope__:local_specifier
                "@" !!"constructor"
                #Declaration.create_ctype(local_specifier)
                declarator:decl
                callable:callable
                ';' #create_ctor(decl, current_block, callable)
            ]
            dtor = [
                __scope__:local_specifier
                "@" !!"destructor"
                #Declaration.create_ctype(local_specifier)
                declarator:decl
                callable:callable
                ';' #create_dtor(decl, current_block, callable)
            ]
            inner_class = [
                __scope__:local_specifier
                #Declaration.create_ctype(local_specifier)
                declaration_specifier*:dsp
                declarator:decl
                [
                    access:access #check_attribute(decl, access)
                    |
                    callable:callable #check_method(decl, callable)
                ] ';' #store_declaration(decl, current_block)
            ]
            access = [
                "@property" #create_access(_)
                '('
                    [
                        [
                            "get:" id:access_type #configure_get_access(_, access_type) |
                            "set:" id:access_type #configure_set_access(_, access_type)
                        ] ','
                    ]*
                    [
                        "get:" id:access_type #configure_get_access(_, access_type) |
                        "set:" id:access_type #configure_set_access(_, access_type)
                    ]?
                ')'
            ]
            callable = [
                "@callable" #create_callable(_)
                '('
                     [
                        [
                            [ "static"  #configure_staticity(_)  ] |
                            [ "virtual" #configure_virtuality(_) ] |
                            [ "call:"   id:access_type #configure_call_access(_, access_type) ]
                        ] ','
                    ]*
                    [
                        [ "static"  #configure_staticity(_)  ] |
                        [ "virtual" #configure_virtuality(_) ] |
                        [ "override" #configure_overriding(_) ] |
                        [ "call:"   id:access_type #configure_call_access(_, access_type) ]
                    ]?
                ')'
            ]
        """


@meta.hook(Klass)
def create_class(self: Klass, context, class_name, current_block):
    context.set(nodes.Class(self.value(class_name)))
    current_block.ref = context
    return True


@meta.hook(Klass)
def end_class_definition(self: Klass, context: nodes.Class):
    self.rule_nodes.parents['current_block'].ref.body.append(context)
    self.rule_nodes.parents['current_block'].ref.types[context.class_name] = context
    return True


@meta.hook(Klass)
def create_access(self: Klass, context):
    context.set(nodes.Access())
    return True


@meta.hook(Klass)
def configure_get_access(self: Klass, context: nodes.Access, access_type):
    if self.value(access_type) not in Accessibility:
        print(error.Error("accessibility specification are [{0}]".format(' '.join(Accessibility))), file=sys.stderr)
        return False
    context.get = self.value(access_type)
    return True


@meta.hook(Klass)
def configure_set_access(self: Klass, context: nodes.Access, access_type):
    if self.value(access_type) not in Accessibility:
        print(error.Error("accessibility specification are [{0}]".format(' '.join(Accessibility))), file=sys.stderr)
        return False
    context.set = self.value(access_type)
    return True


@meta.hook(Klass)
def create_callable(self: Klass, context):
    context.set(nodes.Callable())
    return True


@meta.hook(Klass)
def configure_staticity(self: Klass, context: nodes.Callable):
    if context.virtual is True:
        print(error.Error("methodes can not be virtual and static at the same time"), file=sys.stderr)
        return False
    context.static = True
    return True


@meta.hook(Klass)
def configure_virtuality(self: Klass, context: nodes.Callable):
    if context.static is True:
        print(error.Error("methodes can not be virtual and static at the same time"), file=sys.stderr)
        return False
    if context.override is True:
        print(error.Error("methodes can not redifine its own virtuality in case of overriding"))
        return False
    context.virtual = True
    return True


@meta.hook(Klass)
def configure_overriding(self: Klass, context: nodes.Callable):
    if context.static is True:
        print(error.Error("methodes can not override static parents"), file=sys.stderr)
        return False
    if context.virtual is True:
        print(error.Error("methodes can not redifine its own virtuality in case of overriding"))
        return False
    context.override = True
    return True


@meta.hook(Klass)
def configure_call_access(self: Klass, context: nodes.Callable, access_type):
    if self.value(access_type) not in Accessibility:
        print(error.Error("accessibility specification are [{0}]".format(' '.join(Accessibility))), file=sys.stderr)
        return False
    context.access = self.value(access_type)
    return True


@meta.hook(Klass)
def check_attribute(self: Klass, _declaration: cnorm.nodes.Decl, accessibility):
    if type(_declaration._ctype) is not cnorm.nodes.PrimaryType:
        print(error.Error("@access is the accessibility definition for attribute"), file=sys.stderr)
        return False
    _declaration.set(nodes.Attribute(_declaration, accessibility))
    return True


@meta.hook(Klass)
def check_method(self: Klass, _declaration: cnorm.nodes.Decl, accessibility):
    if type(_declaration._ctype) is not cnorm.nodes.FuncType:
        print(error.Error("@callable is the accessibility definition for methode"), file=sys.stderr)
        return False
    _declaration.set(nodes.Method(_declaration, accessibility))
    return True


@meta.hook(Klass)
def store_declaration(self: Klass, _declaration, current_block):
    current_block.ref._ctype.fields.append(_declaration)
    return True


@meta.hook(Klass)
def create_ctor(self: Klass, _declaration: cnorm.nodes.Decl, current_block, accessibility: nodes.Callable):
    if accessibility.static is True:
        print(error.Error("constructor cannot be static"), file=sys.stderr)
        return False
    if accessibility.virtual is True:
        print(error.Error("constructor cannot be virtual"), file=sys.stderr)
        return False
    current_block.ref._ctype.fields.append(nodes.Constructor(_declaration, accessibility))
    return True


@meta.hook(Klass)
def create_dtor(self: Klass, _declaration: cnorm.nodes.Decl, current_block, accessibility: nodes.Callable):
    if accessibility.static is True:
        print(error.Error("destructor cannot be static"), file=sys.stderr)
        return False
    if len(_declaration._ctype.params):
        print(error.Error("destructor cannot have parameters"), file=sys.stderr)
        return False
    current_block.ref._ctype.fields.append(nodes.Destructor(_declaration, accessibility))
    return True
