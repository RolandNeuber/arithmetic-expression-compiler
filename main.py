"""This project compiles arithmetic expressions containing 
+, * and integer literals into the corresponding NASM."""


from pprint import pprint
from parsing import parse
from lexing import tokenize


def main():
    """Entrypoint of the compiler."""
    pprint(parse(tokenize("4 + 2 * 55 + 3")), width=1)


if __name__ == "__main__":
    main()
