
class Printer(object):

    DEBUG = True

    CRED = '\033[91m'
    CGREEN = '\033[92m'
    CBLUE = '\033[94m'
    CGREY = '\033[90m'

    CEND = '\033[0m'

    @classmethod
    def print_error(cls, text):
        print("".join([cls.CRED, text, cls.CEND]))

    @classmethod
    def print_success(cls, text):
        print("".join([cls.CGREEN, text, cls.CEND]))

    @classmethod
    def print_comment(cls, text):
        print("".join([cls.CGREY, text, cls.CEND]))

    @classmethod
    def print_answer(cls, text):
        print("".join([cls.CBLUE, text, cls.CEND]))

    @classmethod
    def print_debug(cls, text):
        if cls.DEBUG:
            print("".join([cls.CGREY, text, cls.CEND]))

