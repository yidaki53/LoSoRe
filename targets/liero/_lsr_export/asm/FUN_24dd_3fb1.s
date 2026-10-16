; FUN_24dd_3fb1  entry=24dd:3fb1 size=18
24dd:3fb1  CLD
24dd:3fb2  MOV BX,SP
24dd:3fb4  LES DI,SS:[BX + 0x6]
24dd:3fb8  MOV AL,0x1
24dd:3fba  STOSB ES:DI
24dd:3fbb  MOV AL,byte ptr SS:[BX + 0x4]
24dd:3fbf  STOSB ES:DI
24dd:3fc0  RETF 0x2
