; FUN_1000_0c8f  entry=1000:0c8f size=160
1000:0c8f  PUSH BP
1000:0c90  MOV BP,SP
1000:0c92  MOV AX,0x8
1000:0c95  CALLF 0x4000:302f
1000:0c9a  SUB SP,0x8
1000:0c9d  MOV byte ptr [BP + -0x1],0x1
1000:0ca1  MOV CX,word ptr [BP + 0x6]
1000:0ca4  MOV AX,0x50
1000:0ca7  MUL word ptr [BP + 0x4]
1000:0caa  MOV DI,AX
1000:0cac  ADD DI,CX
1000:0cae  CMP byte ptr [DI + 0x1f6f],0x0
1000:0cb3  JZ 0x1000:0cb7
1000:0cb5  JMP 0x1000:0d26
1000:0cb7  MOV word ptr [BP + -0x4],0x1
1000:0cbc  JMP 0x1000:0cc1
1000:0cbe  INC word ptr [BP + -0x4]
1000:0cc1  MOV AX,0x275
1000:0cc4  MUL word ptr [BP + -0x4]
1000:0cc7  MOV DI,AX
1000:0cc9  ADD DI,0x459
1000:0ccd  MOV word ptr [BP + -0x8],DI
1000:0cd0  MOV word ptr [BP + -0x6],DS
1000:0cd3  LES DI,[BP + -0x8]
1000:0cd6  CMP word ptr ES:[DI],0x0
1000:0cda  JZ 0x1000:0d1c
1000:0cdc  MOV AX,word ptr [BP + 0x6]
1000:0cdf  LES DI,[BP + -0x8]
1000:0ce2  CMP AX,word ptr ES:[DI]
1000:0ce5  JL 0x1000:0d1c
1000:0ce7  LES DI,[BP + -0x8]
1000:0cea  MOV AX,word ptr ES:[DI]
1000:0ced  LES DI,[BP + -0x8]
1000:0cf0  ADD AX,word ptr ES:[DI + 0xc]
1000:0cf4  DEC AX
1000:0cf5  CMP AX,word ptr [BP + 0x6]
1000:0cf8  JL 0x1000:0d1c
1000:0cfa  MOV AX,word ptr [BP + 0x4]
1000:0cfd  LES DI,[BP + -0x8]
1000:0d00  CMP AX,word ptr ES:[DI + 0x2]
1000:0d04  JL 0x1000:0d1c
1000:0d06  LES DI,[BP + -0x8]
1000:0d09  MOV AX,word ptr ES:[DI + 0x2]
1000:0d0d  LES DI,[BP + -0x8]
1000:0d10  ADD AX,word ptr ES:[DI + 0xe]
1000:0d14  DEC AX
1000:0d15  CMP AX,word ptr [BP + 0x4]
1000:0d18  JL 0x1000:0d1c
1000:0d1a  JMP 0x1000:0d26
1000:0d1c  CMP word ptr [BP + -0x4],0xa
1000:0d20  JNZ 0x1000:0cbe
1000:0d22  MOV byte ptr [BP + -0x1],0x0
1000:0d26  MOV AL,byte ptr [BP + -0x1]
1000:0d29  MOV SP,BP
1000:0d2b  POP BP
1000:0d2c  RET 0x4
