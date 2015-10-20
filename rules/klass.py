from pyrser import grammar, meta, parsing
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes


class Klass(grammar.Grammar):
    entry = 'translation_unit'
    grammar = """
            declaration = [
                "@class" __scope__:current_block  id:class_name "()"
                '{' [ declaration ]* '}'
            ]
            inner_class = [
                [ access | callable ]
                c_decl
            ]
            access = [
                "@access" #create_access(_)
                '(' [
                    "get:" id:access_type #configure_get_access(_, access_type) |
                    "set:" id:access_type #configure_set_access(_, access_type)
                    ]* ')'
            ]
            callable = [
                "@callable" #create_callable(_)
                '(' [
                    "static" #configure_staticity(_) |
                    "virtual" #configure_virtuality(_) |
                    "call:" id:access_type #configure_call_access(_, access_type)
                    ]* ')'
            ]
        """
