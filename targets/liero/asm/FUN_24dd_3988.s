; FUN_24dd_3988  entry=24dd:3988 size=35
24dd:3988  PUSH BP
24dd:3989  MOV BP,SP
24dd:398b  LES BX,[BP + 0xc]
24dd:398e  MOV AX,0x39ab
24dd:3991  MOV CX,word ptr [BP + 0x6]
24dd:3994  MOV DI,word ptr [BP + 0x8]
24dd:3997  MOV DX,word ptr [BP + 0xa]
24dd:399a  INC DI
24dd:399b  CALL 0x2000:85bc
24dd:399e  MOV AX,DI
24dd:39a0  LES DI,[BP + 0x8]
24dd:39a3  SUB AX,DI
24dd:39a5  DEC AX
24dd:39a6  STOSB ES:DI
24dd:39a7  POP BP
24dd:39a8  RETF 0x6
