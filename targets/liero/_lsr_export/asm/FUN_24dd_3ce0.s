; FUN_24dd_3ce0  entry=24dd:3ce0 size=79
24dd:3ce0  PUSH BP
24dd:3ce1  MOV BP,SP
24dd:3ce3  MOV DX,word ptr [BP + 0x6]
24dd:3ce6  OR DX,DX
24dd:3ce8  JZ 0x2000:8abf
24dd:3cea  CALL 0x2000:8b06
24dd:3ced  JMP 0x2000:8aef
24dd:3cef  MOV AH,0x30
24dd:3cf1  INT 0x21
24dd:3cf3  CMP AL,0x3
24dd:3cf5  MOV AX,0x0
24dd:3cf8  JC 0x2000:8aef
24dd:3cfa  MOV ES,word ptr [0x640c]
24dd:3cfe  MOV ES,word ptr ES:[0x2c]
24dd:3d03  XOR DI,DI
24dd:3d05  CLD
24dd:3d06  CMP AL,byte ptr ES:[DI]
24dd:3d09  JZ 0x2000:8ae2
24dd:3d0b  MOV CX,0xffff
24dd:3d0e  SCASB.REPNE ES:DI
24dd:3d10  JMP 0x2000:8ad6
24dd:3d12  ADD DI,0x3
24dd:3d15  MOV SI,DI
24dd:3d17  MOV CX,0x100
24dd:3d1a  SCASB.REPNE ES:DI
24dd:3d1c  XCHG AX,CX
24dd:3d1d  NOT AL
24dd:3d1f  PUSH DS
24dd:3d20  PUSH ES
24dd:3d21  POP DS
24dd:3d22  LES DI,[BP + 0x8]
24dd:3d25  CLD
24dd:3d26  STOSB ES:DI
24dd:3d27  XCHG AX,CX
24dd:3d28  MOVSB.REP ES:DI,SI
24dd:3d2a  POP DS
24dd:3d2b  POP BP
24dd:3d2c  RETF 0x2
