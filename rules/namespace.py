from pyrser.parsing import Node

__author__ = 'collio_v'

from pyrser import grammar, meta
import nodes


class Namespace(grammar.Grammar):
    entry = "trnaslation_unit"
    grammar = """
        declaration = [
                        "@namespace(" id:namespace_name ')'
                        #make_namespace(namespace_name, current_block)
                        '{' declaration '}'
                        #depile_context(current_block)
                        ]
    """


@meta.hook(Namespace)
def make_namespace(self: Namespace, namespace_name, current_block) -> bool:
    if not hasattr(current_block, 'pile'):
        current_block.pile = []
    current_block.pile.insert(0, current_block.ref)
    current_block.ref = nodes.Nmspce(self.value(namespace_name))
    return True


@meta.hook(Namespace)
def depile_context(self: Namespace, current_block):
    current_block.pile[0].body.append(current_block.ref)
    current_block.ref = current_block.pile[0]
    current_block.pile = current_block.pile[1:len(current_block.pile)]
    print(current_block.to_yml())
    return True
