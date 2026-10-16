; FUN_24dd_0ee2  entry=24dd:0ee2 size=453
24dd:0ee2  MOV CL,0x0
24dd:0ee4  PUSH BP
24dd:0ee5  MOV BP,SP
24dd:0ee7  LEA SP,[BP + -0x6]
24dd:0eea  PUSH SI
24dd:0eeb  PUSH DI
24dd:0eec  MOV SI,word ptr [BP + 0x8]
24dd:0eef  MOV DI,word ptr [BP + 0x6]
24dd:0ef2  MOV AL,CL
24dd:0ef4  XOR AL,byte ptr [DI + 0xa]
24dd:0ef7  XOR AL,byte ptr [SI + 0xa]
24dd:0efa  MOV byte ptr [BP + -0x6],AL
24dd:0efd  MOV AX,word ptr [SI + 0x8]
24dd:0f00  MOV BX,word ptr [DI + 0x8]
24dd:0f03  CMP AX,0x4001
24dd:0f06  JGE 0x2000:5d11
24dd:0f08  CMP BX,0x4001
24dd:0f0c  JGE 0x2000:5d2e
24dd:0f0e  CMP AX,BX
24dd:0f10  JGE 0x2000:5cea
24dd:0f12  XOR CL,byte ptr [DI + 0xa]
24dd:0f15  XCHG AX,BX
24dd:0f16  XCHG DI,SI
24dd:0f18  JMP 0x2000:5ced
24dd:0f1a  MOV CL,byte ptr [SI + 0xa]
24dd:0f1d  MOV byte ptr [BP + -0x5],CL
24dd:0f20  MOV CX,word ptr [SI + 0x8]
24dd:0f23  MOV word ptr [BP + -0x4],CX
24dd:0f26  CMP BX,0xc001
24dd:0f2a  JLE 0x2000:5d03
24dd:0f2c  SUB AX,BX
24dd:0f2e  CMP AX,0x40
24dd:0f31  JLE 0x2000:5d58
24dd:0f33  MOV AX,word ptr [SI]
24dd:0f35  MOV BX,word ptr [SI + 0x2]
24dd:0f38  MOV CX,word ptr [SI + 0x4]
24dd:0f3b  MOV DX,word ptr [SI + 0x6]
24dd:0f3e  JMP 0x2000:5e3b
24dd:0f41  PUSH BX
24dd:0f42  PUSH DI
24dd:0f43  MOV BX,DI
24dd:0f45  MOV DI,word ptr [BP + 0x4]
24dd:0f48  CALL 0x2000:5c27
24dd:0f4b  POP DI
24dd:0f4c  POP BX
24dd:0f4d  JC 0x2000:5d55
24dd:0f4f  CMP BX,0x4001
24dd:0f53  JL 0x2000:5d42
24dd:0f55  MOV AL,byte ptr [BP + -0x6]
24dd:0f58  OR AL,AL
24dd:0f5a  JNZ 0x2000:5d4f
24dd:0f5c  JMP 0x2000:5d42
24dd:0f5e  MOV BX,0xffff
24dd:0f61  MOV AL,byte ptr [DI + 0xa]
24dd:0f64  XOR AL,CL
24dd:0f66  MOV SI,DI
24dd:0f68  MOV DI,word ptr [BP + 0x4]
24dd:0f6b  CALL 0x2000:5c27
24dd:0f6e  JC 0x2000:5d55
24dd:0f70  JMP 0x2000:5d45
24dd:0f72  MOV AL,byte ptr [SI + 0xa]
24dd:0f75  MOV byte ptr [BP + -0x5],AL
24dd:0f78  MOV word ptr [BP + -0x4],0x4001
24dd:0f7d  JMP 0x2000:5d03
24dd:0f7f  MOV DI,word ptr [BP + 0x4]
24dd:0f82  CALL 0x2000:53df
24dd:0f85  JMP 0x2000:5e4e
24dd:0f88  MOV byte ptr [BP + -0x1],AL
24dd:0f8b  MOV AX,word ptr [DI]
24dd:0f8d  MOV BX,word ptr [DI + 0x2]
24dd:0f90  MOV CX,word ptr [DI + 0x4]
24dd:0f93  MOV DX,word ptr [DI + 0x6]
24dd:0f96  MOV byte ptr [BP + -0x2],0x0
24dd:0f9a  SUB byte ptr [BP + -0x1],0x8
24dd:0f9e  JL 0x2000:5d89
24dd:0fa0  MOV byte ptr [BP + -0x2],AL
24dd:0fa3  MOV AL,AH
24dd:0fa5  MOV AH,BL
24dd:0fa7  MOV BL,BH
24dd:0fa9  MOV BH,CL
24dd:0fab  MOV CL,CH
24dd:0fad  MOV CH,DL
24dd:0faf  MOV DL,DH
24dd:0fb1  MOV DH,0x0
24dd:0fb3  SUB byte ptr [BP + -0x1],0x8
24dd:0fb7  JGE 0x2000:5d70
24dd:0fb9  AND byte ptr [BP + -0x1],0x7
24dd:0fbd  JZ 0x2000:5d9f
24dd:0fbf  SHR DX,0x1
24dd:0fc1  RCR CX,0x1
24dd:0fc3  RCR BX,0x1
24dd:0fc5  RCR AX,0x1
24dd:0fc7  RCR byte ptr [BP + -0x2],0x1
24dd:0fca  DEC byte ptr [BP + -0x1]
24dd:0fcd  JNZ 0x2000:5d8f
24dd:0fcf  SUB DI,DI
24dd:0fd1  CMP byte ptr [BP + -0x6],0x0
24dd:0fd5  JNZ 0x2000:5dc4
24dd:0fd7  ADD AX,word ptr [SI]
24dd:0fd9  ADC BX,word ptr [SI + 0x2]
24dd:0fdc  ADC CX,word ptr [SI + 0x4]
24dd:0fdf  ADC DX,word ptr [SI + 0x6]
24dd:0fe2  JNC 0x2000:5e1b
24dd:0fe4  RCR DX,0x1
24dd:0fe6  RCR CX,0x1
24dd:0fe8  RCR BX,0x1
24dd:0fea  RCR AX,0x1
24dd:0fec  RCR byte ptr [BP + -0x2],0x1
24dd:0fef  INC word ptr [BP + -0x4]
24dd:0ff2  JMP 0x2000:5e1b
24dd:0ff4  XOR byte ptr [BP + -0x5],0x1
24dd:0ff8  SUB AX,word ptr [SI]
24dd:0ffa  SBB BX,word ptr [SI + 0x2]
24dd:0ffd  SBB CX,word ptr [SI + 0x4]
24dd:1000  SBB DX,word ptr [SI + 0x6]
24dd:1003  JNC 0x2000:5ded
24dd:1005  XOR byte ptr [BP + -0x5],0x1
24dd:1009  NOT DX
24dd:100b  NOT CX
24dd:100d  NOT BX
24dd:100f  NOT AX
24dd:1011  NEG byte ptr [BP + -0x2]
24dd:1014  CMC
24dd:1015  ADC AX,DI
24dd:1017  ADC BX,DI
24dd:1019  ADC CX,DI
24dd:101b  ADC DX,DI
24dd:101d  MOV SI,0x40
24dd:1020  OR DH,DH
24dd:1022  JS 0x2000:5e1b
24dd:1024  DEC SI
24dd:1025  JZ 0x2000:5e0c
24dd:1027  SHL byte ptr [BP + -0x2],0x1
24dd:102a  RCL AX,0x1
24dd:102c  RCL BX,0x1
24dd:102e  RCL CX,0x1
24dd:1030  ADC DX,DX
24dd:1032  JNS 0x2000:5df4
24dd:1034  SUB SI,0x40
24dd:1037  ADD word ptr [BP + -0x4],SI
24dd:103a  JMP 0x2000:5e1b
24dd:103c  OR DX,DX
24dd:103e  JNZ 0x2000:5df7
24dd:1040  MOV word ptr [BP + -0x4],0xc001
24dd:1045  MOV byte ptr [BP + -0x5],0x0
24dd:1049  JMP 0x2000:5e3b
24dd:104b  SHL byte ptr [BP + -0x2],0x1
24dd:104e  ADC AX,DI
24dd:1050  ADC BX,DI
24dd:1052  ADC CX,DI
24dd:1054  ADC DX,DI
24dd:1056  JNC 0x2000:5e2d
24dd:1058  RCR DX,0x1
24dd:105a  INC word ptr [BP + -0x4]
24dd:105d  CMP word ptr [BP + -0x4],0x4001
24dd:1062  JGE 0x2000:5e56
24dd:1064  CMP word ptr [BP + -0x4],0xc001
24dd:1069  JLE 0x2000:5e5f
24dd:106b  CLD
24dd:106c  MOV DI,word ptr [BP + 0x4]
24dd:106f  STOSW ES:DI
24dd:1070  XCHG AX,BX
24dd:1071  STOSW ES:DI
24dd:1072  XCHG AX,CX
24dd:1073  STOSW ES:DI
24dd:1074  XCHG AX,DX
24dd:1075  STOSW ES:DI
24dd:1076  MOV AX,word ptr [BP + -0x4]
24dd:1079  STOSW ES:DI
24dd:107a  MOV AL,byte ptr [BP + -0x5]
24dd:107d  STOSB ES:DI
24dd:107e  POP DI
24dd:107f  POP SI
24dd:1080  MOV SP,BP
24dd:1082  POP BP
24dd:1083  RET 0x6
24dd:1086  MOV CH,0x8
24dd:1088  MOV word ptr [BP + -0x4],0x4001
24dd:108d  JMP 0x2000:5e66
24dd:108f  MOV CH,0x10
24dd:1091  MOV word ptr [BP + -0x4],0xc001
24dd:1096  CALL 0x2000:7131
24dd:1099  MOV byte ptr [BP + -0x5],0x0
24dd:109d  SUB AX,AX
24dd:109f  MOV BX,AX
24dd:10a1  MOV CX,AX
24dd:10a3  MOV DX,AX
24dd:10a5  JMP 0x2000:5e3b
