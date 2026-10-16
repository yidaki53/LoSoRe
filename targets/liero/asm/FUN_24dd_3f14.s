; FUN_24dd_3f14  entry=24dd:3f14 size=44
24dd:3f14  CLD
24dd:3f15  MOV BX,SP
24dd:3f17  MOV DX,DS
24dd:3f19  LES DI,SS:[BX + 0x8]
24dd:3f1d  LDS SI,SS:[BX + 0x4]
24dd:3f21  MOV CL,byte ptr ES:[DI]
24dd:3f24  XOR CH,CH
24dd:3f26  LODSB SI
24dd:3f27  ADD byte ptr ES:[DI],AL
24dd:3f2a  JNC 0x2000:8d04
24dd:3f2c  MOV byte ptr ES:[DI],0xff
24dd:3f30  MOV AL,CL
24dd:3f32  NOT AL
24dd:3f34  ADD DI,CX
24dd:3f36  INC DI
24dd:3f37  MOV CL,AL
24dd:3f39  MOVSB.REP ES:DI,SI
24dd:3f3b  MOV DX,DS
24dd:3f3d  RETF 0x4
