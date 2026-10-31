; FUN_3de3_053f  entry=3de3:053f size=106
3de3:053f  PUSH BP
3de3:0540  MOV BP,SP
3de3:0542  MOV AX,0xc
3de3:0545  CALLF 0x4000:302f
3de3:054a  SUB SP,0xc
3de3:054d  LES DI,[BP + 0x8]
3de3:0550  PUSH ES
3de3:0551  PUSH DI
3de3:0552  CALL 0x3000:e254
3de3:0555  MOV word ptr [BP + -0x4],AX
3de3:0558  MOV word ptr [BP + -0x2],DX
3de3:055b  LES DI,[BP + 0x4]
3de3:055e  PUSH ES
3de3:055f  PUSH DI
3de3:0560  CALL 0x3000:e254
3de3:0563  MOV word ptr [BP + -0x8],AX
3de3:0566  MOV word ptr [BP + -0x6],DX
3de3:0569  MOV AX,word ptr [BP + -0x4]
3de3:056c  MOV DX,word ptr [BP + -0x2]
3de3:056f  CMP DX,word ptr [BP + -0x6]
3de3:0572  JL 0x3000:e3ab
3de3:0574  JG 0x3000:e3bd
3de3:0576  CMP AX,word ptr [BP + -0x8]
3de3:0579  JNC 0x3000:e3bd
3de3:057b  MOV AX,word ptr [BP + -0x4]
3de3:057e  MOV DX,word ptr [BP + -0x2]
3de3:0581  ADD AX,0x5180
3de3:0584  ADC DX,0x1
3de3:0587  MOV word ptr [BP + -0x4],AX
3de3:058a  MOV word ptr [BP + -0x2],DX
3de3:058d  MOV AX,word ptr [BP + -0x4]
3de3:0590  MOV DX,word ptr [BP + -0x2]
3de3:0593  SUB AX,word ptr [BP + -0x8]
3de3:0596  SBB DX,word ptr [BP + -0x6]
3de3:0599  PUSH DX
3de3:059a  PUSH AX
3de3:059b  LES DI,[BP + 0x8]
3de3:059e  PUSH ES
3de3:059f  PUSH DI
3de3:05a0  CALL 0x3000:e2c3
3de3:05a3  MOV SP,BP
3de3:05a5  POP BP
3de3:05a6  RET 0x8
