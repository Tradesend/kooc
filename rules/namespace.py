__author__ = 'collio_v'

from pyrser.parsing import Node
from pyrser import grammar, meta
import nodes


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
