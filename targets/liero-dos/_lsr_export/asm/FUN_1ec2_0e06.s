; FUN_1ec2_0e06  entry=1ec2:0e06 size=68
1ec2:0e06  PUSH BP
1ec2:0e07  MOV BP,SP
1ec2:0e09  OR byte ptr [BP + 0xa],0x0
1ec2:0e0d  JZ 0x1000:fa66
1ec2:0e0f  MOV BX,word ptr [BP + 0xc]
1ec2:0e12  MOV CX,word ptr [BP + 0xe]
1ec2:0e15  CMP CX,0x0
1ec2:0e18  JL 0x1000:fa66
1ec2:0e1a  CMP CX,0x9d
1ec2:0e1e  JG 0x1000:fa66
1ec2:0e20  CMP BX,0x0
1ec2:0e23  JL 0x1000:fa66
1ec2:0e25  CMP BX,0x9d
1ec2:0e29  JG 0x1000:fa66
1ec2:0e2b  LES DI,[BP + 0x6]
1ec2:0e2e  SHL BX,0x6
1ec2:0e31  ADD DI,BX
1ec2:0e33  SHL BX,0x2
1ec2:0e36  ADD DI,BX
1ec2:0e38  ADD DI,CX
1ec2:0e3a  MOV AL,byte ptr [BP + 0xa]
1ec2:0e3d  CMP AL,0x26
1ec2:0e3f  JA 0x1000:fa63
1ec2:0e41  ADD AL,0x9
1ec2:0e43  MOV byte ptr ES:[DI],AL
1ec2:0e46  LEAVE
1ec2:0e47  RETF 0xa
