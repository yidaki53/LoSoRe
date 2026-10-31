; FUN_1000_2d1f  entry=1000:2d1f size=310
1000:2d1f  PUSH BP
1000:2d20  MOV BP,SP
1000:2d22  MOV AX,0x10c
1000:2d25  CALLF 0x4000:302f
1000:2d2a  SUB SP,0x10c
1000:2d2e  MOV word ptr [BP + -0x8],0xb418
1000:2d33  MOV word ptr [BP + -0xa],0x1baf
1000:2d38  MOV AL,[0x32]
1000:2d3b  MOV byte ptr [BP + 0xfef6],AL
1000:2d3f  MOV AL,byte ptr [BP + 0xfef6]
1000:2d43  XOR AH,AH
1000:2d45  MOV word ptr [BP + 0xfef4],AX
1000:2d49  MOV AX,0x1
1000:2d4c  CMP AX,word ptr [BP + 0xfef4]
1000:2d50  JG 0x1000:2da7
1000:2d52  MOV word ptr [BP + -0x4],AX
1000:2d55  JMP 0x1000:2d5a
1000:2d57  INC word ptr [BP + -0x4]
1000:2d5a  MOV AX,word ptr [BP + -0xa]
1000:2d5d  MOV word ptr [BP + -0x6],AX
1000:2d60  MOV AX,word ptr [BP + -0x8]
1000:2d63  ADD AX,word ptr [BP + -0xa]
1000:2d66  MOV word ptr [BP + -0xa],AX
1000:2d69  MOV AX,word ptr [BP + -0x6]
1000:2d6c  MOV word ptr [BP + -0x8],AX
1000:2d6f  MOV DI,word ptr [BP + -0x4]
1000:2d72  MOV AL,byte ptr [DI + 0x32]
1000:2d76  XOR AL,byte ptr [BP + -0xa]
1000:2d79  MOV DI,word ptr [BP + -0x4]
1000:2d7c  MOV byte ptr [BP + DI + 0xfef6],AL
1000:2d80  MOV DI,word ptr [BP + -0x4]
1000:2d83  CMP byte ptr [BP + DI + 0xfef6],0x1b
1000:2d88  JC 0x1000:2d94
1000:2d8a  MOV DI,word ptr [BP + -0x4]
1000:2d8d  CMP byte ptr [BP + DI + 0xfef6],0x7e
1000:2d92  JBE 0x1000:2d9e
1000:2d94  MOV DI,0x2d04
1000:2d97  PUSH CS
1000:2d98  PUSH DI
1000:2d99  CALLF 0x3000:e0a8
1000:2d9e  MOV AX,word ptr [BP + -0x4]
1000:2da1  CMP AX,word ptr [BP + 0xfef4]
1000:2da5  JNZ 0x1000:2d57
1000:2da7  MOV AX,0x1c
1000:2daa  PUSH AX
1000:2dab  MOV AX,0x12
1000:2dae  PUSH AX
1000:2daf  LEA DI,[BP + 0xfef6]
1000:2db3  PUSH SS
1000:2db4  PUSH DI
1000:2db5  CALLF 0x3000:ea1a
1000:2dba  MOV byte ptr [BP + -0x1],0x5e
1000:2dbe  MOV word ptr [BP + -0x8],0xe557
1000:2dc3  MOV word ptr [BP + -0xa],0x14cd
1000:2dc8  MOV AL,[0x8]
1000:2dcb  MOV byte ptr [BP + 0xfef6],AL
1000:2dcf  MOV AL,byte ptr [BP + 0xfef6]
1000:2dd3  XOR AH,AH
1000:2dd5  MOV word ptr [BP + 0xfef4],AX
1000:2dd9  MOV AX,0x1
1000:2ddc  CMP AX,word ptr [BP + 0xfef4]
1000:2de0  JG 0x1000:2e2e
1000:2de2  MOV word ptr [BP + -0x4],AX
1000:2de5  JMP 0x1000:2dea
1000:2de7  INC word ptr [BP + -0x4]
1000:2dea  MOV AX,word ptr [BP + -0xa]
1000:2ded  MOV word ptr [BP + -0x6],AX
1000:2df0  MOV AX,word ptr [BP + -0x8]
1000:2df3  ADD AX,word ptr [BP + -0xa]
1000:2df6  MOV word ptr [BP + -0xa],AX
1000:2df9  MOV AX,word ptr [BP + -0x6]
1000:2dfc  MOV word ptr [BP + -0x8],AX
1000:2dff  MOV DI,word ptr [BP + -0x4]
1000:2e02  MOV AL,byte ptr [DI + 0x8]
1000:2e06  XOR AL,byte ptr [BP + -0xa]
1000:2e09  MOV DI,word ptr [BP + -0x4]
1000:2e0c  MOV byte ptr [BP + DI + 0xfef6],AL
1000:2e10  MOV DI,word ptr [BP + -0x4]
1000:2e13  MOV AL,byte ptr [BP + DI + 0xfef6]
1000:2e17  XOR AH,AH
1000:2e19  MOV DX,AX
1000:2e1b  MOV AL,byte ptr [BP + -0x1]
1000:2e1e  XOR AH,AH
1000:2e20  ADD AX,DX
1000:2e22  MOV byte ptr [BP + -0x1],AL
1000:2e25  MOV AX,word ptr [BP + -0x4]
1000:2e28  CMP AX,word ptr [BP + 0xfef4]
1000:2e2c  JNZ 0x1000:2de7
1000:2e2e  CMP byte ptr [BP + -0x1],0xc9
1000:2e32  JZ 0x1000:2e3e
1000:2e34  MOV DI,0x2d04
1000:2e37  PUSH CS
1000:2e38  PUSH DI
1000:2e39  CALLF 0x3000:e0a8
1000:2e3e  MOV AX,0x15
1000:2e41  PUSH AX
1000:2e42  MOV AX,0x16
1000:2e45  PUSH AX
1000:2e46  LEA DI,[BP + 0xfef6]
1000:2e4a  PUSH SS
1000:2e4b  PUSH DI
1000:2e4c  CALLF 0x3000:ea1a
1000:2e51  MOV SP,BP
1000:2e53  POP BP
1000:2e54  RET
