; FUN_24dd_3bde  entry=24dd:3bde size=37
24dd:3bde  MOV BX,SP
24dd:3be0  LES DI,SS:[BX + 0x4]
24dd:3be4  CALL 0x2000:89d3
24dd:3be7  JNZ 0x2000:89d0
24dd:3be9  MOV BX,word ptr ES:[DI]
24dd:3bec  CMP BX,0x4
24dd:3bef  JBE 0x2000:89ca
24dd:3bf1  MOV AH,0x3e
24dd:3bf3  INT 0x21
24dd:3bf5  JNC 0x2000:89ca
24dd:3bf7  MOV [0x6410],AX
24dd:3bfa  MOV word ptr ES:[DI + 0x2],0xd7b0
24dd:3c00  RETF 0x4
