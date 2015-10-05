from pyrser import grammar, meta, parsing
from cnorm.parsing import declaration
import nodes


class Import(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
        preproc_decl = [ kooc_import | Declaration.preproc_decl ]
        kooc_import = [ "@import" import_directive:filename
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
    ast = nodes.Imp(self.value(filename).strip('(').strip(')'))
    current_block.ref.body.append(ast)
    return True
