; FUN_24dd_3c4f  entry=24dd:3c4f size=97
24dd:3c4f  MOV BL,0x40
24dd:3c51  MOV CX,0x65
24dd:3c54  PUSH BP
24dd:3c55  MOV BP,SP
24dd:3c57  LES DI,[BP + 0x10]
24dd:3c5a  CALL 0x2000:89d3
24dd:3c5d  JNZ 0x2000:8a6e
24dd:3c5f  MOV AX,word ptr [BP + 0xa]
24dd:3c62  OR AX,AX
24dd:3c64  JZ 0x2000:8a52
24dd:3c66  PUSH DS
24dd:3c67  PUSH CX
24dd:3c68  MUL word ptr ES:[DI + 0x4]
24dd:3c6c  MOV CX,AX
24dd:3c6e  LDS DX,[BP + 0xc]
24dd:3c71  MOV AH,BL
24dd:3c73  MOV BX,word ptr ES:[DI]
24dd:3c76  INT 0x21
24dd:3c78  POP CX
24dd:3c79  POP DS
24dd:3c7a  JC 0x2000:8a6b
24dd:3c7c  XOR DX,DX
24dd:3c7e  DIV word ptr ES:[DI + 0x4]
24dd:3c82  LES DI,[BP + 0x6]
24dd:3c85  MOV DX,ES
24dd:3c87  OR DX,DI
24dd:3c89  JZ 0x2000:8a60
24dd:3c8b  MOV word ptr ES:[DI],AX
24dd:3c8e  JMP 0x2000:8a7c
24dd:3c90  CMP AX,word ptr [BP + 0xa]
24dd:3c93  JZ 0x2000:8a7c
24dd:3c95  MOV word ptr [0x6410],CX
24dd:3c99  JMP 0x2000:8a7c
24dd:3c9b  MOV [0x6410],AX
24dd:3c9e  LES DI,[BP + 0x6]
24dd:3ca1  MOV DX,ES
24dd:3ca3  OR DX,DI
24dd:3ca5  JZ 0x2000:8a7c
24dd:3ca7  XOR AX,AX
24dd:3ca9  MOV word ptr ES:[DI],AX
24dd:3cac  POP BP
24dd:3cad  RETF 0xe
