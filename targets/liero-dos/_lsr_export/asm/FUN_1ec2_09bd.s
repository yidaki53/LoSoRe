; FUN_1ec2_09bd  entry=1ec2:09bd size=42
1ec2:09bd  ENTER 0x2,0x0
1ec2:09c1  CMP word ptr [BP + 0x6],0x0
1ec2:09c5  JGE 0x1000:f5ee
1ec2:09c7  MOV word ptr [BP + -0x2],0xffff
1ec2:09cc  JMP 0x1000:f600
1ec2:09ce  CMP word ptr [BP + 0x6],0x0
1ec2:09d2  JLE 0x1000:f5fb
1ec2:09d4  MOV word ptr [BP + -0x2],0x1
1ec2:09d9  JMP 0x1000:f600
1ec2:09db  XOR AX,AX
1ec2:09dd  MOV word ptr [BP + -0x2],AX
1ec2:09e0  MOV AX,word ptr [BP + -0x2]
1ec2:09e3  LEAVE
1ec2:09e4  RET 0x4
