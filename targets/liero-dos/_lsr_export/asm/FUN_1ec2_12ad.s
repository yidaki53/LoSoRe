; FUN_1ec2_12ad  entry=1ec2:12ad size=57
1ec2:12ad  PUSH BP
1ec2:12ae  MOV BP,SP
1ec2:12b0  LES DI,[BP + 0x6]
1ec2:12b3  MOV BX,word ptr [BP + 0xc]
1ec2:12b6  SHL BX,0x6
1ec2:12b9  ADD DI,BX
1ec2:12bb  SHL BX,0x2
1ec2:12be  ADD DI,BX
1ec2:12c0  ADD DI,word ptr [BP + 0x10]
1ec2:12c3  MOV CX,word ptr [BP + 0xe]
1ec2:12c6  MOV AL,byte ptr [BP + 0xa]
1ec2:12c9  MOV AH,AL
1ec2:12cb  SHR CX,0x1
1ec2:12cd  JNC 0x1000:fef0
1ec2:12cf  STOSB ES:DI
1ec2:12d0  STOSW.REP ES:DI
1ec2:12d2  ADD DI,0x140
1ec2:12d6  ADD CX,word ptr [BP + 0xe]
1ec2:12d9  SUB DI,CX
1ec2:12db  SHR CX,0x1
1ec2:12dd  JNC 0x1000:ff00
1ec2:12df  STOSB ES:DI
1ec2:12e0  STOSW.REP ES:DI
1ec2:12e2  LEAVE
1ec2:12e3  RETF 0xc
