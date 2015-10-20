__author__ = 'collio_v'

from pyrser.parsing import Node
from pyrser import grammar, meta
import nodes


class Definition(grammar.Grammar):
    entry = "translation_unit"
    grammar = """
            declaration = [
                "@definition(" id:definition_name ")"
                #make_definition(definition_name, current_block)
                '{' [ declaration ]* '}'
                #depile_context(current_block)
            ]
        """


@meta.hook(Definition)
def make_definition(self: Definition, definition_name, current_block) -> bool:
    if not hasattr(current_block, 'pile'):
        current_block.pile = []
    current_block.pile.insert(0, current_block.ref)
    current_block.ref = nodes.Defn(self.value(definition_name))
    return True


@meta.hook(Definition)
def depile_context(self: Definition, current_block):
    current_block.ref.types = [_key for _key, _value in current_block.ref.types.items()]
    current_block.pile[0].body.append(current_block.ref)
    current_block.ref = current_block.pile[0]
    current_block.pile = current_block.pile[1:len(current_block.pile)]
    return True
