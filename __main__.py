__author__ = 'collio_v'

from rules import importing
from kooc import Kooc
from cnorm.passes import to_c
from cnorm import nodes

cooker = Kooc()
print(cooker.parse("""
#include "toto.h"
@import(./toto)
""").to_c())