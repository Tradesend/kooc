
__author__ = 'collio_v'

import sys
from kooc import Kooc
from compiler import information
from cnorm.passes import to_c
from ast import resolution

cooker = Kooc()

information.File.name = "test.kc"
res = cooker.parse("""
@namespace(toto){
    @namespace(titi) {
        int main();
    }
}
""")

res.kooc_resolution(res)