import cnorm
from pyrser import grammar, meta, parsing
from compiler import error
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes

KoocOperators = {
    "new": nodes.New,
    "delete": nodes.Delete
}


class Koperands(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
        postfix_expression = [ [
            '@' kooc_operators:operator '(' identifier:operator_type ')' '(' func_arg_list?:args ')'
            #make_kooc_operator(_, operator, operator_type, args)
            ] | Expression.postfix_expression:>_
        ]
        kooc_operators = [ "new" | "delete" ]
        """


@meta.hook(Koperands)
def make_kooc_operator(self: Koperands, context, operator, operator_type, args):
    if (hasattr(args, 'list')):
        context.set(KoocOperators[self.value(operator)](self.value(operator_type), cnorm.nodes.Id(self.value(operator)),
                                                        args.list))
    else:
        context.set(
            KoocOperators[self.value(operator)](self.value(operator_type), cnorm.nodes.Id(self.value(operator)), []))
    return True
