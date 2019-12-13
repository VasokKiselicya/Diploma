# Generated from sol.g4 by ANTLR 4.7.1
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .solParser import solParser
else:
    from solParser import solParser


# This class defines a complete listener for a parse tree produced by solParser.
class solListener(ParseTreeListener):

    # Enter a parse tree produced by solParser#program.
    def enterProgram(self, ctx: solParser.ProgramContext):
        pass

    # Exit a parse tree produced by solParser#program.
    def exitProgram(self, ctx: solParser.ProgramContext):
        pass

    # Enter a parse tree produced by solParser#line.
    def enterLine(self, ctx: solParser.LineContext):
        pass

    # Exit a parse tree produced by solParser#line.
    def exitLine(self, ctx: solParser.LineContext):
        pass

    # Enter a parse tree produced by solParser#assignment.
    def enterAssignment(self, ctx: solParser.AssignmentContext):
        pass

    # Exit a parse tree produced by solParser#assignment.
    def exitAssignment(self, ctx: solParser.AssignmentContext):
        pass

    # Enter a parse tree produced by solParser#print_statement.
    def enterPrint_statement(self, ctx: solParser.Print_statementContext):
        pass

    # Exit a parse tree produced by solParser#print_statement.
    def exitPrint_statement(self, ctx: solParser.Print_statementContext):
        pass

    # Enter a parse tree produced by solParser#comment.
    def enterComment(self, ctx: solParser.CommentContext):
        pass

    # Exit a parse tree produced by solParser#comment.
    def exitComment(self, ctx: solParser.CommentContext):
        pass

    # Enter a parse tree produced by solParser#identifier.
    def enterIdentifier(self, ctx: solParser.IdentifierContext):
        pass

    # Exit a parse tree produced by solParser#identifier.
    def exitIdentifier(self, ctx: solParser.IdentifierContext):
        pass

    # Enter a parse tree produced by solParser#expression.
    def enterExpression(self, ctx: solParser.ExpressionContext):
        pass

    # Exit a parse tree produced by solParser#expression.
    def exitExpression(self, ctx: solParser.ExpressionContext):
        pass

    # Enter a parse tree produced by solParser#term.
    def enterTerm(self, ctx: solParser.TermContext):
        pass

    # Exit a parse tree produced by solParser#term.
    def exitTerm(self, ctx: solParser.TermContext):
        pass

    # Enter a parse tree produced by solParser#factor.
    def enterFactor(self, ctx: solParser.FactorContext):
        pass

    # Exit a parse tree produced by solParser#factor.
    def exitFactor(self, ctx: solParser.FactorContext):
        pass

    # Enter a parse tree produced by solParser#complex_factor.
    def enterComplex_factor(self, ctx: solParser.Complex_factorContext):
        pass

    # Exit a parse tree produced by solParser#complex_factor.
    def exitComplex_factor(self, ctx: solParser.Complex_factorContext):
        pass

    # Enter a parse tree produced by solParser#raw_set.
    def enterRaw_set(self, ctx: solParser.Raw_setContext):
        pass

    # Exit a parse tree produced by solParser#raw_set.
    def exitRaw_set(self, ctx: solParser.Raw_setContext):
        pass

    # Enter a parse tree produced by solParser#row_of_numbers.
    def enterRow_of_numbers(self, ctx: solParser.Row_of_numbersContext):
        pass

    # Exit a parse tree produced by solParser#row_of_numbers.
    def exitRow_of_numbers(self, ctx: solParser.Row_of_numbersContext):
        pass

    # Enter a parse tree produced by solParser#natural_number.
    def enterNatural_number(self, ctx: solParser.Natural_numberContext):
        pass

    # Exit a parse tree produced by solParser#natural_number.
    def exitNatural_number(self, ctx: solParser.Natural_numberContext):
        pass

    # Enter a parse tree produced by solParser#positive_number.
    def enterPositive_number(self, ctx: solParser.Positive_numberContext):
        pass

    # Exit a parse tree produced by solParser#positive_number.
    def exitPositive_number(self, ctx: solParser.Positive_numberContext):
        pass

    # Enter a parse tree produced by solParser#number.
    def enterNumber(self, ctx: solParser.NumberContext):
        pass

    # Exit a parse tree produced by solParser#number.
    def exitNumber(self, ctx: solParser.NumberContext):
        pass

    # Enter a parse tree produced by solParser#zero.
    def enterZero(self, ctx: solParser.ZeroContext):
        pass

    # Exit a parse tree produced by solParser#zero.
    def exitZero(self, ctx: solParser.ZeroContext):
        pass
