__author__ = 'collio_v'

from rules import importing, namespace, definition, klass, koperands, implementation
from cnorm.parsing import declaration
from pyrser import grammar


ScopedKeywords = [
    'access', 'set', 'get', 'new', 'delete'
]

class Kooc(grammar.Grammar,
           importing.Import,
           klass.Klass, implementation.Implementation,
           namespace.Namespace, definition.Definition,
           koperands.Koperands,
           declaration.Declaration):
    entry = "translation_unit"
    grammar = """
        declaration = [
                Declaration.declaration | Namespace.declaration |
                Definition.declaration | Klass.declaration |
                Implementation.declaration
                ]
        identifier = [ Namespace.identifier:>_ ]
    """
    pass
