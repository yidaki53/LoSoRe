; FUN_1ec2_155e  entry=1ec2:155e size=93
1ec2:155e  ENTER 0x2,0x0
1ec2:1562  MOV byte ptr [BP + -0x1],0x0
1ec2:1566  JMP 0x2000:018b
1ec2:1568  INC byte ptr [BP + -0x1]
1ec2:156b  MOV AL,byte ptr [BP + -0x1]
1ec2:156e  PUSH AX
1ec2:156f  MOV AL,byte ptr [BP + -0x1]
1ec2:1572  XOR AH,AH
1ec2:1574  MOV SI,AX
1ec2:1576  SHL AX,0x1
1ec2:1578  ADD AX,SI
1ec2:157a  LES DI,[BP + 0x6]
1ec2:157d  ADD DI,AX
1ec2:157f  MOV AL,byte ptr ES:[DI]
1ec2:1582  PUSH AX
1ec2:1583  MOV AL,byte ptr [BP + -0x1]
1ec2:1586  XOR AH,AH
1ec2:1588  MOV SI,AX
1ec2:158a  SHL AX,0x1
1ec2:158c  ADD AX,SI
1ec2:158e  LES DI,[BP + 0x6]
1ec2:1591  ADD DI,AX
1ec2:1593  MOV AL,byte ptr ES:[DI + 0x1]
1ec2:1597  PUSH AX
1ec2:1598  MOV AL,byte ptr [BP + -0x1]
1ec2:159b  XOR AH,AH
1ec2:159d  MOV SI,AX
1ec2:159f  SHL AX,0x1
1ec2:15a1  ADD AX,SI
1ec2:15a3  LES DI,[BP + 0x6]
1ec2:15a6  ADD DI,AX
1ec2:15a8  MOV AL,byte ptr ES:[DI + 0x2]
1ec2:15ac  PUSH AX
1ec2:15ad  PUSH CS
1ec2:15ae  CALL 0x2000:fcef
1ec2:15b1  CMP byte ptr [BP + -0x1],0xff
1ec2:15b5  JNZ 0x2000:0188
1ec2:15b7  LEAVE
1ec2:15b8  RETF 0x4
