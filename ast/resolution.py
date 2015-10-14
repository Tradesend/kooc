from pyrser import meta
from pyrser.parsing import node
from compiler import mangler
import cnorm
import nodes


def sub_resolution(var, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler):
    if isinstance(var, node.Node):
        return var.kooc_resolution(ast, mangler)
    elif isinstance(var, dict):
        return {_key: _var for _key, _var in var if not sub_resolution(_var, ast, mangler)}
    elif isinstance(var, str):
        return var;
    elif hasattr(var, '__iter__'):
        bod = []
        for _var in var:
            __var = sub_resolution(_var, ast, mangler)
            if hasattr(__var, '__iter__'):
                bod = bod + __var
            elif not (__var is None):
                bod.append(__var)
        return bod
    return var


@meta.add_method(node.Node)
def kooc_resolution(self, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler = mangler.Mangler("")):
    dellist = []
    for var in vars(self):
        _var = sub_resolution(getattr(self, var), ast, mangler)
        if _var is None:
            dellist.append(var)
        else:
            setattr(self, var, _var)
    for _del in dellist:
        delattr(self, _del)
    return self


@meta.add_method(nodes.Nmspce)
def kooc_resolution(self: nodes.Nmspce, ast: cnorm.nodes.BlockStmt, mangler: mangler.Mangler):
    mangler.container(self.name)
    super(node.Node, self).kooc_resolution(ast, mangler)
    return self.body
