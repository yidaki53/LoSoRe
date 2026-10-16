; FUN_1ec2_1008  entry=1ec2:1008 size=199
1ec2:1008  ENTER 0x2,0x0
1ec2:100c  MOV BX,word ptr [BP + 0x16]
1ec2:100f  MOV CX,word ptr [BP + 0x18]
1ec2:1012  PUSH BX
1ec2:1013  PUSH CX
1ec2:1014  CMP BX,0x9d
1ec2:1018  JLE 0x1000:fc3d
1ec2:101a  JMP 0x1000:fceb
1ec2:101d  CMP CX,0x9d
1ec2:1021  JLE 0x1000:fc46
1ec2:1023  JMP 0x1000:fceb
1ec2:1026  ADD BX,word ptr [BP + 0x12]
1ec2:1029  CMP BX,0x0
1ec2:102c  JGE 0x1000:fc51
1ec2:102e  JMP 0x1000:fceb
1ec2:1031  ADD CX,word ptr [BP + 0x14]
1ec2:1034  CMP CX,0x0
1ec2:1037  JGE 0x1000:fc5c
1ec2:1039  JMP 0x1000:fceb
1ec2:103c  POP CX
1ec2:103d  POP BX
1ec2:103e  MOV word ptr [BP + -0x2],0x140
1ec2:1043  PUSH DS
1ec2:1044  LDS SI,[BP + 0x6]
1ec2:1047  LES DI,[BP + 0xa]
1ec2:104a  PUSH BX
1ec2:104b  SHL BX,0x6
1ec2:104e  ADD DI,BX
1ec2:1050  SHL BX,0x2
1ec2:1053  ADD DI,BX
1ec2:1055  ADD DI,CX
1ec2:1057  POP BX
1ec2:1058  XOR AH,AH
1ec2:105a  XOR DX,DX
1ec2:105c  OR AH,byte ptr [BP + 0x12]
1ec2:105f  OR DL,byte ptr [BP + 0x14]
1ec2:1062  SUB word ptr [BP + -0x2],DX
1ec2:1065  MOV DL,byte ptr [BP + 0x14]
1ec2:1068  CMP BX,0x0
1ec2:106b  JGE 0x1000:fc9a
1ec2:106d  ADD DI,0x140
1ec2:1071  ADD SI,DX
1ec2:1073  INC BX
1ec2:1074  DEC AH
1ec2:1076  JNZ 0x1000:fc85
1ec2:1078  JMP 0x1000:fcea
1ec2:107a  CMP BX,0x9d
1ec2:107e  JG 0x1000:fcea
1ec2:1080  CMP CX,0x0
1ec2:1083  JL 0x1000:fcd8
1ec2:1085  CMP CX,0x9d
1ec2:1089  JLE 0x1000:fcbc
1ec2:108b  ADD DI,word ptr [BP + -0x2]
1ec2:108e  ADD DI,DX
1ec2:1090  ADD SI,DX
1ec2:1092  INC BX
1ec2:1093  MOV CX,word ptr [BP + 0x18]
1ec2:1096  DEC AH
1ec2:1098  JNZ 0x1000:fc85
1ec2:109a  JMP 0x1000:fcea
1ec2:109c  MOV AL,byte ptr [SI]
1ec2:109e  OR AL,0x0
1ec2:10a0  JZ 0x1000:fcd8
1ec2:10a2  MOV AL,byte ptr ES:[DI]
1ec2:10a5  CMP AL,0x7
1ec2:10a7  JC 0x1000:fcd3
1ec2:10a9  CMP AL,byte ptr [BP + 0x10]
1ec2:10ac  JC 0x1000:fcd8
1ec2:10ae  CMP AL,byte ptr [BP + 0xe]
1ec2:10b1  JA 0x1000:fcd8
1ec2:10b3  MOV AL,byte ptr [SI]
1ec2:10b5  MOV byte ptr ES:[DI],AL
1ec2:10b8  INC DI
1ec2:10b9  INC SI
1ec2:10ba  INC CX
1ec2:10bb  DEC DL
1ec2:10bd  JNZ 0x1000:fca0
1ec2:10bf  ADD DI,word ptr [BP + -0x2]
1ec2:10c2  INC BX
1ec2:10c3  MOV CX,word ptr [BP + 0x18]
1ec2:10c6  DEC AH
1ec2:10c8  JNZ 0x1000:fc85
1ec2:10ca  POP DS
1ec2:10cb  LEAVE
1ec2:10cc  RETF 0x14
