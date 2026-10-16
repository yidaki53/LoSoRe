; FUN_24dd_3fc3  entry=24dd:3fc3 size=27
24dd:3fc3  CLD
24dd:3fc4  MOV BX,SP
24dd:3fc6  MOV DX,DS
24dd:3fc8  LES DI,SS:[BX + 0xa]
24dd:3fcc  LDS SI,SS:[BX + 0x6]
24dd:3fd0  MOV AX,word ptr SS:[BX + 0x4]
24dd:3fd4  STOSB ES:DI
24dd:3fd5  MOV CX,AX
24dd:3fd7  MOVSB.REP ES:DI,SI
24dd:3fd9  MOV DX,DS
24dd:3fdb  RETF 0x6
