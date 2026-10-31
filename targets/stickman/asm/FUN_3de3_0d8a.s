; FUN_3de3_0d8a  entry=3de3:0d8a size=184
3de3:0d8a  PUSH BP
3de3:0d8b  MOV BP,SP
3de3:0d8d  MOV AX,0x104
3de3:0d90  CALLF 0x4000:302f
3de3:0d95  SUB SP,0x104
3de3:0d99  MOV DI,0xd79
3de3:0d9c  PUSH CS
3de3:0d9d  PUSH DI
3de3:0d9e  PUSH CS
3de3:0d9f  CALL 0x3000:de5d
3de3:0da2  PUSH CS
3de3:0da3  CALL 0x3000:e892
3de3:0da6  OR AL,AL
3de3:0da8  JZ 0x3000:ebdd
3de3:0daa  JMP 0x3000:ec65
3de3:0dad  PUSH CS
3de3:0dae  CALL 0x3000:e6fd
3de3:0db1  INC word ptr [0x14e]
3de3:0db5  MOV AL,[0x150]
3de3:0db8  XOR AH,AH
3de3:0dba  CMP AX,word ptr [0x14e]
3de3:0dbe  JGE 0x3000:ebf6
3de3:0dc0  MOV word ptr [0x14e],0x1
3de3:0dc6  LEA DI,[BP + 0xfefc]
3de3:0dca  PUSH SS
3de3:0dcb  PUSH DI
3de3:0dcc  MOV DI,word ptr [0x14e]
3de3:0dd0  MOV AL,byte ptr [DI + 0x150]
3de3:0dd4  PUSH AX
3de3:0dd5  CALLF 0x4000:3844
3de3:0dda  MOV DI,0xd84
3de3:0ddd  PUSH CS
3de3:0dde  PUSH DI
3de3:0ddf  CALLF 0x4000:37a1
3de3:0de4  PUSH CS
3de3:0de5  CALL 0x3000:de5d
3de3:0de8  CALLF 0x4000:1796
3de3:0ded  MOV word ptr [BP + -0x4],AX
3de3:0df0  MOV word ptr [BP + -0x2],DX
3de3:0df3  CALLF 0x4000:1796
3de3:0df8  CMP DX,word ptr [BP + -0x2]
3de3:0dfb  JG 0x3000:ec34
3de3:0dfd  JL 0x3000:ec62
3de3:0dff  CMP AX,word ptr [BP + -0x4]
3de3:0e02  JC 0x3000:ec62
3de3:0e04  CALLF 0x4000:1796
3de3:0e09  MOV CX,AX
3de3:0e0b  MOV BX,DX
3de3:0e0d  MOV AX,word ptr [BP + -0x4]
3de3:0e10  MOV DX,word ptr [BP + -0x2]
3de3:0e13  ADD AX,0x2
3de3:0e16  ADC DX,0x0
3de3:0e19  CMP DX,BX
3de3:0e1b  JG 0x3000:ec53
3de3:0e1d  JL 0x3000:ec62
3de3:0e1f  CMP AX,CX
3de3:0e21  JC 0x3000:ec62
3de3:0e23  PUSH CS
3de3:0e24  CALL 0x3000:e892
3de3:0e27  OR AL,AL
3de3:0e29  JNZ 0x3000:ec62
3de3:0e2b  CALLF 0x4000:076d
3de3:0e30  JMP 0x3000:ec23
3de3:0e32  JMP 0x3000:ebd2
3de3:0e35  MOV DI,0xd88
3de3:0e38  PUSH CS
3de3:0e39  PUSH DI
3de3:0e3a  PUSH CS
3de3:0e3b  CALL 0x3000:de5d
3de3:0e3e  MOV SP,BP
3de3:0e40  POP BP
3de3:0e41  RETF
