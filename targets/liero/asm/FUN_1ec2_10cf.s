; FUN_1ec2_10cf  entry=1ec2:10cf size=27
1ec2:10cf  PUSH BP
1ec2:10d0  MOV BP,SP
1ec2:10d2  MOV DX,0x3c8
1ec2:10d5  MOV AL,byte ptr [BP + 0xc]
1ec2:10d8  OUT DX,AL
1ec2:10d9  INC DX
1ec2:10da  MOV AL,byte ptr [BP + 0xa]
1ec2:10dd  OUT DX,AL
1ec2:10de  MOV AL,byte ptr [BP + 0x8]
1ec2:10e1  OUT DX,AL
1ec2:10e2  MOV AL,byte ptr [BP + 0x6]
1ec2:10e5  OUT DX,AL
1ec2:10e6  LEAVE
1ec2:10e7  RETF 0x8
