import pyrser

import kooc

__author__ = 'collio_v'

from pyrser.parsing import Node
from pyrser import grammar, meta
from cnorm.parsing.expression import Idset
import cnorm
import nodes


# TODO: verify that contain no function definition
class Namespace(grammar.Grammar):
    entry = "translation_unit"
    grammar = """
        declaration = [
                        __scope__:current_block
                        "@namespace(" id:namespace_name ')'
                        #make_namespace(_, namespace_name, current_block)
                        '{' [ declaration ]* '}'
                        #depile_context(_)
                        ]


        identifier = [  scoped_identifier:>_ ]
        scoped_identifier = [
            @ignore("null") [
                #make_scoped_identifier(_)
                [ #can_scope(current_block) @ignore("C/C++") id:identifier '@' #add_scope(_, identifier) ]*
                id:id #check_id(_, id)
            ]
        ]

        declaration_specifier = [
            [ [ Base.id '@' ]* Base.id ]:i
            #new_decl_spec(local_specifier, i, current_block)
            [
                #is_composed(local_specifier)
                composed_type_specifier
                |
                #is_enum(local_specifier)
                enum_specifier
                |
                #is_typeof(i)
                typeof_expr
            ]?
            |
            attr_asm_decl:attr
            #add_attr_specifier(local_specifier, attr)
        ]

    """

@meta.hook(Namespace)
def make_namespace(self: Namespace, context, namespace_name, current_block) -> bool:
    context.set(nodes.Namespace(self.value(namespace_name)))
    context.types = self.rule_nodes.parents['current_block'].ref.types.new_child()
    current_block.ref = context
    return True


@meta.hook(Namespace)
def depile_context(self: Namespace, context :nodes.Namespace):
    self.rule_nodes.parents['current_block'].ref.body.append(context)
    for value in context.types:
        self.rule_nodes.parents['current_block'].ref.types["{0}@{1}".format(context.name, value)] = context.types[value]
    return True


@meta.hook(Namespace)
def make_scoped_identifier(self: Namespace, context):
    context.set(nodes.KoocId())
    return True


@meta.hook(Namespace)
def add_scope(self: Namespace, context: nodes.KoocId, identifier):
    if not hasattr(context, 'scope'):
        context.scope = []
    context.scope.append(self.value(identifier))
    return True


@meta.hook(Namespace)
def check_id(self: Namespace, context: nodes.KoocId, identifier):
    if len(context.scope) == 0 and self.value(identifier) in Idset:
        return False
    context.value = self.value(identifier)
    return True


@meta.hook(Namespace)
def can_scope(self: Namespace, current_block):
    return not isinstance(current_block.ref, nodes.Class)