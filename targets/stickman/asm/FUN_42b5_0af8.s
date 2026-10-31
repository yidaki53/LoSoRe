; FUN_42b5_0af8  entry=42b5:0af8 size=24
42b5:0af8  MOV BX,SP
42b5:0afa  MOV DX,DS
42b5:0afc  LDS SI,SS:[BX + 0xa]
42b5:0b00  LES DI,SS:[BX + 0x6]
42b5:0b04  MOV CX,word ptr SS:[BX + 0x4]
42b5:0b08  CLD
42b5:0b09  MOVSB.REP ES:DI,SI
42b5:0b0b  MOV DX,DS
42b5:0b0d  RETF 0xa
