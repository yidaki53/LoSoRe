; FUN_1ec2_0f44  entry=1ec2:0f44 size=196
1ec2:0f44  ENTER 0x2,0x0
1ec2:0f48  MOV BX,word ptr [BP + 0x18]
1ec2:0f4b  MOV CX,word ptr [BP + 0x1a]
1ec2:0f4e  PUSH BX
1ec2:0f4f  PUSH CX
1ec2:0f50  CMP BX,0x9d
1ec2:0f54  JLE 0x1000:fb79
1ec2:0f56  JMP 0x1000:fc24
1ec2:0f59  CMP CX,0x9d
1ec2:0f5d  JLE 0x1000:fb82
1ec2:0f5f  JMP 0x1000:fc24
1ec2:0f62  ADD BX,word ptr [BP + 0x14]
1ec2:0f65  CMP BX,0x0
1ec2:0f68  JGE 0x1000:fb8d
1ec2:0f6a  JMP 0x1000:fc24
1ec2:0f6d  ADD CX,word ptr [BP + 0x16]
1ec2:0f70  CMP CX,0x0
1ec2:0f73  JGE 0x1000:fb98
1ec2:0f75  JMP 0x1000:fc24
1ec2:0f78  POP CX
1ec2:0f79  POP BX
1ec2:0f7a  MOV word ptr [BP + -0x2],0x140
1ec2:0f7f  PUSH DS
1ec2:0f80  LDS SI,[BP + 0x6]
1ec2:0f83  LES DI,[BP + 0xa]
1ec2:0f86  PUSH BX
1ec2:0f87  SHL BX,0x6
1ec2:0f8a  ADD DI,BX
1ec2:0f8c  SHL BX,0x2
1ec2:0f8f  ADD DI,BX
1ec2:0f91  ADD DI,CX
1ec2:0f93  POP BX
1ec2:0f94  XOR AH,AH
1ec2:0f96  XOR DX,DX
1ec2:0f98  OR AH,byte ptr [BP + 0x14]
1ec2:0f9b  OR DL,byte ptr [BP + 0x16]
1ec2:0f9e  SUB word ptr [BP + -0x2],DX
1ec2:0fa1  MOV DL,byte ptr [BP + 0x16]
1ec2:0fa4  CMP BX,0x0
1ec2:0fa7  JGE 0x1000:fbd6
1ec2:0fa9  ADD DI,0x140
1ec2:0fad  ADD SI,DX
1ec2:0faf  INC BX
1ec2:0fb0  DEC AH
1ec2:0fb2  JNZ 0x1000:fbc1
1ec2:0fb4  JMP 0x1000:fc23
1ec2:0fb6  CMP BX,0x9d
1ec2:0fba  JG 0x1000:fc23
1ec2:0fbc  CMP CX,0x0
1ec2:0fbf  JL 0x1000:fc11
1ec2:0fc1  CMP CX,0x9d
1ec2:0fc5  JLE 0x1000:fbf8
1ec2:0fc7  ADD DI,word ptr [BP + -0x2]
1ec2:0fca  ADD DI,DX
1ec2:0fcc  ADD SI,DX
1ec2:0fce  INC BX
1ec2:0fcf  MOV CX,word ptr [BP + 0x1a]
1ec2:0fd2  DEC AH
1ec2:0fd4  JNZ 0x1000:fbc1
1ec2:0fd6  JMP 0x1000:fc23
1ec2:0fd8  MOV AL,byte ptr [SI]
1ec2:0fda  OR AL,0x0
1ec2:0fdc  JZ 0x1000:fc11
1ec2:0fde  MOV AL,byte ptr ES:[DI]
1ec2:0fe1  CMP AL,byte ptr [BP + 0x12]
1ec2:0fe4  JC 0x1000:fc11
1ec2:0fe6  CMP AL,byte ptr [BP + 0x10]
1ec2:0fe9  JA 0x1000:fc11
1ec2:0feb  ADD AL,byte ptr [BP + 0xe]
1ec2:0fee  MOV byte ptr ES:[DI],AL
1ec2:0ff1  INC DI
1ec2:0ff2  INC SI
1ec2:0ff3  INC CX
1ec2:0ff4  DEC DL
1ec2:0ff6  JNZ 0x1000:fbdc
1ec2:0ff8  ADD DI,word ptr [BP + -0x2]
1ec2:0ffb  INC BX
1ec2:0ffc  MOV CX,word ptr [BP + 0x1a]
1ec2:0fff  DEC AH
1ec2:1001  JNZ 0x1000:fbc1
1ec2:1003  POP DS
1ec2:1004  LEAVE
1ec2:1005  RETF 0x16
