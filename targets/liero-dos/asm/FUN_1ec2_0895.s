; FUN_1ec2_0895  entry=1ec2:0895 size=296
1ec2:0895  ENTER 0xe,0x0
1ec2:0899  MOV AX,word ptr [BP + 0x10]
1ec2:089c  MOV word ptr [BP + -0x2],AX
1ec2:089f  MOV AX,word ptr [BP + 0xe]
1ec2:08a2  MOV word ptr [BP + -0x4],AX
1ec2:08a5  MOV AX,word ptr [BP + 0xc]
1ec2:08a8  SUB AX,word ptr [BP + 0x10]
1ec2:08ab  MOV word ptr [BP + -0x8],AX
1ec2:08ae  MOV AX,word ptr [BP + 0xa]
1ec2:08b1  SUB AX,word ptr [BP + 0xe]
1ec2:08b4  MOV word ptr [BP + -0xa],AX
1ec2:08b7  PUSH word ptr [BP + -0x8]
1ec2:08ba  PUSH BP
1ec2:08bb  CALL 0x1000:f48b
1ec2:08be  MOV word ptr [BP + -0xc],AX
1ec2:08c1  PUSH word ptr [BP + -0xa]
1ec2:08c4  PUSH BP
1ec2:08c5  CALL 0x1000:f48b
1ec2:08c8  MOV word ptr [BP + -0xe],AX
1ec2:08cb  MOV AX,word ptr [BP + -0x8]
1ec2:08ce  CWD
1ec2:08cf  XOR AX,DX
1ec2:08d1  SUB AX,DX
1ec2:08d3  MOV word ptr [BP + -0x8],AX
1ec2:08d6  MOV AX,word ptr [BP + -0xa]
1ec2:08d9  CWD
1ec2:08da  XOR AX,DX
1ec2:08dc  SUB AX,DX
1ec2:08de  MOV word ptr [BP + -0xa],AX
1ec2:08e1  MOV AX,word ptr [BP + -0x8]
1ec2:08e4  CMP AX,word ptr [BP + -0xa]
1ec2:08e7  JLE 0x1000:f572
1ec2:08e9  MOV AX,word ptr [BP + -0x8]
1ec2:08ec  CWD
1ec2:08ed  MOV CX,0x2
1ec2:08f0  IDIV CX
1ec2:08f2  NEG AX
1ec2:08f4  MOV word ptr [BP + -0x6],AX
1ec2:08f7  MOV AX,word ptr [BP + -0x2]
1ec2:08fa  CMP AX,word ptr [BP + 0xc]
1ec2:08fd  JZ 0x1000:f570
1ec2:08ff  MOV AX,word ptr [BP + -0x6]
1ec2:0902  ADD AX,word ptr [BP + -0xa]
1ec2:0905  MOV word ptr [BP + -0x6],AX
1ec2:0908  MOV AX,word ptr [BP + -0x2]
1ec2:090b  ADD AX,word ptr [BP + -0xc]
1ec2:090e  MOV word ptr [BP + -0x2],AX
1ec2:0911  CMP word ptr [BP + -0x6],0x0
1ec2:0915  JLE 0x1000:f549
1ec2:0917  MOV AX,word ptr [BP + -0x4]
1ec2:091a  ADD AX,word ptr [BP + -0xe]
1ec2:091d  MOV word ptr [BP + -0x4],AX
1ec2:0920  MOV AX,word ptr [BP + -0x6]
1ec2:0923  SUB AX,word ptr [BP + -0x8]
1ec2:0926  MOV word ptr [BP + -0x6],AX
1ec2:0929  PUSH 0x5
1ec2:092b  CALLF 0x2000:9424
1ec2:0930  OR AX,AX
1ec2:0932  JNZ 0x1000:f56e
1ec2:0934  PUSH word ptr [BP + -0x2]
1ec2:0937  PUSH word ptr [BP + -0x4]
1ec2:093a  PUSH 0x2
1ec2:093c  CALLF 0x2000:9424
1ec2:0941  ADD AX,0x53
1ec2:0944  PUSH AX
1ec2:0945  LES DI,[BP + 0x6]
1ec2:0948  PUSH ES
1ec2:0949  PUSH DI
1ec2:094a  PUSH CS
1ec2:094b  CALL 0x1000:f9e8
1ec2:094e  JMP 0x1000:f517
1ec2:0950  JMP 0x1000:f5d9
1ec2:0952  MOV AX,word ptr [BP + -0xa]
1ec2:0955  CWD
1ec2:0956  MOV CX,0x2
1ec2:0959  IDIV CX
1ec2:095b  NEG AX
1ec2:095d  MOV word ptr [BP + -0x6],AX
1ec2:0960  MOV AX,word ptr [BP + -0x4]
1ec2:0963  CMP AX,word ptr [BP + 0xa]
1ec2:0966  JZ 0x1000:f5d9
1ec2:0968  MOV AX,word ptr [BP + -0x6]
1ec2:096b  ADD AX,word ptr [BP + -0x8]
1ec2:096e  MOV word ptr [BP + -0x6],AX
1ec2:0971  MOV AX,word ptr [BP + -0x4]
1ec2:0974  ADD AX,word ptr [BP + -0xe]
1ec2:0977  MOV word ptr [BP + -0x4],AX
1ec2:097a  CMP word ptr [BP + -0x6],0x0
1ec2:097e  JLE 0x1000:f5b2
1ec2:0980  MOV AX,word ptr [BP + -0x2]
1ec2:0983  ADD AX,word ptr [BP + -0xc]
1ec2:0986  MOV word ptr [BP + -0x2],AX
1ec2:0989  MOV AX,word ptr [BP + -0x6]
1ec2:098c  SUB AX,word ptr [BP + -0xa]
1ec2:098f  MOV word ptr [BP + -0x6],AX
1ec2:0992  PUSH 0x5
1ec2:0994  CALLF 0x2000:9424
1ec2:0999  OR AX,AX
1ec2:099b  JNZ 0x1000:f5d7
1ec2:099d  PUSH word ptr [BP + -0x2]
1ec2:09a0  PUSH word ptr [BP + -0x4]
1ec2:09a3  PUSH 0x2
1ec2:09a5  CALLF 0x2000:9424
1ec2:09aa  ADD AX,0x53
1ec2:09ad  PUSH AX
1ec2:09ae  LES DI,[BP + 0x6]
1ec2:09b1  PUSH ES
1ec2:09b2  PUSH DI
1ec2:09b3  PUSH CS
1ec2:09b4  CALL 0x1000:f9e8
1ec2:09b7  JMP 0x1000:f580
1ec2:09b9  LEAVE
1ec2:09ba  RETF 0xc
