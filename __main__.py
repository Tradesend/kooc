__author__ = 'collio_v'

from kooc import Kooc
from cnorm.passes import to_c

cooker = Kooc()
print(cooker.parse("""
@namespace(toto){
    @namespace(titi) {
        int main();
    }
}
""").to_yml())