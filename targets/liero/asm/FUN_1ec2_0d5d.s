; FUN_1ec2_0d5d  entry=1ec2:0d5d size=43
1ec2:0d5d  ENTER 0x4,0x0
1ec2:0d61  LES DI,[BP + 0xc]
1ec2:0d64  MOV BX,word ptr [BP + 0x8]
1ec2:0d67  MOV CX,word ptr [BP + 0xa]
1ec2:0d6a  MOV DX,0x140
1ec2:0d6d  SUB DX,CX
1ec2:0d6f  MOV word ptr [BP + -0x2],CX
1ec2:0d72  XOR AX,AX
1ec2:0d74  MOV AL,byte ptr [BP + 0x6]
1ec2:0d77  OR CX,word ptr [BP + -0x2]
1ec2:0d7a  OR CX,word ptr [BP + -0x2]
1ec2:0d7d  STOSB.REP ES:DI
1ec2:0d7f  ADD DI,DX
1ec2:0d81  DEC BX
1ec2:0d82  JNZ 0x1000:f99a
1ec2:0d84  LEAVE
1ec2:0d85  RETF 0xa
