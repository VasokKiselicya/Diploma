
class Identifier(object):

    def __init__(self, identifier=""):
        self.identifier = identifier

    def __add__(self, other):
        assert isinstance(other, (str, Identifier))
        if not isinstance(other, str):
            other = other.identifier
        return Identifier(self.identifier + other)

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        assert isinstance(other, Identifier)
        return hash(other) == self.__hash__()

    def __str__(self):
        return self.identifier

    def is_valid(self):
        return self.identifier.isidentifier()
