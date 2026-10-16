; FUN_235c_0f57  entry=235c:0f57 size=332
235c:0f57  ENTER 0x8,0x0
235c:0f5b  LES DI,[BP + 0xc]
235c:0f5e  MOV AX,word ptr ES:[DI + 0x6]
235c:0f62  MOV DX,word ptr ES:[DI + 0x8]
235c:0f66  MOV word ptr [BP + -0x4],AX
235c:0f69  MOV word ptr [BP + -0x2],DX
235c:0f6c  MOV AX,0x6856
235c:0f6f  MOV DX,DS
235c:0f71  MOV word ptr [BP + -0x8],AX
235c:0f74  MOV word ptr [BP + -0x6],DX
235c:0f77  LES DI,[BP + 0xc]
235c:0f7a  MOV AX,word ptr ES:[DI]
235c:0f7d  MOV [0x782a],AX
235c:0f80  XOR AX,AX
235c:0f82  MOV [0x7830],AX
235c:0f85  CMP word ptr [BP + 0x6],0x0
235c:0f89  JA 0x2000:454e
235c:0f8b  JMP 0x2000:465f
235c:0f8e  MOV AX,word ptr [BP + -0x4]
235c:0f91  MOV DX,word ptr [BP + -0x2]
235c:0f94  LES DI,[BP + 0x8]
235c:0f97  SUB AX,word ptr ES:[DI]
235c:0f9a  SBB DX,word ptr ES:[DI + 0x2]
235c:0f9e  MOV CX,AX
235c:0fa0  MOV BX,DX
235c:0fa2  MOV AX,word ptr [BP + 0x6]
235c:0fa5  XOR DX,DX
235c:0fa7  CMP DX,BX
235c:0fa9  JL 0x2000:4571
235c:0fab  JG 0x2000:457f
235c:0fad  CMP AX,CX
235c:0faf  JNC 0x2000:457f
235c:0fb1  MOV AX,word ptr [BP + 0x6]
235c:0fb4  XOR DX,DX
235c:0fb6  MOV [0x7826],AX
235c:0fb9  MOV word ptr [0x7828],DX
235c:0fbd  JMP 0x2000:4596
235c:0fbf  MOV AX,word ptr [BP + -0x4]
235c:0fc2  MOV DX,word ptr [BP + -0x2]
235c:0fc5  LES DI,[BP + 0x8]
235c:0fc8  SUB AX,word ptr ES:[DI]
235c:0fcb  SBB DX,word ptr ES:[DI + 0x2]
235c:0fcf  MOV [0x7826],AX
235c:0fd2  MOV word ptr [0x7828],DX
235c:0fd6  LES DI,[BP + 0xc]
235c:0fd9  MOV AX,word ptr ES:[DI + 0x2]
235c:0fdd  MOV DX,word ptr ES:[DI + 0x4]
235c:0fe1  LES DI,[BP + 0x8]
235c:0fe4  ADD AX,word ptr ES:[DI]
235c:0fe7  ADC DX,word ptr ES:[DI + 0x2]
235c:0feb  MOV [0x782c],AX
235c:0fee  MOV word ptr [0x782e],DX
235c:0ff2  MOV AX,word ptr ES:[DI]
235c:0ff5  MOV DX,word ptr ES:[DI + 0x2]
235c:0ff9  ADD AX,word ptr [0x7826]
235c:0ffd  ADC DX,word ptr [0x7828]
235c:1001  MOV word ptr ES:[DI],AX
235c:1004  MOV word ptr ES:[DI + 0x2],DX
235c:1008  CMP byte ptr [BP + 0x4],0x0
235c:100c  JZ 0x2000:45ee
235c:100e  MOV AX,word ptr ES:[DI]
235c:1011  MOV DX,word ptr ES:[DI + 0x2]
235c:1015  MOV CX,word ptr [BP + -0x4]
235c:1018  MOV BX,word ptr [BP + -0x2]
235c:101b  CALLF 0x2000:8b8d
235c:1020  MOV AX,CX
235c:1022  MOV DX,BX
235c:1024  LES DI,[BP + 0x8]
235c:1027  MOV word ptr ES:[DI],AX
235c:102a  MOV word ptr ES:[DI + 0x2],DX
235c:102e  MOV AX,word ptr [BP + -0x8]
235c:1031  MOV DX,word ptr [BP + -0x6]
235c:1034  MOV [0x7832],AX
235c:1037  MOV word ptr [0x7834],DX
235c:103b  LES DI,[BP + -0x8]
235c:103e  MOV AX,DI
235c:1040  XOR DX,DX
235c:1042  ADD AX,word ptr [0x7826]
235c:1046  ADC DX,word ptr [0x7828]
235c:104a  LES DI,[BP + -0x8]
235c:104d  MOV DX,ES
235c:104f  PUSH DX
235c:1050  PUSH AX
235c:1051  CALL 0x2000:40f3
235c:1054  MOV word ptr [BP + -0x8],AX
235c:1057  MOV word ptr [BP + -0x6],DX
235c:105a  MOV AX,word ptr [BP + 0x6]
235c:105d  XOR DX,DX
235c:105f  SUB AX,word ptr [0x7826]
235c:1063  SBB DX,word ptr [0x7828]
235c:1067  MOV word ptr [BP + 0x6],AX
235c:106a  MOV AX,[0x7826]
235c:106d  MOV DX,word ptr [0x7828]
235c:1071  ADD AX,0x1
235c:1074  ADC DX,0x0
235c:1077  MOV CX,0x2
235c:107a  XOR BX,BX
235c:107c  CALLF 0x2000:8b8d
235c:1081  MOV CX,0x2
235c:1084  XOR BX,BX
235c:1086  CALLF 0x2000:8b50
235c:108b  MOV [0x7826],AX
235c:108e  MOV word ptr [0x7828],DX
235c:1092  MOV DI,0x7826
235c:1095  PUSH DS
235c:1096  PUSH DI
235c:1097  CALLF 0x2000:49a0
235c:109c  JMP 0x2000:4545
235c:109f  LEAVE
235c:10a0  RET 0xc
