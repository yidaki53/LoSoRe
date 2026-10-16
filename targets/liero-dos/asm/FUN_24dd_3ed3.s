; FUN_24dd_3ed3  entry=24dd:3ed3 size=65
24dd:3ed3  CLD
24dd:3ed4  MOV BX,SP
24dd:3ed6  MOV DX,DS
24dd:3ed8  LES DI,SS:[BX + 0xc]
24dd:3edc  LDS SI,SS:[BX + 0x8]
24dd:3ee0  MOV AL,byte ptr [SI]
24dd:3ee2  XOR AH,AH
24dd:3ee4  MOV CX,word ptr SS:[BX + 0x6]
24dd:3ee8  OR CX,CX
24dd:3eea  JG 0x2000:8cbf
24dd:3eec  MOV CX,0x1
24dd:3eef  ADD SI,CX
24dd:3ef1  SUB AX,CX
24dd:3ef3  JC 0x2000:8cd8
24dd:3ef5  INC AX
24dd:3ef6  MOV CX,word ptr SS:[BX + 0x4]
24dd:3efa  OR CX,CX
24dd:3efc  JGE 0x2000:8cd0
24dd:3efe  XOR CX,CX
24dd:3f00  CMP AX,CX
24dd:3f02  JBE 0x2000:8cda
24dd:3f04  MOV AX,CX
24dd:3f06  JMP 0x2000:8cda
24dd:3f08  XOR AX,AX
24dd:3f0a  STOSB ES:DI
24dd:3f0b  MOV CX,AX
24dd:3f0d  MOVSB.REP ES:DI,SI
24dd:3f0f  MOV DX,DS
24dd:3f11  RETF 0x8
