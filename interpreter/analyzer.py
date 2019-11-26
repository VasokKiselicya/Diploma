import nltk
from nltk.parse.generate import generate, demo_grammar

# Natural Language Toolkit: code_cfg2

grammar = nltk.CFG.fromstring("""
  S -> NP VP
  VP -> V NP | V NP PP
  PP -> P NP
  V -> "saw" | "ate" | "walked"
  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
  Det -> "a" | "an" | "the" | "my"
  N -> "man" | "dog" | "cat" | "telescope" | "park"
  P -> "in" | "on" | "by" | "with"
  """)

if __name__ == '__main__':
    rd_parser = nltk.RecursiveDescentParser(grammar)
    sent = "Mary saw Bob".split()
    for t in rd_parser.parse(sent):
        print(t)

    for sentence in generate(grammar, n=10):
        print(' '.join(sentence))

    tree1 = nltk.Tree('NP', ['John'])
    tree2 = nltk.Tree('NP', ['the', 'man'])
    tree3 = nltk.Tree('VP', ['saw', tree2])
    tree4 = nltk.Tree('S', [tree1, tree3])
    tree4.draw()
