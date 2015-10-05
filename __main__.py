__author__ = 'collio_v'

from kooc import Kooc
from cnorm.passes import to_c

cooker = Kooc()
print(cooker.parse("""
#include "toto.h"
@import(./toto)
""").to_c())