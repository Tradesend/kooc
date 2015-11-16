#!/usr/bin/python3

__author__ = 'collio_v'

import copy
import os, sys
from kooc import Kooc
from compiler import information
from cnorm.parsing.expression import Idset
from cnorm.passes import to_c
from cnorm.nodes import Raw
from ast import resolution

cooker = Kooc()

if len(sys.argv) < 2:
    sys.exit("Please specify a file")

filename = os.path.abspath(sys.argv[1])
if not os.path.isfile(filename):
    sys.exit("Couldn't find specified file in : " + filename)
os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
information.File.name = sys.argv[1]
res = cooker.parse_file(filename)
res.body.insert(0, Raw('#include <stdlib.h>\n'))
Idset['class'] = "specifier_block"

print(res.kooc_resolution(copy.deepcopy(res)).to_c())
