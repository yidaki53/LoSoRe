; FUN_1ec2_0e8f  entry=1ec2:0e8f size=181
1ec2:0e8f  ENTER 0x2,0x0
1ec2:0e93  MOV BX,word ptr [BP + 0x12]
1ec2:0e96  MOV CX,word ptr [BP + 0x14]
1ec2:0e99  PUSH BX
1ec2:0e9a  PUSH CX
1ec2:0e9b  CMP BX,0x9d
1ec2:0e9f  JLE 0x1000:fac4
1ec2:0ea1  JMP 0x1000:fb60
1ec2:0ea4  CMP CX,0x9d
1ec2:0ea8  JLE 0x1000:facd
1ec2:0eaa  JMP 0x1000:fb60
1ec2:0ead  ADD BX,word ptr [BP + 0xe]
1ec2:0eb0  CMP BX,0x0
1ec2:0eb3  JGE 0x1000:fad8
1ec2:0eb5  JMP 0x1000:fb60
1ec2:0eb8  ADD CX,word ptr [BP + 0x10]
1ec2:0ebb  CMP CX,0x0
1ec2:0ebe  JGE 0x1000:fae3
1ec2:0ec0  JMP 0x1000:fb60
1ec2:0ec3  POP CX
1ec2:0ec4  POP BX
1ec2:0ec5  MOV word ptr [BP + -0x2],0x140
1ec2:0eca  PUSH DS
1ec2:0ecb  LDS SI,[BP + 0x6]
1ec2:0ece  LES DI,[BP + 0xa]
1ec2:0ed1  PUSH BX
1ec2:0ed2  SHL BX,0x6
1ec2:0ed5  ADD DI,BX
1ec2:0ed7  SHL BX,0x2
1ec2:0eda  ADD DI,BX
1ec2:0edc  ADD DI,CX
1ec2:0ede  POP BX
1ec2:0edf  XOR AH,AH
1ec2:0ee1  XOR DX,DX
1ec2:0ee3  OR AH,byte ptr [BP + 0xe]
1ec2:0ee6  OR DL,byte ptr [BP + 0x10]
1ec2:0ee9  SUB word ptr [BP + -0x2],DX
1ec2:0eec  MOV DL,byte ptr [BP + 0x10]
1ec2:0eef  CMP BX,0x0
1ec2:0ef2  JGE 0x1000:fb22
1ec2:0ef4  ADD DI,0x140
1ec2:0ef8  ADD SI,word ptr [BP + 0x10]
1ec2:0efb  INC BX
1ec2:0efc  DEC AH
1ec2:0efe  JNZ 0x1000:fb0c
1ec2:0f00  JMP 0x1000:fb5f
1ec2:0f02  CMP BX,0x9d
1ec2:0f06  JG 0x1000:fb5f
1ec2:0f08  CMP CX,0x0
1ec2:0f0b  JL 0x1000:fb4d
1ec2:0f0d  CMP CX,0x9d
1ec2:0f11  JLE 0x1000:fb44
1ec2:0f13  ADD DI,word ptr [BP + -0x2]
1ec2:0f16  ADD DI,DX
1ec2:0f18  ADD SI,DX
1ec2:0f1a  INC BX
1ec2:0f1b  MOV CX,word ptr [BP + 0x14]
1ec2:0f1e  DEC AH
1ec2:0f20  JNZ 0x1000:fb0c
1ec2:0f22  JMP 0x1000:fb5f
1ec2:0f24  MOV AL,byte ptr [SI]
1ec2:0f26  OR AL,0x0
1ec2:0f28  JZ 0x1000:fb4d
1ec2:0f2a  MOV byte ptr ES:[DI],AL
1ec2:0f2d  INC DI
1ec2:0f2e  INC SI
1ec2:0f2f  INC CX
1ec2:0f30  DEC DL
1ec2:0f32  JNZ 0x1000:fb28
1ec2:0f34  ADD DI,word ptr [BP + -0x2]
1ec2:0f37  INC BX
1ec2:0f38  MOV CX,word ptr [BP + 0x14]
1ec2:0f3b  DEC AH
1ec2:0f3d  JNZ 0x1000:fb0c
1ec2:0f3f  POP DS
1ec2:0f40  LEAVE
1ec2:0f41  RETF 0x10
