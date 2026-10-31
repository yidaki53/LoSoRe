; FUN_4170_034d  entry=4170:034d size=144
4170:034d  PUSH BP
4170:034e  MOV BP,SP
4170:0350  MOV AX,0x1c
4170:0353  CALLF 0x4000:302f
4170:0358  SUB SP,0x1c
4170:035b  MOV byte ptr [BP + -0x1b],0x42
4170:035f  MOV byte ptr [BP + -0x1c],0x1
4170:0363  MOV AX,word ptr [BP + 0x6]
4170:0366  MOV word ptr [BP + -0x1a],AX
4170:0369  XOR AX,AX
4170:036b  MOV word ptr [BP + -0x18],AX
4170:036e  XOR AX,AX
4170:0370  MOV word ptr [BP + -0x16],AX
4170:0373  LEA DI,[BP + -0x1c]
4170:0376  PUSH SS
4170:0377  PUSH DI
4170:0378  CALLF 0x4000:28f0
4170:037d  MOV AX,word ptr [BP + -0xa]
4170:0380  AND AX,0x1
4170:0383  OR AX,AX
4170:0385  JNZ 0x4000:1ac7
4170:0387  MOV AX,word ptr [BP + -0x16]
4170:038a  XOR DX,DX
4170:038c  MOV word ptr [BP + -0x8],AX
4170:038f  MOV word ptr [BP + -0x6],DX
4170:0392  MOV AX,word ptr [BP + -0x8]
4170:0395  MOV DX,word ptr [BP + -0x6]
4170:0398  XOR CX,CX
4170:039a  MOV BX,0x1
4170:039d  CALLF 0x4000:3664
4170:03a2  MOV word ptr [BP + -0x8],AX
4170:03a5  MOV word ptr [BP + -0x6],DX
4170:03a8  MOV AX,word ptr [BP + -0x1c]
4170:03ab  XOR DX,DX
4170:03ad  ADD AX,word ptr [BP + -0x8]
4170:03b0  ADC DX,word ptr [BP + -0x6]
4170:03b3  MOV word ptr [BP + -0x8],AX
4170:03b6  MOV word ptr [BP + -0x6],DX
4170:03b9  MOV AX,word ptr [BP + -0x8]
4170:03bc  MOV DX,word ptr [BP + -0x6]
4170:03bf  MOV word ptr [BP + -0x4],AX
4170:03c2  MOV word ptr [BP + -0x2],DX
4170:03c5  JMP 0x4000:1ad1
4170:03c7  MOV word ptr [BP + -0x4],0xffff
4170:03cc  MOV word ptr [BP + -0x2],0xffff
4170:03d1  MOV AX,word ptr [BP + -0x4]
4170:03d4  MOV DX,word ptr [BP + -0x2]
4170:03d7  MOV SP,BP
4170:03d9  POP BP
4170:03da  RETF 0x2
