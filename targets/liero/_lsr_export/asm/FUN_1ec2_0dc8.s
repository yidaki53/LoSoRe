; FUN_1ec2_0dc8  entry=1ec2:0dc8 size=62
1ec2:0dc8  PUSH BP
1ec2:0dc9  MOV BP,SP
1ec2:0dcb  OR byte ptr [BP + 0xa],0x0
1ec2:0dcf  JZ 0x1000:fa22
1ec2:0dd1  MOV BX,word ptr [BP + 0xc]
1ec2:0dd4  MOV CX,word ptr [BP + 0xe]
1ec2:0dd7  CMP CX,0x0
1ec2:0dda  JL 0x1000:fa22
1ec2:0ddc  CMP CX,0x9d
1ec2:0de0  JG 0x1000:fa22
1ec2:0de2  CMP BX,0x0
1ec2:0de5  JL 0x1000:fa22
1ec2:0de7  CMP BX,0x9d
1ec2:0deb  JG 0x1000:fa22
1ec2:0ded  LES DI,[BP + 0x6]
1ec2:0df0  SHL BX,0x6
1ec2:0df3  ADD DI,BX
1ec2:0df5  SHL BX,0x2
1ec2:0df8  ADD DI,BX
1ec2:0dfa  ADD DI,CX
1ec2:0dfc  MOV AL,byte ptr [BP + 0xa]
1ec2:0dff  MOV byte ptr ES:[DI],AL
1ec2:0e02  LEAVE
1ec2:0e03  RETF 0xa
