.code16
# Oracle: unchanged 37B3 bytes, real DOS outputs or explicitly injected INT21 outcomes.
.global _start
.ifndef DISPATCH_KIND
.set DISPATCH_KIND, 0
.endif
.if DISPATCH_KIND == 0
.set TRACE_BYTES, 4140
.else
.set TRACE_BYTES, 4142
.endif
_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cli
    push %cs
    pop %ss
    mov $0xeff0, %sp
    sti
    cld
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
.if WRITE_MODE == 0
    mov $file_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, target_handle
.elseif WRITE_MODE == 1
    mov $null_name, %dx
    mov $0x3d02, %ax
    int $0x21
    jc failed
    mov %ax, target_handle
.else
    movw $0xffff, target_handle
.endif
    mov $0x3521, %ax
    int $0x21
    mov %bx, old_vector
    mov %es, old_vector+2
    push %cs
    pop %es
next_case:
    mov $0xeff0, %sp
    cld
    mov input_handle, %bx
    mov $input, %dx
    mov $4104, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finished
    cmp $4104, %ax
    jne failed
    mov $input+8, %si
    mov $0x8000, %di
    mov $4096, %cx
    rep movsb
    mov target_handle, %ax
    mov %ax, 0x8000
    mov input+6, %bx
    mov %cs, %ax
    add %bx, %ax
    mov %ax, 0x800e
    shl $4, %bx
    mov $0x8100, %ax
    sub %bx, %ax
    mov %ax, 0x800c
.if DISPATCH_KIND != 0
    movw $original, 0x8014
    movw $original, 0x8018
    mov %cs, %ax
    mov %ax, 0x8016
    mov %ax, 0x801a
    xor %ax, %ax
    cmpw $0, input+6
    je sticky_ready
    mov $0x55aa, %ax
sticky_ready:
    mov %ax, 0x6410
.endif
    movw $0, service_calls
    mov $service_hook, %dx
    mov $0x2521, %ax
    int $0x21
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
.if DISPATCH_KIND == 0
    push %cs
    push $0x8000
.endif
    mov $0x6789, %bp
    mov $0x369c, %dx
    mov $0x1357, %bx
    mov $0x2468, %cx
    mov $0x4567, %si
    mov $0x5678, %di
    mov $0x1234, %ax
.if DISPATCH_KIND == 0
    push %cs
    call original
.else
    mov $0x8000, %bx
    call original_dispatch
.endif
    mov %ax, snapshot
    mov %bx, snapshot+2
    mov %cx, snapshot+4
    mov %dx, snapshot+6
    mov %si, snapshot+8
    mov %di, snapshot+10
    mov %bp, snapshot+12
.if DISPATCH_KIND == 0
    movw $0xefe8, snapshot+14
.else
    movw $0xefee, snapshot+14
.endif
    mov %sp, snapshot+16
    mov %ds, snapshot+18
    mov %es, snapshot+20
    mov %ss, snapshot+22
    pushf
    popw snapshot+24
    mov %ss:0xeff0, %ax
    mov %ax, snapshot+26
    mov %ss:0xeff2, %ax
    mov %ax, snapshot+28
    mov %cs, %ax
    mov %ax, snapshot+30
    push %ds
    lds old_vector, %dx
    mov $0x2521, %ax
    int $0x21
    pop %ds
    cld
    mov $0x8000, %si
    mov $snapshot+32, %di
    mov $4096, %cx
    rep movsb
    mov $service_calls, %si
    mov $6, %cx
    rep movsw
.if DISPATCH_KIND != 0
    mov 0x6410, %ax
    stosw
.endif
    mov trace_handle, %bx
    mov $snapshot, %dx
    mov $TRACE_BYTES, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $TRACE_BYTES, %ax
    jne failed
    jmp next_case
finished:
.if WRITE_MODE < 2
    mov target_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
.endif
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
    incw %cs:service_calls
    mov %bx, %cs:service_handle
    mov %cx, %cs:service_count
    mov %dx, %cs:service_offset
    mov %ds, %cs:service_segment
    push %ax
    mov %es:8(%di), %ax
    mov %ax, %cs:service_used
    pop %ax
.if WRITE_MODE == 3
    push %bp
    mov %sp, %bp
    andw $0xfffe, %ss:6(%bp)
    cmpw $0, %cs:input+2
    je injected_success
    orw $1, %ss:6(%bp)
injected_success:
    mov %cs:input+4, %ax
    pop %bp
    iret
.endif
chain:
    ljmp *%cs:old_vector

input_name: .asciz "CASES.BIN"
trace_name: .asciz "TRACE.BIN"
file_name: .asciz "OUTPUT.BIN"
null_name: .asciz "NUL"
input_handle: .word 0
trace_handle: .word 0
target_handle: .word 0
old_vector: .word 0,0
service_calls: .word 0
service_handle: .word 0
service_count: .word 0
service_offset: .word 0
service_segment: .word 0
service_used: .word 0
original:
    .byte 0x8b,0xdc,0x1e,0x36,0xc4,0x7f,0x04,0x26,0xc5,0x55,0x0c
    .byte 0x33,0xc9,0x26,0x87,0x4d,0x08,0x26,0x8b,0x1d,0xb4,0x40
    .byte 0xcd,0x21,0x72,0x02,0x33,0xc0,0x1f,0xca,0x04,0x00
original_dispatch:
.if DISPATCH_KIND == 1
    .byte 0x06,0x53,0x26,0xff,0x5f,0x14,0x0b,0xc0,0x74,0x03,0xa3,0x10,0x64,0xc3
.elseif DISPATCH_KIND == 2
    .byte 0x06,0x53,0x26,0xff,0x5f,0x18,0x0b,0xc0,0x74,0x03,0xa3,0x10,0x64,0xc3
.endif
input: .space 4104
snapshot: .space 4142
