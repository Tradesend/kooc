import cnorm
import sys
from pyrser import grammar, meta, parsing
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes
import kooc


class Import(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
        preproc_decl = [ kooc_import | Declaration.preproc_decl ]
        kooc_import = [ "@import" @ignore("null") import_directive:filename
                        #validate_import(_, current_block, filename) ]
    """


@meta.rule(Import, "import_directive")
def import_directive(self: Import) -> bool:
    self._stream.save_context()
    if self.read_until(")"):
        return self._stream.validate_context()
    return self._stream.restore_context()


@meta.hook(Import)
def validate_import(self: Import, context: parsing.Node,
                    current_block: parsing.Node, filename: parsing.Node) -> bool:
    pathname = path.abspath(self.value(filename).strip('(').strip(')'))
    if not path.isfile(pathname + ".kh"):
        print(error.Error("imported file " + pathname + ".kh doesn't exist."))
        return False
    ast = nodes.Imp(pathname)
    current_block.ref.body.append(ast)
    self.imported = kooc.Kooc().parse_file('{0}.kh'.format(pathname))
    if type(current_block.ref) is not cnorm.nodes.RootBlockStmt:
        print(error.Error("can not import inside a class or a namespace"), file=sys.stderr)
        return False
    for key in self.imported.types:
        current_block.ref.types[key] = self.imported.types[key]
    return True
