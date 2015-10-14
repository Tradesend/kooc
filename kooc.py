__author__ = 'collio_v'

from rules import importing, namespace
from cnorm.parsing import declaration
from pyrser import grammar


class Kooc(grammar.Grammar, importing.Import, namespace.Namespace, declaration.Declaration):
    entry = "translation_unit"
    grammar = """
        declaration = [ Declaration.declaration | Namespace.declaration ]
    """
    pass
