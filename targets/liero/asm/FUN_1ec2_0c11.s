; FUN_1ec2_0c11  entry=1ec2:0c11 size=42
1ec2:0c11  ENTER 0x2,0x0
1ec2:0c15  CMP word ptr [BP + 0x6],0x0
1ec2:0c19  JGE 0x1000:f842
1ec2:0c1b  MOV word ptr [BP + -0x2],0xffff
1ec2:0c20  JMP 0x1000:f854
1ec2:0c22  CMP word ptr [BP + 0x6],0x0
1ec2:0c26  JLE 0x1000:f84f
1ec2:0c28  MOV word ptr [BP + -0x2],0x1
1ec2:0c2d  JMP 0x1000:f854
1ec2:0c2f  XOR AX,AX
1ec2:0c31  MOV word ptr [BP + -0x2],AX
1ec2:0c34  MOV AX,word ptr [BP + -0x2]
1ec2:0c37  LEAVE
1ec2:0c38  RET 0x4
