; FUN_3de3_0424  entry=3de3:0424 size=111
3de3:0424  PUSH BP
3de3:0425  MOV BP,SP
3de3:0427  MOV AX,0x14
3de3:042a  CALLF 0x4000:302f
3de3:042f  SUB SP,0x14
3de3:0432  LES DI,[BP + 0x4]
3de3:0435  PUSH ES
3de3:0436  PUSH DI
3de3:0437  LEA DI,[BP + -0x10]
3de3:043a  PUSH SS
3de3:043b  PUSH DI
3de3:043c  MOV AX,0xc
3de3:043f  PUSH AX
3de3:0440  CALLF 0x4000:3648
3de3:0445  MOV AX,word ptr [BP + -0xa]
3de3:0448  XOR DX,DX
3de3:044a  MOV word ptr [BP + -0x14],AX
3de3:044d  MOV word ptr [BP + -0x12],DX
3de3:0450  MOV AX,word ptr [BP + -0x14]
3de3:0453  MOV DX,word ptr [BP + -0x12]
3de3:0456  MOV CX,0xe10
3de3:0459  XOR BX,BX
3de3:045b  CALLF 0x4000:3664
3de3:0460  MOV word ptr [BP + -0x14],AX
3de3:0463  MOV word ptr [BP + -0x12],DX
3de3:0466  MOV AX,word ptr [BP + -0x6]
3de3:0469  XOR DX,DX
3de3:046b  MOV CX,AX
3de3:046d  MOV BX,DX
3de3:046f  MOV AX,0x3c
3de3:0472  MUL word ptr [BP + -0x8]
3de3:0475  XOR DX,DX
3de3:0477  ADD AX,word ptr [BP + -0x14]
3de3:047a  ADC DX,word ptr [BP + -0x12]
3de3:047d  ADD AX,CX
3de3:047f  ADC DX,BX
3de3:0481  MOV word ptr [BP + -0x4],AX
3de3:0484  MOV word ptr [BP + -0x2],DX
3de3:0487  MOV AX,word ptr [BP + -0x4]
3de3:048a  MOV DX,word ptr [BP + -0x2]
3de3:048d  MOV SP,BP
3de3:048f  POP BP
3de3:0490  RET 0x4
