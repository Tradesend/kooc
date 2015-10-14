from pyrser import meta
from pyrser.parsing import node
from compiler import mangler
import copy
import cnorm
import nodes


def sub_partial_resolution(var, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler):
    if isinstance(var, node.Node):
        return var.kooc_partial_resolution(ast, mangler)
    elif isinstance(var, dict):
        return {_key: _var for _key, _var in var.items() if not sub_partial_resolution(_var, ast, mangler)}
    elif isinstance(var, str):
        return var;
    elif hasattr(var, '__iter__'):
        bod = []
        for _var in var:
            __var = sub_partial_resolution(_var, ast, mangler)
            if isinstance(__var, list):
                bod = bod + __var
            elif not (__var is None):
                bod.append(__var)
        return bod
    return var


def _kooc_partial_resolution(self, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler):
    dellist = []
    for var in vars(self):
        _var = sub_partial_resolution(getattr(self, var), ast, mangler)
        if _var is None:
            dellist.append(var)
        else:
            setattr(self, var, _var)
    for _del in dellist:
        delattr(self, _del)
    return self


@meta.add_method(node.Node)
def kooc_partial_resolution(self, ast: cnorm.nodes.BlockStmt, _mangler: mangler.Mangler = mangler.Mangler()):
    if hasattr(self, '_name'):
        self._name = _mangler.name(self._name).mangle("container", "name")
    return _kooc_partial_resolution(self, ast, mangler.Mangler())


@meta.add_method(nodes.Nmspce)
def kooc_partial_resolution(self: nodes.Nmspce, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler):
    new_mangler = copy.copy(mangler)
    new_mangler.enable()
    new_mangler.container(self.name)
    _kooc_partial_resolution(self, ast, new_mangler)
    return self.body
