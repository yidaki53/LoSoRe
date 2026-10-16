; FUN_24dd_3a4b  entry=24dd:3a4b size=52
24dd:3a4b  PUSH BP
24dd:3a4c  MOV BP,SP
24dd:3a4e  SUB SP,0x20
24dd:3a51  MOV AX,word ptr [BP + 0x8]
24dd:3a54  MOV DX,word ptr [BP + 0xa]
24dd:3a57  LEA DI,[BP + 0x0]
24dd:3a5a  PUSH SS
24dd:3a5b  POP ES
24dd:3a5c  CALL 0x2000:94c6
24dd:3a5f  LES BX,[BP + 0xc]
24dd:3a62  MOV DX,word ptr [BP + 0x6]
24dd:3a65  SUB DX,CX
24dd:3a67  JLE 0x2000:8840
24dd:3a69  PUSH CX
24dd:3a6a  PUSH DI
24dd:3a6b  CALL 0x2000:861a
24dd:3a6e  POP DI
24dd:3a6f  POP CX
24dd:3a70  MOV AX,CX
24dd:3a72  MOV SI,DI
24dd:3a74  MOV DX,SS
24dd:3a76  CALL 0x2000:8669
24dd:3a79  MOV SP,BP
24dd:3a7b  POP BP
24dd:3a7c  RETF 0x6
