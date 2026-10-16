; FUN_1000_0c7f  entry=1000:0c7f size=241
1000:0c7f  PUSH BP
1000:0c80  MOV BP,SP
1000:0c82  MOV AX,0xe
1000:0c85  CALLF 0x2000:5300
1000:0c8a  SUB SP,0xe
1000:0c8d  MOV AX,word ptr [BP + 0xa]
1000:0c90  SUB AX,word ptr [BP + 0xe]
1000:0c93  MOV word ptr [BP + -0x3],AX
1000:0c96  MOV AX,word ptr [BP + 0x8]
1000:0c99  SUB AX,word ptr [BP + 0xc]
1000:0c9c  MOV word ptr [BP + -0x5],AX
1000:0c9f  MOV AX,word ptr [BP + 0x6]
1000:0ca2  SUB AX,word ptr [BP + 0xe]
1000:0ca5  MOV word ptr [BP + -0x7],AX
1000:0ca8  MOV AX,word ptr [BP + 0x4]
1000:0cab  SUB AX,word ptr [BP + 0xc]
1000:0cae  MOV word ptr [BP + -0x9],AX
1000:0cb1  MOV byte ptr [BP + -0x1],0x1
1000:0cb5  MOV AX,word ptr [BP + -0x3]
1000:0cb8  CWD
1000:0cb9  XOR AX,DX
1000:0cbb  SUB AX,DX
1000:0cbd  CMP AX,0xa0
1000:0cc0  JG 0x1000:0cd2
1000:0cc2  MOV AX,word ptr [BP + -0x5]
1000:0cc5  CWD
1000:0cc6  XOR AX,DX
1000:0cc8  SUB AX,DX
1000:0cca  CMP AX,0xa0
1000:0ccd  JG 0x1000:0cd2
1000:0ccf  JMP 0x1000:0d65
1000:0cd2  MOV AX,word ptr [BP + -0x7]
1000:0cd5  CWD
1000:0cd6  XOR AX,DX
1000:0cd8  SUB AX,DX
1000:0cda  CMP AX,0xa0
1000:0cdd  JG 0x1000:0cec
1000:0cdf  MOV AX,word ptr [BP + -0x9]
1000:0ce2  CWD
1000:0ce3  XOR AX,DX
1000:0ce5  SUB AX,DX
1000:0ce7  CMP AX,0xa0
1000:0cea  JLE 0x1000:0d65
1000:0cec  MOV AX,word ptr [BP + 0xe]
1000:0cef  ADD AX,0x3
1000:0cf2  MOV word ptr [BP + -0xb],AX
1000:0cf5  MOV AX,word ptr [BP + 0xe]
1000:0cf8  SUB AX,0x3
1000:0cfb  CMP AX,word ptr [BP + -0xb]
1000:0cfe  JG 0x1000:0d63
1000:0d00  MOV word ptr [BP + -0x3],AX
1000:0d03  JMP 0x1000:0d08
1000:0d05  INC word ptr [BP + -0x3]
1000:0d08  MOV AX,word ptr [BP + 0xc]
1000:0d0b  ADD AX,0x4
1000:0d0e  MOV word ptr [BP + -0xd],AX
1000:0d11  MOV AX,word ptr [BP + 0xc]
1000:0d14  SUB AX,0x4
1000:0d17  CMP AX,word ptr [BP + -0xd]
1000:0d1a  JG 0x1000:0d5b
1000:0d1c  MOV word ptr [BP + -0x5],AX
1000:0d1f  JMP 0x1000:0d24
1000:0d21  INC word ptr [BP + -0x5]
1000:0d24  MOV DX,word ptr [BP + -0x3]
1000:0d27  MOV AX,word ptr [BP + -0x5]
1000:0d2a  SHL AX,0x2
1000:0d2d  LES DI,[0x6674]
1000:0d31  ADD DI,AX
1000:0d33  LES DI,ES:[DI]
1000:0d36  ADD DI,DX
1000:0d38  MOV AL,byte ptr ES:[DI]
1000:0d3b  MOV AH,0x1
1000:0d3d  MOV DX,0x20
1000:0d40  CALLF 0x2000:8f31
1000:0d45  MOV DI,DX
1000:0d47  TEST byte ptr [DI + 0x14a0],AL
1000:0d4b  JZ 0x1000:0d53
1000:0d4d  MOV byte ptr [BP + -0x1],0x0
1000:0d51  JMP 0x1000:0d69
1000:0d53  MOV AX,word ptr [BP + -0x5]
1000:0d56  CMP AX,word ptr [BP + -0xd]
1000:0d59  JNZ 0x1000:0d21
1000:0d5b  MOV AX,word ptr [BP + -0x3]
1000:0d5e  CMP AX,word ptr [BP + -0xb]
1000:0d61  JNZ 0x1000:0d05
1000:0d63  JMP 0x1000:0d69
1000:0d65  MOV byte ptr [BP + -0x1],0x0
1000:0d69  MOV AL,byte ptr [BP + -0x1]
1000:0d6c  LEAVE
1000:0d6d  RET 0xc
