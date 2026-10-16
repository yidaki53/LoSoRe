; FUN_1ec2_00a5  entry=1ec2:00a5 size=39
1ec2:00a5  PUSH BP
1ec2:00a6  MOV BP,SP
1ec2:00a8  PUSH DS
1ec2:00a9  LES DI,[BP + 0xa]
1ec2:00ac  LDS SI,[BP + 0xe]
1ec2:00af  MOV AX,word ptr [BP + 0x6]
1ec2:00b2  MOV BX,word ptr [BP + 0x8]
1ec2:00b5  MOV DX,0x140
1ec2:00b8  SUB DX,BX
1ec2:00ba  XOR CX,CX
1ec2:00bc  ADD CX,BX
1ec2:00be  MOVSB.REP ES:DI,SI
1ec2:00c0  ADD DI,DX
1ec2:00c2  ADD SI,DX
1ec2:00c4  DEC AX
1ec2:00c5  JNZ 0x1000:ecdc
1ec2:00c7  POP DS
1ec2:00c8  LEAVE
1ec2:00c9  RETF 0xc
