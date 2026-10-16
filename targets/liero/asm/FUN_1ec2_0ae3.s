; FUN_1ec2_0ae3  entry=1ec2:0ae3 size=42
1ec2:0ae3  ENTER 0x2,0x0
1ec2:0ae7  CMP word ptr [BP + 0x6],0x0
1ec2:0aeb  JGE 0x1000:f714
1ec2:0aed  MOV word ptr [BP + -0x2],0xffff
1ec2:0af2  JMP 0x1000:f726
1ec2:0af4  CMP word ptr [BP + 0x6],0x0
1ec2:0af8  JLE 0x1000:f721
1ec2:0afa  MOV word ptr [BP + -0x2],0x1
1ec2:0aff  JMP 0x1000:f726
1ec2:0b01  XOR AX,AX
1ec2:0b03  MOV word ptr [BP + -0x2],AX
1ec2:0b06  MOV AX,word ptr [BP + -0x2]
1ec2:0b09  LEAVE
1ec2:0b0a  RET 0x4
