from antlr4 import *
from analyzer.solLexer import solLexer as MyGrammarLexer
from analyzer.solParser import solParser as MyGrammarParser


def get_grammar_tree(
        file_path=None,
        code_text=None
):
    assert any((file_path, code_text))
    if file_path:
        input_stream = FileStream(file_path)
    else:
        input_stream = InputStream(code_text)
    lexer = MyGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MyGrammarParser(stream)

    if file_path:
        tree = parser.program()
    else:
        tree = parser.line()

    return tree, parser
