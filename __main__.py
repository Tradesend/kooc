
__author__ = 'collio_v'

import sys
from kooc import Kooc
from compiler import information
from cnorm.passes import to_c
from ast import resolution

cooker = Kooc()

information.File.name = "test.kc"
res = cooker.parse("""
typedef int toto;
@namespace(toto){
    @namespace(titi) {
        int main();
    }
    int main();
    typedef int toto;
}
""")

print(res.kooc_resolution(res))