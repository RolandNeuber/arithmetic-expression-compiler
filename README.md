[id1]: ## "Netwide Assembler"

# Getting Started

To compile an arithmetic expression containing `+`, `*`, and integer literals, create a file named `source` in the same directory as this file. 
The file should contain the arithmetic expression you want to compile.

For example (in `source`):
```
123 * 45 + 67 * 89 + 1000 * 200 + 333
```

To compile the source into the corresponding NASM code (in [`target/target.asm`](target/target.asm)), execute the python script:
```sh
$ python3 main.py
```

Install [`NASM`][id1] to for the following steps, if not already installed:
```sh
$ apt install nasm
```

Then execute the [`run_asm.sh`](run_asm.sh) script to assemble the NASM and run it.

For example:
```sh
$ ./run_asm.sh
211831
```

This creates two more files in `target`:
- `target.o` &rarr; [`Object file`](https://en.wikipedia.org/wiki/Object_file) 
- `target` &rarr; [`Executable`](https://en.wikipedia.org/wiki/Executable)

# Examples

## Minimal working example

Source:
```
0
```

ASM:
```NASM
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

    mov rax, 0              ; <----- Only this part is unique.

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
    syscall
```

## Simple expression

```
2 + 3
```

```ASM
mov rax, 2
push rax

mov rax, 3
pop rcx
add rax, rcx
```

## Complex expression

```
4 + 2 * 55 + 3
```

```ASM
mov rax, 4
push rax

mov rax, 2
push rax

mov rax, 55
pop rcx
xor rdx, rdx
mul rcx
pop rcx
add rax, rcx
push rax

mov rax, 3
pop rcx
add rax, rcx
```