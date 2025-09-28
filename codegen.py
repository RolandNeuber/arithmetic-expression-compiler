"""This module is responsible for generating NASM from an AST."""


from textwrap import indent
from lexing import Number
from parsing import Expression, Add, Multiply


def codegen(ast: Expression) -> str:
    """Returns a string of NASM code generated from the AST."""
    def inner(ast: Expression) -> str:
        asm = ""
        if isinstance(ast, Number):
            asm += f"mov rax, {ast.value}\n"
        elif isinstance(ast, (Add, Multiply)):
            asm += inner(ast.left)
            asm += "push rax\n\n"
            asm += inner(ast.right)
            asm += "pop rcx\n"
            if isinstance(ast, Add):
                asm += "add rax, rcx\n"
            else:
                asm += "xor rdx, rdx\n"
                asm += "mul rcx\n"
        return asm
    return wrap_boilerplate(inner(ast).strip())


def wrap_boilerplate(asm: str) -> str:
    """Wraps the generated NASM code with boilerplate."""
    return """\
section .bss
    buffer resb 20          ; reserve 20 bytes for the digits of the result
                            ; (2^64 contains 20 decimal digits)

section .data
    newline db 10

section .text
    global _start

_start:
    ; ==================
    ; Auto-generated asm
    ; ==================

""" + indent(asm, "    ") + """

    ; ======================
    ; Auto-generated asm end
    ; ======================

    mov rcx, 10             ; quotient
    mov rbx, buffer + 20    ; point rbx to the end of buffer
    mov r8, 0               ; counter for digits

.convert_loop:
    ; ================================
    ; Convert remainder to ASCII digit
    ; ================================

    xor rdx, rdx            ; clear rdx to perform division
    div rcx                 ; divide by 10
                            ; rax = rdx:rax / rcx
                            ; rdx = rdx:rax % rcx
    add dl, '0'             ; convert remainder to ASCII digit
                            ; (dl is lower 8 bits of rdx)
    dec rbx                 ; move buffer one byte left
    inc r8
    mov [rbx], dl           ; *rbx = digit -> stores digit in buffer
    test rax, rax           ; "mental" AND (only set flag)
                            ; check if rax is zero and set zero flag accordingly
    jnz .convert_loop       ; repeat until zero

    ; ============================
    ; Write ASCII digits to stdout
    ; ============================

    ; write(1, msg, len)
    mov rax, 1              ; syscall: write
    mov rdi, 1              ; file descriptor: stdout
    mov rsi, rbx            ; pointer to message
    mov rdx, r8             ; message length
    syscall

    ; write(1, msg, len)
    mov rax, 1              ; syscall: write
    mov rdi, 1              ; file descriptor: stdout
    mov rsi, newline        ; pointer to message
    mov rdx, 1              ; message length
    syscall

    ; exit(0)
    mov rax, 60             ; syscall: exit
    mov rdi, 0              ; status: 0
    syscall\
"""
