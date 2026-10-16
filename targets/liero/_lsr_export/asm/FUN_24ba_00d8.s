; FUN_24ba_00d8  entry=24ba:00d8 size=48
24ba:00d8  ENTER 0x2,0x0
24ba:00dc  MOV byte ptr [BP + -0x2],0xab
24ba:00e0  JMP 0x2000:4c85
24ba:00e2  DEC byte ptr [BP + -0x2]
24ba:00e5  MOV AL,byte ptr [BP + -0x2]
24ba:00e8  XOR AH,AH
24ba:00ea  MOV DI,AX
24ba:00ec  CMP byte ptr [DI + 0x783b],0x0
24ba:00f1  JZ 0x2000:4c99
24ba:00f3  MOV byte ptr [BP + -0x1],0x1
24ba:00f7  JMP 0x2000:4ca3
24ba:00f9  CMP byte ptr [BP + -0x2],0x1
24ba:00fd  JNZ 0x2000:4c82
24ba:00ff  MOV byte ptr [BP + -0x1],0x0
24ba:0103  MOV AL,byte ptr [BP + -0x1]
24ba:0106  LEAVE
24ba:0107  RETF
