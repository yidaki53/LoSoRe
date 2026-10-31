; FUN_410e_032f  entry=410e:032f size=43
410e:032f  MOV BX,SP
410e:0331  PUSH DS
410e:0332  LDS DI,SS:[BX + 0x4]
410e:0336  MOV word ptr [DI + 0x2],0xd7b0
410e:033b  MOV word ptr [DI + 0x4],0x80
410e:0340  LEA AX,[DI + 0x80]
410e:0344  MOV word ptr [DI + 0xc],AX
410e:0347  MOV word ptr [DI + 0xe],DS
410e:034a  MOV word ptr [DI + 0x10],0x35a
410e:034f  MOV word ptr [DI + 0x12],CS
410e:0352  MOV byte ptr [DI + 0x30],0x0
410e:0356  POP DS
410e:0357  RETF 0x4
