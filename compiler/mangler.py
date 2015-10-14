__author__ = 'collio_v'


class Mangler:
    def __init__(self, enabled: bool = False):
        self.base_name = ""
        self.enabled = enabled
        self._container = ""
        self._name = ""

    def container(self, container: str):
        self._container = "{0}___{1}{2}".format(
            self._container,
            len(container),
            container
        )
        return self

    def name(self, name: str):
        self.base_name = name
        self._name = "__{0}{1}".format(
            len(name),
            name
        )
        return self

    def mangle(self, *args):
        if not self.enabled:
            return self.base_name
        mangled = ""
        for arg in args:
            mangled += getattr(self, '_' + arg)
        return mangled

    def enable(self):
        self.enabled = True;

    def disable(self):
        self.enabled = False;