__author__ = 'collio_v'


class Mangler:
    def __init__(self, enabled: bool = False):
        self.base_name = ""
        self.enabled = enabled
        self._container = ""
        self._name = ""
        self._type = ""
        self._params = ""
        self._symtype = "__{0}{1}".format(
            len('variable'),
            'variable'
        )

    def container(self, container: str):
        self._container = "{0}___{1}{2}".format(
            self._container,
            len(container),
            container
        )
        return self

    def variable(self):
        self._symtype = "__{0}{1}".format(
            len('variable'),
            'variable'
        )
        return self

    def callable(self):
        self._symtype = "__{0}{1}".format(
            len('callable'),
            'callable'
        )
        return self

    def virtual(self):
        self._symtype = "__{0}{1}".format(
            len('virtual'),
            'virtual'
        )
        return self

    def type(self, _type: str):
        self._type = "__{0}{1}".format(
            len(_type),
            _type
        )
        return self

    def params(self, type_list: list):
        self._params = ""
        for decl in type_list:
            self._params = "{0}__{1}{2}".format(
                self._params,
                len(decl._ctype._identifier),
                decl._ctype._identifier
            )
        return self

    def name(self, name: str):
        self.base_name = name
        self._name = "__{0}{1}".format(
            len(name),
            name
        )
        return self

    def mangle(self):
        if not self.enabled:
            return self.base_name
        mangled = self._container + self._symtype + self._name + self._type + self._params
        return mangled

    def enable(self):
        self.enabled = True;

    def disable(self):
        self.enabled = False;
