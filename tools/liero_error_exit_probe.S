.code16
.ifndef OPEN_OUTPUT
.set OPEN_OUTPUT, 0
.endif
.ifndef TEXT_ERROR
.set TEXT_ERROR, 0
.endif
.global _start
_start:
    jmp setup
.org 0x1000-0x100
setup:
    mov %cs, %ax
    mov %ax, %cs:0x11b
    cmp $0xdfff, %ax
    ja failed
    mov %ax, %dx
    add $0x1000, %dx
    cmp %es:2, %dx
    ja failed
    cli
    mov %ax, %ss
    mov $0xeff0, %sp
    sti
    mov %ax, %ds
    mov %ax, %es
    mov %ax, record
    mov $0x63d8, %di
    mov $58, %cx
    mov $0xa5, %al
    cld
    rep stosb
    xor %ax, %ax
    mov %ax, 0x63e4
    mov %ax, 0x6402
    mov %ax, 0x6404
    push %ax
    mov $0x78f0, %di
    mov $588, %cx
    rep stosb
    pop %ax
    mov %cs, %ax
    sub $16, %ax
    mov %ax, 0x640c
    movw $0xd7b0, 0x78f2
    movw $0xd7b0, 0x79f2
    movw $ERROR_CODE, 0x6410
.if TEXT_ERROR
    movw $0, 0x6410
    movw $0x0a0d, 0x6424
    mov %cs, %ax
    mov %ax, %cs:0x314e
    mov %ax, %cs:0x3153
    add $0x300, %ax
    mov %ax, text_pointer+2
    mov $3, %ax
    int $0x10
    mov $0xb800, %ax
    mov %ax, %es
    xor %di, %di
    mov $2000, %cx
    mov $0x4f2e, %ax
    rep stosw
    push %cs
    pop %es
    xor %ax, %ax
    mov $0x8200, %di
    mov $256, %cx
    rep stosb
    movb $5, 0x8200
    movb $0x41, 0x8201
    movb $0, 0x8202
    movb $2, 0x8203
    movb $3, 0x8204
    movb $0x42, 0x8205
.endif
.if OPEN_OUTPUT
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
.if SCENARIO == 1
    mov %ax, %bx
    mov $0x3e00, %ax
    int $0x21
    mov $0xffff, %ax
.endif
    mov %ax, open_record
    mov %ax, 0x79f0
    movw $0xd7b1, 0x78f2
    movw $0x37d3, 0x790c
    movw $0xd7b2, 0x79f2
    movw $128, 0x79f4
    movw $USED, 0x79f8
    movw $0x7a70, 0x79fc
    movw $0x37b3, 0x7a04
.if TEXT_ERROR
    movw $0x37b3, 0x7a08
.endif
    movw $0x37d3, 0x7a0c
    mov %cs, %ax
    mov %ax, 0x790e
    mov %ax, 0x79fe
    mov %ax, 0x7a06
.if TEXT_ERROR
    mov %ax, 0x7a0a
.endif
    mov %ax, 0x7a0e
    mov $0x7a70, %di
    mov $128, %cx
    mov $0x41, %al
    rep stosb
.endif
    mov $0x3521, %ax
    int $0x21
    mov %bx, old21
    mov %es, old21+2
    push %cs
    pop %ds
    mov $hook21, %dx
    mov $0x2521, %ax
    int $0x21
    mov $0x239, %si
    mov $0x7af0, %di
    mov $19, %cx
save_vectors:
    lodsb %cs:(%si), %al
    mov $0x35, %ah
    int $0x21
    mov %bx, (%di)
    mov %es, 2(%di)
    add $4, %di
    loop save_vectors
    movw $CALLER_OFFSET, 0xeff0
.if CALLER_OFFSET
    mov %cs, %ax
    add $0x200, %ax
.else
    xor %ax, %ax
.endif
    mov %ax, 0xeff2
    mov %cs, %ax
    mov %ax, %ds
    mov %ax, %es
    mov $0x6789, %bp
    mov $ERROR_CODE, %ax
.if TEXT_ERROR
    mov $0xdff0, %sp
    mov $3, %ax
    push %ax
    mov $2, %ax
    push %ax
    push %ds
    mov $0x8200, %ax
    push %ax
    lcall *%cs:text_pointer
    jmp failed
.else
.if ERROR_CHECK
    jmp 0x4f4
.else
    jmp 0x10f
.endif
.endif
failed:
    mov $0x4cff, %ax
    int $0x21
hook21:
.if OPEN_OUTPUT
    cmp $0x40, %ah
    je write_buffer
    cmp $0x3e, %ah
    je close_handle
.endif
    cmp $0x06, %ah
    je output_byte
    cmp $0x25, %ah
    je restore_vector
    cmp $0x4c, %ah
    je terminating
chain:
    ljmp *%cs:old21
.if OPEN_OUTPUT
write_buffer:
.if TEXT_ERROR
    cmpw $0, %cs:open_record+2
    jne write_record
    mov %cx, %cs:first_write
    push %ax
    mov %es:2(%di), %ax
    mov %ax, %cs:first_write+2
    mov %es:8(%di), %ax
    mov %ax, %cs:first_write+4
    pop %ax
    push %ds
    push %es
    push %si
    push %di
    push %cx
    push %cs
    pop %es
    mov $0xb800, %ax
    mov %ax, %ds
    xor %si, %si
    mov $video_before_error, %di
    mov $4000, %cx
    rep movsb
    push %cs
    pop %ds
    mov $0x8200, %si
    mov $input_copy, %di
    mov $256, %cx
    rep movsb
    pop %cx
    pop %di
    pop %si
    pop %es
    pop %ds
    mov $0x4000, %ax
write_record:
.endif
    incw %cs:open_record+2
    mov %cx, %cs:open_record+6
    mov %ds, %cs:open_record+18
    mov %dx, %cs:open_record+20
    push %ax
    mov %es:2(%di), %ax
    mov %ax, %cs:open_record+8
    mov %es:8(%di), %ax
    mov %ax, %cs:open_record+10
    pop %ax
    movw $1, %cs:open_record+22
    push %si
    push %di
    push %cx
    push %es
    mov %dx, %si
    push %cs
    pop %es
    mov $attempted, %di
    cmp $128, %cx
    ja failed
    rep movsb
    pop %es
    pop %cx
    pop %di
    pop %si
.if SCENARIO < 2
    jmp chain
.else
    mov %cx, %ax
.if (SCENARIO == 2) || (SCENARIO == 4)
    mov $5, %ax
    jmp injected_error
.else
    jmp injected_success
.endif
.endif
close_handle:
    incw %cs:open_record+4
    mov %bx, %cs:open_record+16
    push %ax
    mov %es:2(%di), %ax
    mov %ax, %cs:open_record+12
    mov %es:8(%di), %ax
    mov %ax, %cs:open_record+14
    pop %ax
    shlw $4, %cs:open_record+22
    orw $2, %cs:open_record+22
.if SCENARIO < 2
    jmp chain
.else
.if SCENARIO >= 3
    mov $6, %ax
    jmp injected_error
.else
    xor %ax, %ax
    jmp injected_success
.endif
.endif
injected_error:
    push %bp
    mov %sp, %bp
    orw $1, %ss:6(%bp)
    pop %bp
    iret
injected_success:
    push %bp
    mov %sp, %bp
    andw $0xfffe, %ss:6(%bp)
    pop %bp
    iret
.endif
output_byte:
    push %bx
    mov %cs:output_count, %bx
    cmp $128, %bx
    jae failed
    mov %dl, %cs:output_bytes(%bx)
    incw %cs:output_count
    pop %bx
    jmp chain
restore_vector:
    push %bx
    mov %cs:restore_count, %bx
    cmp $19, %bx
    jae failed
    mov %al, %cs:restored_ids(%bx)
    incw %cs:restore_count
    pop %bx
    jmp chain
terminating:
    mov %ax, %cs:record+2
    mov %ds, %cs:record+4
    mov %ss, %cs:record+6
    mov %sp, %cs:record+8
    mov %bp, %cs:record+10
    mov %cs, %ax
    mov %ax, %ds
    mov %ax, %es
    mov $0x63d8, %si
    mov $global_copy, %di
    mov $58, %cx
    cld
    rep movsb
    mov $0x78f0, %si
    mov $objects, %di
    mov $588, %cx
    rep movsb
    mov $0x239, %si
    mov $restored_vectors, %di
    mov $19, %cx
read_restored:
    lodsb %cs:(%si), %al
    mov $0x35, %ah
    pushf
    lcall *%cs:old21
    mov %bx, (%di)
    mov %es, 2(%di)
    add $4, %di
    loop read_restored
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    pushf
    lcall *%cs:old21
    jc failed
    mov %ax, %bx
    mov $record, %dx
    mov $(record_end-record), %cx
    mov $0x4000, %ax
    pushf
    lcall *%cs:old21
    jc failed
    cmp $(record_end-record), %ax
    jne failed
    mov $0x3e00, %ax
    pushf
    lcall *%cs:old21
    jc failed
    mov %cs:old21, %dx
    mov %cs:old21+2, %ds
    mov $0x2521, %ax
    pushf
    lcall *%cs:old21
    mov %cs:record+2, %ax
    ljmp *%cs:old21
old21: .space 4
filename: .asciz "TRACE.BIN"
.if OPEN_OUTPUT
output_name: .asciz "OUTPUT.BIN"
.endif
.if TEXT_ERROR
text_pointer: .word 0x37, 0
.endif
record: .space 12
restore_count: .word 0
output_count: .word 0
global_copy: .space 58
objects: .space 588
restored_ids: .space 19
restored_vectors: .space 76
output_bytes: .space 128
.if OPEN_OUTPUT
open_record: .space 24
attempted: .space 128
.endif
.if TEXT_ERROR
first_write: .space 6
video_before_error: .space 4000
input_copy: .space 256
.endif
record_end:
