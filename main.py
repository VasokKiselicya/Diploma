from utils import Printer
from exceptions import SyntaxException
from identifier import Identifier


class SetInterpreter(object):

    EXIT = "exit"
    PRINT_SYMBOL = "?"
    COMMENT_SYMBOL = "#"
    ALLOWED_OPERATIONS = ["|", "-", "^"]  # & in another state because operation priority
    FACTOR_INCREMENT = {'(': 1, ')': -1}

    def __init__(self):
        self._set_collection = {}

    def parse_statement(self, _input):
        statement = self.format(_input)

        if not statement:
            return

        if statement[0].isalpha():
            self.parse_var_assign(statement)
        elif statement.startswith(self.PRINT_SYMBOL):
            self.print_expression(statement)
        elif statement.startswith(self.COMMENT_SYMBOL):
            Printer.print_comment(statement[1:])
        else:
            raise SyntaxException

    def parse_var_assign(self, statement):

        if "=" not in statement:
            raise SyntaxException

        identifier, expression = statement.split('=', 1)

        identifier = self.parse_identifier(identifier)
        expression = self.parse_expression(expression)

        self._set_collection[identifier] = expression

    def parse_expression(self, expression) -> set:
        result, open_complex_factors, term = (None, 0, "")

        idx, iter_expression = 0, iter(expression)

        while iter_expression.__length_hint__():
            symbol = next(iter_expression, None)

            if symbol in self.FACTOR_INCREMENT.keys():
                open_complex_factors += self.FACTOR_INCREMENT.get(symbol)
                term += symbol

            elif open_complex_factors == 0 and symbol in self.ALLOWED_OPERATIONS:

                if result is None:
                    result = self.parse_term(term) or set()

                operator, term = symbol, ""

                while iter_expression.__length_hint__():
                    symbol = next(iter_expression, None)
                    if open_complex_factors == 0 and symbol in self.ALLOWED_OPERATIONS:
                        result = self.operation(result or set(), self.parse_term(term) or set(), operator)
                        term = ""
                        break
                    elif symbol in self.FACTOR_INCREMENT.keys():
                        open_complex_factors += self.FACTOR_INCREMENT.get(symbol)
                        term += symbol
                    else:
                        term += symbol
                if term:
                    result = self.operation(result or set(), self.parse_term(term) or set(), operator)

            else:
                term += symbol

        if result is None or (not result and term):
            result = self.parse_term(term)

        return result or set()

    def parse_factor(self, factor) -> set:
        result, open_complex_factors, set_values = set(), 0, ""

        idx, iter_factor = 0, iter(factor)

        while True:
            symbol = next(iter_factor, None)
            idx += 1

            if symbol is None:
                break

            if symbol == "(":
                open_complex_factors += 1

                while open_complex_factors != 0:
                    symbol = next(iter_factor, None)
                    if symbol == "(":
                        open_complex_factors += 1
                        set_values += symbol
                    elif symbol == ")":
                        open_complex_factors -= 1

                        if open_complex_factors == 0:
                            symbol = next(iter_factor, None)
                            if symbol is not None:
                                raise SyntaxException("Invalid token detected")
                        else:
                            set_values += symbol
                    else:
                        set_values += symbol

                print(set_values)
                result = self.parse_expression(set_values)

            elif symbol.isalpha():
                set_values += symbol

                while True:
                    symbol = next(iter_factor, None)
                    if symbol and (symbol.isdigit() or symbol.isalpha()):
                        set_values += symbol
                    else:
                        break

                identifier = self.parse_identifier(set_values)
                if self._set_collection.get(identifier):
                    result = self._set_collection[identifier]
                else:
                    raise SyntaxException("Identifier '{}' does not correspond to a Set".format(str(identifier)))

            elif symbol == "{":
                symbol = next(iter_factor, None)

                if symbol == ",":
                    raise SyntaxException("Number missing in set")

                while True:
                    if symbol and symbol != "}":
                        set_values += symbol
                        symbol = next(iter_factor, None)
                    else:
                        break

                if symbol != "}":
                    raise SyntaxException("Invalid token in set")

                if iter_factor.__length_hint__():
                    raise SyntaxException("Operator or end of line missing")

                result = self.parse_set(set_values)
            else:
                raise SyntaxException("Invalid statement detected")

        if open_complex_factors != 0:
            raise SyntaxException("Missing parenthesis detected")

        return result

    def parse_term(self, term):
        result, open_complex_factors, factor = set(), 0, ""

        for idx, symbol in enumerate(term):
            if symbol in self.FACTOR_INCREMENT.keys():
                open_complex_factors += self.FACTOR_INCREMENT.get(symbol)
                factor += symbol
            elif symbol == "&" and open_complex_factors == 0:
                return self.parse_factor(factor).intersection(self.parse_term(term[idx + 1:]))
            else:
                factor += symbol

        return self.parse_factor(factor)

    @classmethod
    def parse_set(cls, set_values):
        set_values = set_values.split(",")
        if not all(map(lambda x: x.isdigit(), set_values)):
            raise SyntaxException("Only digits in set allowed")
        return set(map(int, set_values))

    @staticmethod
    def operation(op1: set, op2: set, operation: str):
        print(op1, op2, operation)
        if operation == "|":
            return op1.union(op2)
        if operation == "^":
            return op1.symmetric_difference(op2)
        if operation == "-":
            return op1.difference(op2)

        return set()

    @classmethod
    def parse_identifier(cls, identifier):
        identifier = Identifier(identifier)

        if not identifier.is_valid():
            raise SyntaxException("Identifier has not valid format.")

        return identifier

    def print_expression(self, expression):
        self.skip_token(expression, "?")
        Printer.print_answer(", ".join(map(str, self.parse_expression(expression[1:]))))

    @classmethod
    def skip_token(cls, _input, char):
        if not _input.startswith(char):
            raise SyntaxException("Missing token : {}".format(char))

    @classmethod
    def check_formatted_expression(cls, expression):

        for idx in range(len(expression)):
            if expression[idx] == ",":
                try:
                    if not all((
                            expression[idx - 1].isdigit(),
                            expression[idx + 1].isdigit()
                    )):
                        raise SyntaxException("Missing Number in set")
                except Exception as e:
                    raise SyntaxException(str(e))
            elif expression[idx] == '0':
                if all((
                        not expression[idx - 1].isdigit(),
                        expression[idx + 1].isdigit(),
                )):
                    raise SyntaxException("Invalid number given")

    def format(self, code_line):

        if code_line.startswith(self.COMMENT_SYMBOL):  # Comment
            return code_line

        statement = ""

        for idx, symbol in enumerate(code_line):

            if symbol.isdigit() or symbol.isalpha():
                statement += symbol

                char = 1
                while idx + char < len(code_line) and code_line[idx + char] == " ":
                    self.skip_token(code_line[idx + char], " ")
                    char += 1

                    if any((code_line[idx + char].isdigit(), code_line[idx + char].isalpha())):
                        raise SyntaxException("Spaces in Identifier and between numbers not allowed")

            elif symbol == " ":
                continue
            else:
                statement += symbol

        self.check_formatted_expression(statement)

        return statement

    def __call__(self, *args, **kwargs):
        Printer.print_success("Start Program: ")

        while True:
            try:

                _input = input()

                if _input.lower() == self.EXIT:
                    Printer.print_success("End Program\n")
                    break

                self.parse_statement(_input)

            except SyntaxException as e:
                Printer.print_error(str(e))
            except Exception as e:
                import traceback
                Printer.print_error("{}\n{}".format(str(e), traceback.format_exc()))


if __name__ == '__main__':
    SetInterpreter()()
