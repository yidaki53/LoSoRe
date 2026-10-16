; FUN_24dd_3d68  entry=24dd:3d68 size=24
24dd:3d68  MOV BX,SP
24dd:3d6a  MOV DX,DS
24dd:3d6c  LDS SI,SS:[BX + 0xa]
24dd:3d70  LES DI,SS:[BX + 0x6]
24dd:3d74  MOV CX,word ptr SS:[BX + 0x4]
24dd:3d78  CLD
24dd:3d79  MOVSB.REP ES:DI,SI
24dd:3d7b  MOV DX,DS
24dd:3d7d  RETF 0xa
