
__author__ = 'collio_v'

import os, sys
from kooc import Kooc
from compiler import information
from cnorm.passes import to_c
from ast import resolution

cooker = Kooc()

os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
information.File.name = sys.argv[1]
res = cooker.parse_file(sys.argv[1])

print(res)
print(res.kooc_resolution(res).to_c())
