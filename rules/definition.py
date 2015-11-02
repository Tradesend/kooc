__author__ = 'collio_v'

from pyrser.parsing import Node
from pyrser import grammar, meta
import nodes


class Definition(grammar.Grammar):
    entry = "translation_unit"
    grammar = """
            declaration = [
                "@definition("
                __scope__:current_block
                #make_definition(_, current_block)
                 id:definition_name ")"
                #name_definition(_, definition_name)
                '{' [ declaration ]* '}'
                #depile_defn_context(_)
            ]
        """


@meta.hook(Definition)
def make_definition(self: Definition, ast, current_block) -> bool:
    ast.set(nodes.Defn(self.value("")))
    current_block.ref = ast
    return True


@meta.hook(Definition)
def name_definition(self: Definition, ast: nodes.Defn, definition_name) -> bool:
    ast.name = self.value(definition_name)
    return True


@meta.hook(Definition)
def depile_defn_context(self: Definition, context):
    self.rule_nodes.parents['current_block'].ref.body.append(context)
    return True
