"""This project compiles arithmetic expressions containing 
+, * and integer literals into the corresponding NASM."""


from codegen import codegen
from parsing import parse
from lexing import tokenize


def main():
    """Entrypoint of the compiler."""
    with open("source", "r", encoding="utf-8") as source:
        asm = codegen(parse(tokenize(source.readline())))
    with open("target/target.asm", "w", encoding="utf-8") as target:
        target.write(asm)

if __name__ == "__main__":
    main()
