__author__ = 'collio_v'

from rules.importing import Import
from cnorm.parsing import declaration
from pyrser import grammar


class Kooc(grammar.Grammar, Import, declaration.Declaration):
    entry = "translation_unit"
    pass
