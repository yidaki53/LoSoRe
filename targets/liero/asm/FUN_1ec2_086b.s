; FUN_1ec2_086b  entry=1ec2:086b size=42
1ec2:086b  ENTER 0x2,0x0
1ec2:086f  CMP word ptr [BP + 0x6],0x0
1ec2:0873  JGE 0x1000:f49c
1ec2:0875  MOV word ptr [BP + -0x2],0xffff
1ec2:087a  JMP 0x1000:f4ae
1ec2:087c  CMP word ptr [BP + 0x6],0x0
1ec2:0880  JLE 0x1000:f4a9
1ec2:0882  MOV word ptr [BP + -0x2],0x1
1ec2:0887  JMP 0x1000:f4ae
1ec2:0889  XOR AX,AX
1ec2:088b  MOV word ptr [BP + -0x2],AX
1ec2:088e  MOV AX,word ptr [BP + -0x2]
1ec2:0891  LEAVE
1ec2:0892  RET 0x4
