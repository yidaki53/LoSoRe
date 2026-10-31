.code16
.section .text
.global _start

.set STRING_SIZE, 256
.set CASE_SIZE, 4 + STRING_SIZE * 2
.set TRACE_SIZE, 20 + STRING_SIZE * 2

_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cld

    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle

    mov $trace_name, %dx
    mov $0x3c00, %ax
    xor %cx, %cx
    int $0x21
    jc failed
    mov %ax, output_handle

next_case:
    mov input_handle, %bx
    mov $0x6800, %dx
    mov $CASE_SIZE, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    test %ax, %ax
    jz finish
    cmp $CASE_SIZE, %ax
    jne failed

    push %ds
    push %es
    push %cs
    pop %ds
    push %cs
    pop %es
    mov $0x6804, %si
    mov $0x5000, %di
    mov $STRING_SIZE, %cx
    rep movsb
    mov $0x6904, %si
    mov $0x5400, %di
    mov $STRING_SIZE, %cx
    rep movsb
    pop %es
    pop %ds

    incw case_index
    mov case_index, %ax
    mov %ax, trace_record
    mov %cs, %ax
    mov %ax, trace_record+2
    mov %ds, %ax
    mov %ax, trace_record+4
    mov %es, %ax
    mov %ax, trace_record+6
    mov %ss, %ax
    mov %ax, trace_record+8
    mov %sp, %ax
    mov %ax, trace_record+10
    movw $0x5000, trace_record+16
    movw $0x5400, trace_record+18

    push %cs
    push $0x5400
    push %cs
    push $0x5000
    push %cs
    push $compare_return
    push %cs
    push $0x3f86
    lret

compare_return:
    pushf
    pop %ax
    mov %ax, trace_record+14
    mov %sp, %ax
    mov %ax, trace_record+12

    push %ds
    push %es
    push %cs
    pop %ds
    push %cs
    pop %es
    mov $0x5000, %si
    mov $trace_record+20, %di
    mov $STRING_SIZE, %cx
    rep movsb
    mov $0x5400, %si
    mov $trace_record+276, %di
    mov $STRING_SIZE, %cx
    rep movsb
    pop %es
    pop %ds

    mov output_handle, %bx
    mov $trace_record, %dx
    mov $TRACE_SIZE, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $TRACE_SIZE, %ax
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

input_name:
    .asciz "CASES.BIN"
trace_name:
    .asciz "TRACE.BIN"

.align 2
case_index:
    .word 0
input_handle:
    .word 0
output_handle:
    .word 0
trace_record:
    .space TRACE_SIZE
