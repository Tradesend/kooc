import sys
import cnorm
from pyrser import grammar, meta, parsing
from compiler import error
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes

KoocOperators = {
    "new": nodes.New,
    "delete": nodes.Delete,
    "call": nodes.Call,
    "set": nodes.Set,
    "get": nodes.Get,
}


class Koperators(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
        postfix_expression = [
          [
            '@' kooc_operators:operator '(' identifier:operator_type ')' '(' func_arg_list?:args ')'
            #make_kooc_operator(_, operator, operator_type, args)
          ]
          | Expression.postfix_expression:>_
        ]
        kooc_operators = [ "new" | "delete" | "call" | "set" | "get" ]
        """


@meta.hook(Koperators)
def make_kooc_operator(self: Koperators, context, operator, operator_type, args):
    alist = []
    if hasattr(args, 'list'):
        alist = args.list
    if self.value(operator) in ["new", "delete"]:
        context.set(
            KoocOperators[self.value(operator)]
            (self.value(operator_type),
             cnorm.nodes.Id(self.value(operator)),
             alist))
    elif self.value(operator) in ["call", "get", "set"]:
        if not hasattr(args, 'list'):
            print(error.Error("Koperator " + self.value(operator).upper() + " must have instance as first argument"),
                  file=sys.stderr)
            return False
        if self.value(operator) == "get" and len(args.list) != 1:
            print(error.Error("Koperator GET must have the instance as first and unique argument"), file=sys.stderr)
            return False
        if self.value(operator) == "set" and len(args.list) != 2:
            print(
                error.Error("Koperator SET must have the instance as first and new_value as second and only arguments"),
                file=sys.stderr)
            return False
        context.set(
            KoocOperators[self.value(operator)]
            (self.value(operator_type),
             cnorm.nodes.Id(self.value(operator)),
             alist))
    return True
