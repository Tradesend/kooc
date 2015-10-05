__author__ = 'collio_v'

from rules.importing import Import
from pyrser import grammar


class Kooc(grammar.Grammar, Import):
    entry = "translation_unit"
    pass
