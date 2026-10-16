; FUN_24dd_3b66  entry=24dd:3b66 size=92
24dd:3b66  MOV AX,0x3c00
24dd:3b69  MOV DX,0x1
24dd:3b6c  PUSH BP
24dd:3b6d  MOV BP,SP
24dd:3b6f  LES DI,[BP + 0x8]
24dd:3b72  CMP word ptr ES:[DI + 0x2],0xd7b0
24dd:3b78  JZ 0x2000:8964
24dd:3b7a  CMP word ptr ES:[DI + 0x2],0xd7b3
24dd:3b80  JZ 0x2000:895a
24dd:3b82  MOV word ptr [0x6410],0x66
24dd:3b88  JMP 0x2000:898e
24dd:3b8a  PUSH AX
24dd:3b8b  PUSH DX
24dd:3b8c  PUSH ES
24dd:3b8d  PUSH DI
24dd:3b8e  PUSH CS
24dd:3b8f  CALL 0x2000:89ae
24dd:3b92  POP DX
24dd:3b93  POP AX
24dd:3b94  CMP byte ptr ES:[DI + 0x30],0x0
24dd:3b99  JZ 0x2000:897d
24dd:3b9b  PUSH DS
24dd:3b9c  LEA DX,[DI + 0x30]
24dd:3b9f  PUSH ES
24dd:3ba0  POP DS
24dd:3ba1  XOR CX,CX
24dd:3ba3  INT 0x21
24dd:3ba5  POP DS
24dd:3ba6  JNC 0x2000:897e
24dd:3ba8  MOV [0x6410],AX
24dd:3bab  JMP 0x2000:898e
24dd:3bad  XCHG AX,DX
24dd:3bae  MOV word ptr ES:[DI + 0x2],0xd7b3
24dd:3bb4  MOV word ptr ES:[DI],AX
24dd:3bb7  MOV AX,word ptr [BP + 0x6]
24dd:3bba  MOV word ptr ES:[DI + 0x4],AX
24dd:3bbe  POP BP
24dd:3bbf  RETF 0x6
