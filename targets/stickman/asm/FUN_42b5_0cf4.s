; FUN_42b5_0cf4  entry=42b5:0cf4 size=18
42b5:0cf4  CLD
42b5:0cf5  MOV BX,SP
42b5:0cf7  LES DI,SS:[BX + 0x6]
42b5:0cfb  MOV AL,0x1
42b5:0cfd  STOSB ES:DI
42b5:0cfe  MOV AL,byte ptr SS:[BX + 0x4]
42b5:0d02  STOSB ES:DI
42b5:0d03  RETF 0x2
