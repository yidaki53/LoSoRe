; FUN_24dd_4905  entry=24dd:4905 size=20
24dd:4905  MOV BX,SP
24dd:4907  LES DI,SS:[BX + 0x8]
24dd:490b  MOV CX,word ptr SS:[BX + 0x6]
24dd:490f  MOV AL,byte ptr SS:[BX + 0x4]
24dd:4913  CLD
24dd:4914  STOSB.REP ES:DI
24dd:4916  RETF 0x8
