__author__ = 'collio_v'

from rules import importing

cooker = importing.Import()
print(cooker.parse("""
#include "toto.h"
@import(toto)
"""))