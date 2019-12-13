from tkinter import Tk

import nltk
import string

from nltk.draw import CFGEditor

grammar_text = """
  S -> assignment | print_statement | comment
  assignment -> identifier assignment_operator expression
  print_statement -> print_operator expression
  comment  -> comment_operator 
 
  identifier -> letter identifier_endx
  identifier_end -> letter | number
  
  expression -> term additive_operator_termx
  additive_operator_term -> additive_operator term

  term -> factor multiplicative_operator_factorx
  multiplicative_operator_factor -> multiplicative_operator factor
 
  factor -> identifier | complex_factor | set
  complex_factor -> open_factor expression close_factor
 
  set -> open_set row_natural_numbers close_set
 
  row_natural_numbers -> natural_number comma_numberx
  comma_number -> comma_symbol natural_number
     
  natural_number -> positive_number | zero
  positive_number -> not_zero numberx
  number -> zero | not_zero
 
  additive_operator ->  "+" | "|" | "-"
  multiplicative_operator -> "*"
  assignment_operator -> "="
  print_operator -> "?"
  comment_operator -> "#"
  comma_symbol -> ","

  open_factor -> "("
  close_factor -> ")"
  
  open_set -> {open_set}
  close_set -> {close_set}

  zero -> "0"
  not_zero -> {numbers}
  letter -> {letters}
  
  """.format(
    open_set='"{"',
    close_set='"}"',
    numbers="|".join(map(lambda x: '"%s"' % x, string.digits[1:])),
    letters="|".join(map(lambda x: '"%s"' % x, string.ascii_letters)),
)

grammar = nltk.CFG.fromstring(grammar_text)

if __name__ == '__main__':
    rd_parser = nltk.ChartParser(grammar)
    res = rd_parser.parse("Set1={1,2,3}")

    print(list(res))

    top = Tk()
    editor = CFGEditor(top, grammar, print)
    top.mainloop()

