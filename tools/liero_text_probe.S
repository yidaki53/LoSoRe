.code16
# Oracle: original buffered/text routines at original offsets; external errors abort.
.global _start
_start:
    jmp main
.org 0x0f
    mov $0x4c63, %ax
    int $0x21
.org 0x500
main:
    push %cs
    pop %ds
    push %cs
    pop %es
    cli
    push %cs
    pop %ss
    mov $0xdff0, %sp
    sti
    cld
    mov %cs, %ax
    mov %ax, 0x114e
    mov %ax, 0x1153
    add $0x100, %ax
    mov %ax, text_entry+2
    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle
    mov $trace_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, trace_handle
    mov $file_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, output_handle
    mov $0x3521, %ax
    int $0x21
    mov %bx, old_vector
    mov %es, old_vector+2
    push %cs
    pop %es
next_case:
    mov $0xdff0, %sp
    mov input_handle, %bx
    mov $0x6800, %dx
    mov $536, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finished
    cmp $536, %ax
    jne failed
    mov $3, %ax
    int $0x10
    push %es
    mov $0xb800, %ax
    mov %ax, %es
    xor %di, %di
    mov $0x4f2e, %ax
    mov $2000, %cx
    cld
    rep stosw
    pop %es
    mov $0x6818, %si
    mov $0x79f0, %di
    mov $256, %cx
    rep movsb
    mov $0x6918, %si
    mov $0x8200, %di
    mov $256, %cx
    rep movsb
    mov output_handle, %ax
.if CONSOLE == 1
    mov $1, %ax
.endif
    cmpw $0, 0x6816
    je valid_handle
    mov $0xffff, %ax
valid_handle:
    mov %ax, target_handle
    mov %ax, 0x79f0
    mov 0x680c, %ax
    mov %ax, 0x79f2
    mov 0x6806, %ax
    mov %ax, 0x79f4
    mov 0x6808, %ax
    mov %ax, 0x79f8
    mov 0x680a, %ax
    mov %ax, 0x6410
    mov $0x7a70, %ax
    mov 0x6810, %bx
    shl $4, %bx
    sub %bx, %ax
    mov %ax, 0x79fc
    mov %cs, %ax
    add 0x6810, %ax
    mov %ax, 0x79fe
    movw $0x37b3, 0x7a04
    mov %cs, %ax
    mov %ax, 0x7a06
    movw $0x37b3, 0x7a08
    xor %ax, %ax
    cmpw $0, 0x680e
    je optional_ready
    mov %cs, %ax
optional_ready:
    mov %ax, 0x7a0a
    movw $0, calls
    movw $0, violation
    movw $0, sent
    mov $0xc000, %di
    mov $0xffff, %ax
    mov $256, %cx
    rep stosw
    mov $0xc200, %di
    mov $256, %cx
    rep stosw
    mov $service_hook, %dx
    mov $0x2521, %ax
    int $0x21
    movw $0x1357, %ss:0xdff0
    movw $0x2468, %ss:0xdff2
    mov $0x6789, %bp
    mov $0x79f0, %bx
    mov $0x8200, %si
    mov %cs, %dx
    mov 0x6800, %ax
.if TEXT_ENTRY == 0
    call 0x3899
.elseif TEXT_ENTRY == 1
    push %cs
    push $0x79f0
    push %cs
    call 0x3930
.else
    pushw 0x6804
    pushw 0x6802
    push %cs
    push $0x8200
    lcall *text_entry
.endif
    mov 0x6410, %ax
    mov %ax, 0xa000
    mov %ds, 0xa002
    mov %es, 0xa004
    mov %ss, 0xa006
    mov %bp, 0xa008
    mov %sp, 0xa00a
    mov %ax, 0xa00c
    pushf
    popw 0xa00e
    mov %ss:0xdff0, %ax
    mov %ax, 0xa010
    mov %ss:0xdff2, %ax
    mov %ax, 0xa012
    mov calls, %ax
    mov %ax, 0xa014
    mov %cs, %ax
    mov %ax, 0xa016
    mov $0x0300, %ax
    xor %bx, %bx
    int $0x10
    mov %dx, 0xa018
    push %es
    mov $0x40, %ax
    mov %ax, %es
    mov %es:0x49, %al
    xor %ah, %ah
    mov %ax, %cs:0xa01a
    pop %es
    mov violation, %ax
    mov %ax, 0xa01c
    movw $0, 0xa01e
    push %ds
    lds old_vector, %dx
    mov $0x2521, %ax
    int $0x21
    pop %ds
    push %cs
    pop %es
    cld
    mov $0x79f0, %si
    mov $0xa020, %di
    mov $256, %cx
    rep movsb
    mov $0x8200, %si
    mov $256, %cx
    rep movsb
    push %ds
    mov $0xb800, %ax
    mov %ax, %ds
    xor %si, %si
    mov $4000, %cx
    rep movsb
    pop %ds
    mov $0xc000, %si
    mov $256, %cx
    rep movsw
    mov $0xc200, %si
    mov $256, %cx
    rep movsw
    mov trace_handle, %bx
    mov $0xa000, %dx
    mov $5568, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $5568, %ax
    jne failed
    jmp next_case
finished:
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov trace_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21

service_hook:
    cmp $0x40, %ah
    jne chain
    incw %cs:calls
    cmpw $256, %cs:calls
    jbe log_count
    movw $5, %cs:violation
    jmp count_logged
log_count:
    push %bx
    mov %cs:calls, %bx
    dec %bx
    shl $1, %bx
    mov %cx, %cs:0xc000(%bx)
    pop %bx
count_logged:
    cmpw $0, %es:8(%di)
    je used_zero
    movw $1, %cs:violation
used_zero:
    cmp $128, %cx
    jbe count_valid
    movw $2, %cs:violation
count_valid:
    cmp %cs:target_handle, %bx
    je handle_valid
    movw $3, %cs:violation
handle_valid:
    push %ax
    push %bp
    mov %ds, %ax
    mov %cs, %bp
    add %cs:0x6810, %bp
    cmp %bp, %ax
    je segment_valid
    movw $4, %cs:violation
segment_valid:
    pop %bp
    pop %ax
    pushf
    push %cx
    push %si
    push %di
    push %es
    mov %cs:sent, %di
    add %cx, %di
    cmp $512, %di
    jbe payload_valid
    movw $6, %cs:violation
    jmp payload_done
payload_valid:
    sub %cx, %di
    add %cx, %cs:sent
    add $0xc200, %di
    mov %dx, %si
    push %cs
    pop %es
    cld
    rep movsb
payload_done:
    pop %es
    pop %di
    pop %si
    pop %cx
    popf
.if INJECTED == 1
    push %bp
    mov %sp, %bp
    andw $0xfffe, %ss:6(%bp)
    cmpw $0, %cs:0x6812
    je injected_success
    orw $1, %ss:6(%bp)
injected_success:
    mov %cs:0x6814, %ax
    pop %bp
    iret
.endif
chain:
    ljmp *%cs:old_vector
input_name: .asciz "CASES.BIN"
trace_name: .asciz "TRACE.BIN"
file_name: .asciz "OUTPUT.BIN"
input_handle: .word 0
trace_handle: .word 0
output_handle: .word 0
target_handle: .word 0
old_vector: .word 0,0
text_entry: .word 0x37,0
calls: .word 0
violation: .word 0
sent: .word 0
