; FUN_24dd_40d6  entry=24dd:40d6 size=22
24dd:40d6  CLD
24dd:40d7  MOV BX,SP
24dd:40d9  LES DI,SS:[BX + 0x6]
24dd:40dd  MOV AX,word ptr SS:[BX + 0x4]
24dd:40e1  STOSW ES:DI
24dd:40e2  MOV CX,0xf
24dd:40e5  XOR AX,AX
24dd:40e7  STOSW.REP ES:DI
24dd:40e9  RETF 0x2
