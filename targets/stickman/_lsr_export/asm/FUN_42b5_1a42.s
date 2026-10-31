; FUN_42b5_1a42  entry=42b5:1a42 size=20
42b5:1a42  MOV BX,SP
42b5:1a44  LES DI,SS:[BX + 0x8]
42b5:1a48  MOV CX,word ptr SS:[BX + 0x6]
42b5:1a4c  MOV AL,byte ptr SS:[BX + 0x4]
42b5:1a50  CLD
42b5:1a51  STOSB.REP ES:DI
42b5:1a53  RETF 0x8
