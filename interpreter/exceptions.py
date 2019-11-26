
class SyntaxException(Exception):

    def __init__(self, *args):

        if not args:
            args = ("Invalid statement, please read the documentation",)

        super().__init__(*args)
