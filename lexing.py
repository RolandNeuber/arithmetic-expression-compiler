"""This module is responsible for tokenizing the source code string into a list of tokens."""


from dataclasses import dataclass
from typing import List


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
class Number(Token):
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
