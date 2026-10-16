; FUN_1ec2_0e4a  entry=1ec2:0e4a size=69
1ec2:0e4a  PUSH BP
1ec2:0e4b  MOV BP,SP
1ec2:0e4d  MOV BX,word ptr [BP + 0xa]
1ec2:0e50  MOV CX,word ptr [BP + 0xc]
1ec2:0e53  CMP CX,0x0
1ec2:0e56  JL 0x1000:faab
1ec2:0e58  CMP CX,0x9d
1ec2:0e5c  JG 0x1000:faab
1ec2:0e5e  CMP BX,0x0
1ec2:0e61  JL 0x1000:faab
1ec2:0e63  CMP BX,0x9d
1ec2:0e67  JG 0x1000:faab
1ec2:0e69  LES DI,[BP + 0x6]
1ec2:0e6c  SHL BX,0x6
1ec2:0e6f  ADD DI,BX
1ec2:0e71  SHL BX,0x2
1ec2:0e74  ADD DI,BX
1ec2:0e76  ADD DI,CX
1ec2:0e78  MOV AH,byte ptr ES:[DI]
1ec2:0e7b  CMP AH,0xa0
1ec2:0e7e  JC 0x1000:faab
1ec2:0e80  CMP AH,0xa3
1ec2:0e83  JA 0x1000:faab
1ec2:0e85  ADD AH,0x4
1ec2:0e88  MOV byte ptr ES:[DI],AH
1ec2:0e8b  LEAVE
1ec2:0e8c  RETF 0x8
