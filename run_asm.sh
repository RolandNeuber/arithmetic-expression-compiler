nasm -f elf64 target/target.asm -o target/target.o
ld target/target.o -o target/target
target/target