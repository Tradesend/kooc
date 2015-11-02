__author__ = 'collio_v'

import copy
import os, sys
from kooc import Kooc
from compiler import information
from cnorm.parsing.expression import Idset
from cnorm.passes import to_c
from ast import resolution

cooker = Kooc()

filename = os.path.abspath(sys.argv[1])
os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
information.File.name = sys.argv[1]
res = cooker.parse_file(filename)
Idset['class'] = "specifier_block"

print(res.to_yml())
print(res.kooc_resolution(copy.deepcopy(res)).to_c())
