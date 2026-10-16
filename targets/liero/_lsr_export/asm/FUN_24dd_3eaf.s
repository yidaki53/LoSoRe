; FUN_24dd_3eaf  entry=24dd:3eaf size=36
24dd:3eaf  CLD
24dd:3eb0  MOV BX,SP
24dd:3eb2  MOV DX,DS
24dd:3eb4  LDS SI,SS:[BX + 0xa]
24dd:3eb8  LES DI,SS:[BX + 0x6]
24dd:3ebc  MOV CX,word ptr SS:[BX + 0x4]
24dd:3ec0  LODSB SI
24dd:3ec1  CMP AL,CL
24dd:3ec3  JBE 0x2000:8c97
24dd:3ec5  MOV AL,CL
24dd:3ec7  STOSB ES:DI
24dd:3ec8  MOV CL,AL
24dd:3eca  XOR CH,CH
24dd:3ecc  MOVSB.REP ES:DI,SI
24dd:3ece  MOV DX,DS
24dd:3ed0  RETF 0xa
