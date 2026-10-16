; FUN_1000_0d70  entry=1000:0d70 size=334
1000:0d70  PUSH BP
1000:0d71  MOV BP,SP
1000:0d73  MOV AX,0xe
1000:0d76  CALLF 0x2000:5300
1000:0d7b  SUB SP,0xe
1000:0d7e  MOV byte ptr [BP + -0x1],0x0
1000:0d82  MOV AL,byte ptr [BP + 0xa]
1000:0d85  XOR AH,AH
1000:0d87  IMUL AX,AX,0xaa
1000:0d8b  LES DI,[0x6670]
1000:0d8f  ADD DI,AX
1000:0d91  CMP byte ptr ES:[DI + 0x9a],0x0
1000:0d97  JNZ 0x1000:0d9c
1000:0d99  JMP 0x1000:0eb7
1000:0d9c  MOV AL,byte ptr [BP + 0xa]
1000:0d9f  XOR AH,AH
1000:0da1  IMUL AX,AX,0xaa
1000:0da5  LES DI,[0x6670]
1000:0da9  ADD DI,AX
1000:0dab  MOV DX,word ptr ES:[DI + 0x6]
1000:0daf  MOV AX,word ptr [BP + 0x6]
1000:0db2  SUB AX,DX
1000:0db4  ADD AX,0x7
1000:0db7  MOV word ptr [BP + -0x3],AX
1000:0dba  MOV AL,byte ptr [BP + 0xa]
1000:0dbd  XOR AH,AH
1000:0dbf  IMUL AX,AX,0xaa
1000:0dc3  LES DI,[0x6670]
1000:0dc7  ADD DI,AX
1000:0dc9  MOV DX,word ptr ES:[DI + 0xa]
1000:0dcd  MOV AX,word ptr [BP + 0x4]
1000:0dd0  SUB AX,DX
1000:0dd2  ADD AX,0x5
1000:0dd5  MOV word ptr [BP + -0x5],AX
1000:0dd8  MOV AL,byte ptr [BP + 0xa]
1000:0ddb  XOR AH,AH
1000:0ddd  IMUL AX,AX,0xaa
1000:0de1  LES DI,[0x6670]
1000:0de5  ADD DI,AX
1000:0de7  CMP byte ptr ES:[DI + 0x9b],0x0
1000:0ded  JNZ 0x1000:0df8
1000:0def  MOV AX,0xe
1000:0df2  SUB AX,word ptr [BP + -0x3]
1000:0df5  MOV word ptr [BP + -0x3],AX
1000:0df8  MOV AL,byte ptr [BP + 0x8]
1000:0dfb  XOR AH,AH
1000:0dfd  ADD AX,word ptr [BP + -0x3]
1000:0e00  MOV word ptr [BP + -0xb],AX
1000:0e03  MOV AL,byte ptr [BP + 0x8]
1000:0e06  XOR AH,AH
1000:0e08  MOV DX,AX
1000:0e0a  MOV AX,word ptr [BP + -0x3]
1000:0e0d  SUB AX,DX
1000:0e0f  CMP AX,word ptr [BP + -0xb]
1000:0e12  JLE 0x1000:0e17
1000:0e14  JMP 0x1000:0eb7
1000:0e17  MOV word ptr [BP + -0x7],AX
1000:0e1a  JMP 0x1000:0e1f
1000:0e1c  INC word ptr [BP + -0x7]
1000:0e1f  MOV AL,byte ptr [BP + 0x8]
1000:0e22  XOR AH,AH
1000:0e24  ADD AX,word ptr [BP + -0x5]
1000:0e27  MOV word ptr [BP + -0xd],AX
1000:0e2a  MOV AL,byte ptr [BP + 0x8]
1000:0e2d  XOR AH,AH
1000:0e2f  MOV DX,AX
1000:0e31  MOV AX,word ptr [BP + -0x5]
1000:0e34  SUB AX,DX
1000:0e36  CMP AX,word ptr [BP + -0xd]
1000:0e39  JG 0x1000:0eac
1000:0e3b  MOV word ptr [BP + -0x9],AX
1000:0e3e  JMP 0x1000:0e43
1000:0e40  INC word ptr [BP + -0x9]
1000:0e43  CMP word ptr [BP + -0x7],0x0
1000:0e47  JLE 0x1000:0ea4
1000:0e49  CMP word ptr [BP + -0x7],0xe
1000:0e4d  JGE 0x1000:0ea4
1000:0e4f  CMP word ptr [BP + -0x9],-0x1
1000:0e53  JLE 0x1000:0ea4
1000:0e55  CMP word ptr [BP + -0x9],0xa
1000:0e59  JGE 0x1000:0ea4
1000:0e5b  MOV CX,word ptr [BP + -0x7]
1000:0e5e  MOV AX,word ptr [BP + -0x9]
1000:0e61  SHL AX,0x4
1000:0e64  MOV DX,AX
1000:0e66  MOV AL,byte ptr [BP + 0xa]
1000:0e69  XOR AH,AH
1000:0e6b  IMUL AX,AX,0xaa
1000:0e6f  LES DI,[0x6670]
1000:0e73  ADD DI,AX
1000:0e75  MOV AL,byte ptr ES:[DI + 0xa1]
1000:0e7a  XOR AH,AH
1000:0e7c  SHL AX,0x8
1000:0e7f  LES DI,[0x6678]
1000:0e83  ADD DI,AX
1000:0e85  ADD DI,DX
1000:0e87  ADD DI,CX
1000:0e89  MOV AL,byte ptr ES:[DI]
1000:0e8c  MOV AH,0x1
1000:0e8e  MOV DX,0x20
1000:0e91  CALLF 0x2000:8f31
1000:0e96  MOV DI,DX
1000:0e98  TEST byte ptr [DI + 0x28],AL
1000:0e9c  JZ 0x1000:0ea4
1000:0e9e  MOV byte ptr [BP + -0x1],0x1
1000:0ea2  JMP 0x1000:0eb7
1000:0ea4  MOV AX,word ptr [BP + -0x9]
1000:0ea7  CMP AX,word ptr [BP + -0xd]
1000:0eaa  JNZ 0x1000:0e40
1000:0eac  MOV AX,word ptr [BP + -0x7]
1000:0eaf  CMP AX,word ptr [BP + -0xb]
1000:0eb2  JZ 0x1000:0eb7
1000:0eb4  JMP 0x1000:0e1c
1000:0eb7  MOV AL,byte ptr [BP + -0x1]
1000:0eba  LEAVE
1000:0ebb  RET 0x8
