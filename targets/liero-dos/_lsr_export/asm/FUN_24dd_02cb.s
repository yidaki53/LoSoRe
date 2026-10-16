; FUN_24dd_02cb  entry=24dd:02cb size=28
24dd:02cb  MOV BX,SP
24dd:02cd  LES DI,SS:[BX + 0x4]
24dd:02d1  LES DI,ES:[DI]
24dd:02d4  MOV word ptr [0x63ee],DI
24dd:02d8  MOV word ptr [0x63f0],ES
24dd:02dc  MOV word ptr [0x63f6],DI
24dd:02e0  MOV word ptr [0x63f8],ES
24dd:02e4  RETF 0x4
