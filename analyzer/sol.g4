grammar sol;

program: line+ EOF;
line: (assignment | print_statement | comment) NEWLINE;

assignment: identifier '=' expression;
print_statement: '?' expression;
comment : '#' .* ;

identifier: LETTER (LETTER | number)*;

expression: term (('|' | '-' | '^') term)*;

term: factor ('&' factor)*;

factor: identifier | complex_factor | raw_set;

complex_factor: '(' expression ')';
raw_set: '{' row_of_numbers '}';

row_of_numbers: natural_number (',' natural_number)*;

natural_number: positive_number | zero;
positive_number: NON_ZERO_DIGIT number*;
number: zero | NON_ZERO_DIGIT;

zero: '0';


LETTER : 'A'..'Z' | 'a'..'z';
NON_ZERO_DIGIT : [1-9];
NEWLINE: ('\r'? '\n' | '\r')+ ;
WS  : [ \t\n]+ -> skip;
