; FUN_3de3_0bea  entry=3de3:0bea size=61
3de3:0bea  PUSH BP
3de3:0beb  MOV BP,SP
3de3:0bed  MOV AX,0x100
3de3:0bf0  CALLF 0x4000:302f
3de3:0bf5  SUB SP,0x100
3de3:0bf9  LES DI,[BP + 0x6]
3de3:0bfc  PUSH ES
3de3:0bfd  PUSH DI
3de3:0bfe  LEA DI,[BP + 0xff00]
3de3:0c02  PUSH SS
3de3:0c03  PUSH DI
3de3:0c04  MOV AX,0xff
3de3:0c07  PUSH AX
3de3:0c08  CALLF 0x4000:372e
3de3:0c0d  PUSH word ptr [BP + 0xc]
3de3:0c10  PUSH word ptr [BP + 0xa]
3de3:0c13  PUSH CS
3de3:0c14  CALL 0x3000:e997
3de3:0c17  LEA DI,[BP + 0xff00]
3de3:0c1b  PUSH SS
3de3:0c1c  PUSH DI
3de3:0c1d  PUSH CS
3de3:0c1e  CALL 0x3000:de5d
3de3:0c21  MOV SP,BP
3de3:0c23  POP BP
3de3:0c24  RETF 0x8
