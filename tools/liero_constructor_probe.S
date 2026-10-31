.code16
# Oracle: isolated original constructor bytes, guarded memory and actual RETF 8.
.section .text
.global _start

_start:
    push %cs
    pop %ds
    mov %sp, %bp
    mov %cs, %ax
    mov %ax, 0x3663
    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, output_handle

next_case:
    mov input_handle, %bx
    mov $0x6800, %dx
    mov $544, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finish
    cmp $544, %ax
    jne failed
    mov %sp, 0x67f4
    push %cs
    push $0x6910
    push %cs
    push $0x6800
    push %cs
    call 0x3639
    mov %sp, %cs:0x67f6
    mov %ds, %ax
    mov %ax, %cs:0x67f0
    mov %ss, %ax
    mov %ax, %cs:0x67f2
    push %cs
    pop %ds
    mov %cs, %ax
    mov %ax, 0x67ee
    mov case_index, %ax
    mov %ax, 0x67ec
    incw case_index
    mov %es, %ax
    mov %ax, 0x67f8
    mov %di, 0x67fa
    movw $0x6910, 0x67fc
    movw $0x6800, 0x67fe
    mov output_handle, %bx
    mov $0x67ec, %dx
    mov $564, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $564, %ax
    jne failed
    jmp next_case

finish:
    mov input_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21

input_handle: .word 0
output_handle: .word 0
case_index: .word 0
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
