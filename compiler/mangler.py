__author__ = 'collio_v'


class Mangler:
    def __init__(self, name: str):
        self.container = ""
        self.name = "__{0}{1}".format(
            len(name),
            name
        )

    def container(self, container: str):
        self.container = "{0}___{1}{2}".format(
            self.container,
            len(container),
            container
        )
