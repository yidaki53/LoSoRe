; FUN_1000_0be1  entry=1000:0be1 size=158
1000:0be1  PUSH BP
1000:0be2  MOV BP,SP
1000:0be4  MOV AX,0x2
1000:0be7  CALLF 0x2000:5300
1000:0bec  SUB SP,0x2
1000:0bef  XOR AX,AX
1000:0bf1  MOV word ptr [BP + -0x2],AX
1000:0bf4  IMUL AX,word ptr [BP + -0x2],0x11
1000:0bf8  LES DI,[0x6690]
1000:0bfc  ADD DI,AX
1000:0bfe  CMP byte ptr ES:[DI],0x0
1000:0c02  JBE 0x1000:0c10
1000:0c04  CMP word ptr [BP + -0x2],0x2bc
1000:0c09  JGE 0x1000:0c10
1000:0c0b  INC word ptr [BP + -0x2]
1000:0c0e  JMP 0x1000:0bf4
1000:0c10  PUSH 0x2
1000:0c12  CALLF 0x2000:9424
1000:0c17  ADD AX,0x50
1000:0c1a  MOV DL,AL
1000:0c1c  IMUL AX,word ptr [BP + -0x2],0x11
1000:0c20  LES DI,[0x6690]
1000:0c24  ADD DI,AX
1000:0c26  MOV byte ptr ES:[DI],DL
1000:0c29  MOV DX,word ptr [BP + 0xe]
1000:0c2c  IMUL AX,word ptr [BP + -0x2],0x11
1000:0c30  LES DI,[0x6690]
1000:0c34  ADD DI,AX
1000:0c36  MOV word ptr ES:[DI + 0x3],DX
1000:0c3a  MOV DX,word ptr [BP + 0xc]
1000:0c3d  IMUL AX,word ptr [BP + -0x2],0x11
1000:0c41  LES DI,[0x6690]
1000:0c45  ADD DI,AX
1000:0c47  MOV word ptr ES:[DI + 0x7],DX
1000:0c4b  MOV CX,word ptr [BP + 0x8]
1000:0c4e  MOV BX,word ptr [BP + 0xa]
1000:0c51  IMUL AX,word ptr [BP + -0x2],0x11
1000:0c55  LES DI,[0x6690]
1000:0c59  ADD DI,AX
1000:0c5b  MOV word ptr ES:[DI + 0x9],CX
1000:0c5f  MOV word ptr ES:[DI + 0xb],BX
1000:0c63  MOV CX,word ptr [BP + 0x4]
1000:0c66  MOV BX,word ptr [BP + 0x6]
1000:0c69  IMUL AX,word ptr [BP + -0x2],0x11
1000:0c6d  LES DI,[0x6690]
1000:0c71  ADD DI,AX
1000:0c73  MOV word ptr ES:[DI + 0xd],CX
1000:0c77  MOV word ptr ES:[DI + 0xf],BX
1000:0c7b  LEAVE
1000:0c7c  RET 0xc
