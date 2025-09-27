"""This project compiles arithmetic expressions containing 
+, * and integer literals into the corresponding NASM."""


from dataclasses import dataclass
from typing import List, cast
from pprint import pprint


@dataclass
class Token:
    """Base class for all tokens emitted by the tokenizer."""


@dataclass
class Plus(Token):
    """Token for the '+' operator."""


@dataclass
class Star(Token):
    """Token for the '*' operator."""


@dataclass
class Expression:
    """Base class for all expressions contained in the AST."""


@dataclass
class Add(Expression):
    """Expression of the form: expr_left + expr_right"""
    left: Expression
    right: Expression


@dataclass
class Multiply(Expression):
    """Expression of the form: expr_left * expr_right"""
    left: Expression
    right: Expression


@dataclass
class Number(Token, Expression):
    """Number literal, both token and expression."""
    value: int


def tokenize(source: str) -> List[Token]:
    """Tokenizes the source code string into a list of tokens."""
    acc = ""
    result: List[Token] = []

    while len(source) != 0:
        acc += source[0]
        source = source[1:]
        match acc:
            case " ":
                pass
            case "+":
                result.append(Plus())
            case "*":
                result.append(Star())
            case _:
                if len(source) != 0 and source[0].isdigit():
                    continue # Not all digits of the number have been yielded.
                result.append(Number(int(acc)))
        acc = ""
    return result


def parse(tokens: List[Token]) -> List[Expression]:
    """Parses a list of tokens into an AST."""
    lookahead = 0
    terms: List[Token|Expression] = []
    expr: Token|Expression

    for i, expr in enumerate(tokens):
        if lookahead > 0:
            lookahead -= 1
            continue
        if isinstance(expr, Star):
            arg1: Token | Expression = terms.pop() # remove arg1 from ast
            arg2: Token | Expression = tokens[i + 1]
            assert isinstance(arg1, Expression)
            assert isinstance(arg2, Expression)
            terms.append(Multiply(arg1, arg2))
            lookahead = 1 # remove arg2 from ast
        else:
            terms.append(expr)

    ast: List[Token|Expression] = []

    for i, expr in enumerate(terms):
        if lookahead > 0:
            lookahead -= 1
            continue
        if isinstance(expr, Plus):
            arg1 = ast.pop() # remove arg1 from ast
            arg2 = terms[i + 1]
            assert isinstance(arg1, Expression)
            assert isinstance(arg2, Expression)
            ast.append(Add(arg1, arg2))
            lookahead = 1 # remove arg2 from ast
        else:
            ast.append(expr)

    return cast(List[Expression], ast)


def main():
    """Entrypoint of the compiler."""
    pprint(parse(tokenize("2 * 55 + 3 + 4")), width=1)


if __name__ == "__main__":
    main()
