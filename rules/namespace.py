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
                [ @ignore("C/C++") id:identifier '@' #add_scope(_, identifier) ]*
                id:id #check_id(_, id)
            ]
        ]
    """


@meta.hook(Namespace)
def make_namespace(self: Namespace, ast, namespace_name, current_block) -> bool:
    ast.set(nodes.Nmspce(self.value(namespace_name)))
    current_block.ref = ast
    return True


@meta.hook(Namespace)
def depile_context(self: Namespace, current_block):
    self.rule_nodes.parents['current_block'].ref.body.append(current_block)
    return True


@meta.hook(Namespace)
def make_scoped_identifier(self: Namespace, context):
    context.set(nodes.KoocId())
    return True

@meta.hook(Namespace)
def add_scope(self: Namespace, context: nodes.KoocId, identifier):
    context.scope.append(self.value(identifier))
    return True

@meta.hook(Namespace)
def check_id(self: Namespace, context : nodes.KoocId, identifier):
    if len(context.scope) == 0 and self.value(identifier) in Idset:
        return False
    context.value = self.value(identifier)
    return True