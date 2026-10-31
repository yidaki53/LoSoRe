.code16
# Oracle: original-byte DOSBox execution; not normal game startup or Pascal parity.
.section .text
.global _start

.macro object_arg
    lea -0x104(%bp), %di
    push %ss
    push %di
.endm

.macro original target
    push %cs
    call \target
.endm

.macro capture event
    mov $\event, %ax
    call snapshot
.endm

.macro read_string
    object_arg
    lea -0x204(%bp), %di
    push %ss
    push %di
    push $255
    original 0x3988
.endm

_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    mov %sp, %bp
    sub $0x206, %sp
    cld
    mov $0, %ax
    mov $0x6410, %di
    stosw
    lea -0x204(%bp), %di
    mov $256, %cx
    rep stosw
    mov %cs, %ax
    mov $fixups, %si
    mov $5, %cx
1:
    lodsw
    mov %ax, %di
    mov %cs, %ax
    mov %ax, (%di)
    loop 1b

    object_arg
    mov $input_name, %di
    push %cs
    push %di
    original 0x3639
    capture 1
    object_arg
    original 0x36b7
.ifdef CLOSE_HANDLER_PROBE
    movw $0x55aa, -0xfc(%bp)
    movw $0xffff, -0xfa(%bp)
    push %cs
    pop %es
    lea -0x84(%bp), %di
    mov $0xa5a5, %ax
    mov $64, %cx
    rep stosw
    lea -0x204(%bp), %di
    mov $0x5a5a, %ax
    mov $128, %cx
    rep stosw
.endif
.ifdef DISPATCH_HANDLER_PROBE
    movw $0x0400, -0xec(%bp)
    mov %cs, %ax
    mov %ax, -0xea(%bp)
.endif
.ifdef WRAPPERS_HANDLER_PROBE
    movw $0x0400, -0xec(%bp)
    mov %cs, %ax
    mov %ax, -0xea(%bp)
.endif
.ifdef SETUP_HANDLER_PROBE
    mov $setup_name, %si
    lea -0xd4(%bp), %di
    mov $80, %cx
    rep movsb
.endif
.ifdef CALLBACKS_HANDLER_PROBE
    object_arg
    original 0x375e
    or %ax, %ax
    jnz failed
.endif
    capture 2
    cmpw $0, 0x6410
    jne save_trace
    .ifdef WRAPPERS_HANDLER_PROBE
        movw $3, wrapper_stage
    wrapper_case:
        testw $1, wrapper_stage
        jz wrapper_skip
        read_string
        jmp wrapper_capture
    wrapper_skip:
        original 0x38f0
    wrapper_capture:
        mov wrapper_stage, %ax
        call snapshot
        incw wrapper_stage
        cmpw $7, wrapper_stage
        jne wrapper_case
        jmp save_trace
    .endif
    .ifdef BUFFER_HANDLER_PROBE
    movw $3, buffer_stage
buffer_case:
    push %cs
    pop %es
    lea -0x204(%bp), %di
    mov $0xa5a5, %ax
    mov $128, %cx
    rep stosw
    mov buffer_stage, %ax
    sub $3, %ax
    shr $1, %ax
    shl $1, %ax
    mov %ax, %bx
    mov buffer_limits(%bx), %cx
    mov $0x39ab, %ax
    testw $1, buffer_stage
    jnz buffer_callback_selected
    mov $0x390e, %ax
buffer_callback_selected:
.if READ_CAPACITY == 1
    cmpw $3, buffer_stage
    jne buffer_valid_handle
    movw $0xffff, -0x104(%bp)
buffer_valid_handle:
.endif
    cmpw $9, buffer_stage
    jne buffer_not_sticky
    movw $0x55aa, 0x6410
buffer_not_sticky:
    cmpw $10, buffer_stage
    jne buffer_mode_selected
    movw $0, 0x6410
    movw $0x1212, -0x102(%bp)
buffer_mode_selected:
    mov $0xbeef, %si
    lea -0x204(%bp), %di
    lea -0x104(%bp), %bx
    mov %cs, %dx
    call 0x37ec
    pushf
    pop %dx
    mov %ax, -0xde(%bp)
    mov %si, -0xe4(%bp)
    lea -0x204(%bp), %ax
    sub %ax, %di
    mov %di, -0xe2(%bp)
    mov %cx, -0xe0(%bp)
    and $0x40, %dx
    shr $6, %dx
    mov %dx, -0xdc(%bp)
    mov buffer_stage, %ax
    call snapshot
    incw buffer_stage
    cmpw $11, buffer_stage
    jne buffer_case
    jmp save_trace
.endif
.ifdef CALLBACKS_HANDLER_PROBE
    mov $3, %ax
    mov %ax, callback_stage
callback_case:
    push %cs
    pop %es
    lea -0x204(%bp), %di
    mov $0xa5a5, %ax
    mov $128, %cx
    rep stosw
    lea -0x84(%bp), %si
    mov %si, %bx
    add -0xfa(%bp), %bx
    lea -0x204(%bp), %di
    mov callback_stage, %ax
    sub $3, %ax
    shr $1, %ax
    shl $1, %ax
    push %bx
    mov %ax, %bx
    mov callback_limits(%bx), %cx
    pop %bx
    testw $1, callback_stage
    jz callback_skip
    call 0x39ab
    jmp callback_returned
callback_skip:
    call 0x390e
callback_returned:
    mov %ax, 0x6410
    mov %ax, -0x106(%bp)
    lea -0x84(%bp), %dx
    sub %dx, %si
    mov %si, -0x10c(%bp)
    lea -0x204(%bp), %dx
    sub %dx, %di
    mov %di, -0x10a(%bp)
    mov %cx, -0x108(%bp)
    mov callback_stage, %ax
    call snapshot
    incw callback_stage
    cmpw $11, callback_stage
    jne callback_case
    jmp save_trace
.endif
.ifdef OPEN_HANDLER_PROBE
    mov -0x104(%bp), %ax
    mov %ax, opened_handle
    movw $0x55aa, 0x6410
    mov $3, %si
open_case:
    cmp $4, %si
    je open_invalidate
    cmp $7, %si
    jne open_not_invalidated
open_invalidate:
    mov opened_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    movw $0xffff, -0x104(%bp)
open_not_invalidated:
    cmp $5, %si
    jne open_not_missing
    mov $missing_name, %bx
    call copy_open_name
open_not_missing:
    cmp $6, %si
    jne open_not_existing
    mov $existing_name, %bx
    call copy_open_name
open_not_existing:
    cmp $9, %si
    jne open_not_bad_mode
    movw $0x1234, -0x102(%bp)
open_not_bad_mode:
    cmp $10, %si
    jne open_not_empty
    movw $0xd7b0, -0x102(%bp)
    mov $empty_name, %bx
    call copy_open_name
open_not_empty:
    movw $0x55aa, -0xfc(%bp)
    movw $0xffff, -0xfa(%bp)
    object_arg
    cmp $7, %si
    je open_close
    cmp $8, %si
    je open_close
    original 0x36b7
    jmp open_capture
open_close:
    original 0x3711
open_capture:
    mov %si, %ax
    call snapshot
    inc %si
    cmp $11, %si
    jne open_case
.else
.ifdef SETUP_HANDLER_PROBE
    mov -0x104(%bp), %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $3, %si
setup_case:
    movw $0xbeef, -0x104(%bp)
    movw $0x55aa, -0xfc(%bp)
    movw $0xffff, -0xfa(%bp)
    lea -0xf0(%bp), %di
    mov $0xa5a5, %ax
    mov $6, %cx
    rep stosw
    object_arg
    original 0x420c
    mov %ax, 0x6410
    cmpb $0, -0xd4(%bp)
    je setup_no_open
    incw open_calls
setup_no_open:
    mov open_calls, %ax
    mov %ax, -0x204(%bp)
    mov %si, %ax
    call snapshot
    cmpw $0, 0x6410
    jne setup_next
    cmpb $0, -0xd4(%bp)
    je setup_next
    mov -0x104(%bp), %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
setup_next:
    inc %si
    cmp $11, %si
    jne setup_case
.else
.ifdef DISPATCH_HANDLER_PROBE
    movw $0x55aa, 0x6410
    mov $3, %si
dispatch_case:
    mov $0x1c, %bx
    cmp $3, %si
    je dispatch_read
    cmp $7, %si
    je dispatch_read
    jmp dispatch_selected
dispatch_read:
    mov $0x14, %bx
dispatch_selected:
    cmp $6, %si
    jne dispatch_not_reserved
    movw $4, -0x104(%bp)
dispatch_not_reserved:
    cmp $7, %si
    jne dispatch_not_invalid
    movw $0xffff, -0x104(%bp)
dispatch_not_invalid:
    cmp $8, %si
    jb dispatch_call
    mov $0x18, %bx
    mov $0x1234, %ax
    cmp $8, %si
    je dispatch_synthetic_return
    xor %ax, %ax
    cmp $9, %si
    je dispatch_synthetic_return
    mov $0xffff, %ax
dispatch_synthetic_return:
    mov %ax, synthetic_return
dispatch_call:
    push %ss
    pop %es
    lea -0x104(%bp), %di
    call 0x374d
    pushf
    pop %dx
    mov %ax, -0x204(%bp)
    mov %es, %ax
    mov %ax, -0x202(%bp)
    mov %di, -0x200(%bp)
    and $0x40, %dx
    shr $6, %dx
    mov %dx, -0x1fe(%bp)
    mov %si, %ax
    call snapshot
    inc %si
    cmp $11, %si
    jne dispatch_case
.else
.ifdef CLOSE_HANDLER_PROBE
    mov -0x104(%bp), %ax
    mov %ax, opened_handle
    mov $3, %si
close_handler_case:
    mov %si, %ax
    sub $3, %ax
    cmp $7, %si
    jbe selected_handle
    mov opened_handle, %ax
    cmp $10, %si
    jne selected_handle
    mov $0xffff, %ax
selected_handle:
.ifdef CLOSE_BOUNDARY_PROBE
    cmp $7, %si
    ja close_boundary_selected
    mov %si, %bx
    sub $3, %bx
    shl $1, %bx
    mov close_boundary_handles(%bx), %ax
close_boundary_selected:
.endif
    mov %ax, -0x104(%bp)
    object_arg
    original 0x37d3
    mov %ax, 0x6410
    mov %si, %ax
    call snapshot
    inc %si
    cmp $11, %si
    jne close_handler_case
.ifdef CLOSE_BOUNDARY_PROBE
    jmp close_boundary_table_end
close_boundary_handles:
    .word 6, 7, 255, 0x8000, 0xfffe
close_boundary_table_end:
.endif
.else
.ifdef READ_HANDLER_PROBE
    movw $READ_CAPACITY, -0x100(%bp)
    mov $3, %si
read_handler_case:
    cmp $10, %si
    jne valid_read
    movw $0xffff, -0x104(%bp)
valid_read:
    movw $0x55aa, -0xfc(%bp)
    movw $0xffff, -0xfa(%bp)
    object_arg
    original 0x375e
    mov %ax, 0x6410
    mov %si, %ax
    call snapshot
    inc %si
    cmp $11, %si
    jne read_handler_case
.else
    read_string
    capture 3
    original 0x38f0
    capture 4
    read_string
    capture 5
    original 0x38f0
    capture 6
    object_arg
    original 0x36b7
    capture 7
    cmpw $0, 0x6410
    jne save_trace
    read_string
    capture 8
    original 0x38f0
    capture 9
    object_arg
    original 0x3711
    capture 10
.endif
.endif
.endif
.endif
.endif

save_trace:
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $0x8000, %dx
    mov snapshot_end, %cx
    sub %dx, %cx
    mov %cx, output_count
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp output_count, %ax
    jne failed
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21

snapshot:
    pushf
    pusha
    push %ds
    push %es
    push %cs
    pop %es
    mov snapshot_end, %di
    stosw
    mov %cs, %ax
    stosw
    mov %ds, %ax
    stosw
    mov %ss, %ax
    stosw
    mov %bp, %ax
    stosw
    mov %sp, %ax
    add $24, %ax
    stosw
    mov %sp, %bx
    mov %ss:20(%bx), %ax
    stosw
    mov 0x6410, %ax
    stosw
    lea -0x104(%bp), %ax
    stosw
    lea -0x204(%bp), %ax
    stosw
    push %ss
    pop %ds
    lea -0x104(%bp), %si
    mov $128, %cx
    rep movsw
    lea -0x204(%bp), %si
    mov $128, %cx
    rep movsw
    push %cs
    pop %ds
    mov %di, snapshot_end
    pop %es
    pop %ds
    popa
    popf
    ret

snapshot_end: .word 0x8000
output_count: .word 0
opened_handle: .word 0
synthetic_return: .word 0
.ifdef WRAPPERS_HANDLER_PROBE
wrapper_stage: .word 0
.endif
.ifdef BUFFER_HANDLER_PROBE
buffer_stage: .word 0
buffer_limits: .word 7, 111, 1, 111
.endif
.ifdef CALLBACKS_HANDLER_PROBE
callback_stage: .word 0
callback_limits: .word 0, 1, 7, 255
.endif
input_name: .byte 9
    .ascii "INPUT.TXT"
output_name: .asciz "TRACE.BIN"
fixups: .word 0x3663, 0x4241, 0x425c, 0x4272, 0x4291

.ifdef OPEN_HANDLER_PROBE
copy_open_name:
    push %si
    mov %bx, %si
    push %cs
    pop %es
    lea -0xd4(%bp), %di
    mov $80, %cx
    rep movsb
    pop %si
    ret
existing_name: .asciz "INPUT.TXT"
    .fill 70, 1, 0
missing_name: .asciz "MISSING.TXT"
    .fill 68, 1, 0
empty_name: .fill 80, 1, 0
.endif

.ifdef SETUP_HANDLER_PROBE
open_calls: .word 0
setup_name:
.if READ_CAPACITY == 0
    .byte 0
.elseif READ_CAPACITY == 1
    .asciz "MISSING.TXT"
.elseif READ_CAPACITY == 2
    .asciz "NO_DIR/INPUT.TXT"
.else
    .asciz "INPUT.TXT"
.endif
    .fill 80-(.-setup_name), 1, 0
.endif

.ifdef DISPATCH_HANDLER_PROBE
    .org 0x300
synthetic_method:
    # Oracle: synthetic far callback, NOT a recovered Liero method.
    mov %sp, %bx
    les %ss:4(%bx), %di
    incw %es:6(%di)
    mov $0xbeef, %di
    mov $0x1234, %ax
    mov %ax, %es
    mov %cs:synthetic_return, %ax
    lret $4
.endif
.ifdef WRAPPERS_HANDLER_PROBE
    .org 0x300
synthetic_wrapper_method:
    # Oracle: bounded synthetic optional method, not a recovered Liero method.
    mov $WRAPPER_METHOD_RETURN, %ax
    lret $4
.endif
