; FUN_24dd_0e57  entry=24dd:0e57 size=135
24dd:0e57  PUSH DX
24dd:0e58  PUSH SI
24dd:0e59  MOV DX,word ptr [SI + 0x6]
24dd:0e5c  AND DX,0x7fff
24dd:0e60  OR DX,word ptr [SI]
24dd:0e62  OR DX,word ptr [SI + 0x2]
24dd:0e65  OR DX,word ptr [SI + 0x4]
24dd:0e68  JNZ 0x2000:5c5b
24dd:0e6a  CMP BX,-0x1
24dd:0e6d  JZ 0x2000:5c57
24dd:0e6f  CMP word ptr [BX + 0x8],0x4001
24dd:0e74  JL 0x2000:5c57
24dd:0e76  MOV DX,word ptr [BX + 0x6]
24dd:0e79  AND DX,0x7fff
24dd:0e7d  OR DX,word ptr [BX]
24dd:0e7f  OR DX,word ptr [BX + 0x2]
24dd:0e82  OR DX,word ptr [BX + 0x4]
24dd:0e85  JNZ 0x2000:5c9c
24dd:0e87  CLC
24dd:0e88  POP SI
24dd:0e89  POP DX
24dd:0e8a  RET
24dd:0e8b  CMP BX,-0x1
24dd:0e8e  JZ 0x2000:5c9e
24dd:0e90  CMP word ptr [BX + 0x8],0x4001
24dd:0e95  JL 0x2000:5c9e
24dd:0e97  MOV DX,word ptr [BX + 0x6]
24dd:0e9a  AND DX,0x7fff
24dd:0e9e  OR DX,word ptr [BX]
24dd:0ea0  OR DX,word ptr [BX + 0x2]
24dd:0ea3  OR DX,word ptr [BX + 0x4]
24dd:0ea6  JZ 0x2000:5c9e
24dd:0ea8  MOV DX,word ptr [SI + 0x6]
24dd:0eab  CMP DX,word ptr [BX + 0x6]
24dd:0eae  JA 0x2000:5c9e
24dd:0eb0  JC 0x2000:5c9c
24dd:0eb2  MOV DX,word ptr [SI + 0x4]
24dd:0eb5  CMP DX,word ptr [BX + 0x4]
24dd:0eb8  JA 0x2000:5c9e
24dd:0eba  JC 0x2000:5c9c
24dd:0ebc  MOV DX,word ptr [SI + 0x2]
24dd:0ebf  CMP DX,word ptr [BX + 0x2]
24dd:0ec2  JA 0x2000:5c9e
24dd:0ec4  JC 0x2000:5c9c
24dd:0ec6  MOV DX,word ptr [SI]
24dd:0ec8  CMP DX,word ptr [BX]
24dd:0eca  JA 0x2000:5c9e
24dd:0ecc  MOV SI,BX
24dd:0ece  PUSH DI
24dd:0ecf  MOV CH,0x1
24dd:0ed1  CALL 0x2000:7131
24dd:0ed4  MOV CX,0x6
24dd:0ed7  CLD
24dd:0ed8  MOVSW.REP ES:DI,SI
24dd:0eda  STC
24dd:0edb  POP DI
24dd:0edc  JMP 0x2000:5c58
