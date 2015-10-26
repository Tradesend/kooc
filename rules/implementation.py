import cnorm
from pyrser import grammar, meta, parsing
from compiler import error
from os import path
from compiler import error
from cnorm.parsing import declaration
import nodes


class Implementation(grammar.Grammar):
    entry = "translation_unit"
    grammar = """
            declaration = [
                "@implementation" __scope__:current_block '(' id:implementation_name ')' #create_implementation(_, implementation_name, current_block)
                '{' [ method_implementation | ctor_implementation | dtor_implementation ]* '}' #end_implementation(_)
                ';'
            ]

            method_implementation = [
                __scope__:local_specifier
                #Declaration.create_ctype(local_specifier)
                declaration_specifier*:dsp
                declarator:decl
                Statement.compound_statement:block
                #define_method(decl, current_block)
                #Declaration.add_body(decl, block)
            ]

            ctor_implementation = [
                __scope__:local_specifier
                "@" !!"constructor"
                #Declaration.create_ctype(local_specifier)
                declarator:decl
                callable:callable
                Statement.compound_statement:block
                #define_ctor(decl, current_block)
                #Declaration.add_body(decl, block)
            ]

            dtor_implementation = [
                __scope__:local_specifier
                "@" !!"destructor"
                #Declaration.create_ctype(local_specifier)
                declarator:decl
                callable:callable
                Statement.compound_statement:block
                #define_dtor(decl, current_block)
                #Declaration.add_body(decl, block)
            ]
        """


@meta.hook(Implementation)
def create_implementation(self: Implementation, context, implementation_name: str, current_block):
    context.set(nodes.Impl(self.value(implementation_name)))
    current_block.ref = context
    return True


@meta.hook(Implementation)
def end_implementation(self: Implementation, context: nodes.Impl):
    self.rule_nodes.parents['current_block'].ref.body.append(context)
    return True


@meta.hook(Implementation)
def define_method(self: Implementation, declaration, current_block):
    declaration.set(nodes.MethodImplementation(declaration))
    current_block.ref.body.append(declaration)
    return True


@meta.hook(Implementation)
def define_ctor(self: Implementation, declaration, current_block):
    declaration.set(nodes.ConstructorImplementation(declaration))
    current_block.ref.body.append(declaration)
    return True


@meta.hook(Implementation)
def define_dtor(self: Implementation, declaration, current_block):
    declaration.set(nodes.ConstructorImplementation(declaration))
    current_block.ref.body.append(declaration)
    return True
