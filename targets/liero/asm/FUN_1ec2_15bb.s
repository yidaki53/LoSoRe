; FUN_1ec2_15bb  entry=1ec2:15bb size=94
1ec2:15bb  ENTER 0x2,0x0
1ec2:15bf  MOV byte ptr [BP + -0x1],0x0
1ec2:15c3  JMP 0x2000:01e8
1ec2:15c5  INC byte ptr [BP + -0x1]
1ec2:15c8  LEA DI,[BP + -0x1]
1ec2:15cb  PUSH SS
1ec2:15cc  PUSH DI
1ec2:15cd  MOV AL,byte ptr [BP + -0x1]
1ec2:15d0  XOR AH,AH
1ec2:15d2  MOV SI,AX
1ec2:15d4  SHL AX,0x1
1ec2:15d6  ADD AX,SI
1ec2:15d8  LES DI,[BP + 0x6]
1ec2:15db  ADD DI,AX
1ec2:15dd  PUSH ES
1ec2:15de  PUSH DI
1ec2:15df  MOV AL,byte ptr [BP + -0x1]
1ec2:15e2  XOR AH,AH
1ec2:15e4  MOV SI,AX
1ec2:15e6  SHL AX,0x1
1ec2:15e8  ADD AX,SI
1ec2:15ea  LES DI,[BP + 0x6]
1ec2:15ed  ADD DI,AX
1ec2:15ef  ADD DI,0x1
1ec2:15f3  PUSH ES
1ec2:15f4  PUSH DI
1ec2:15f5  MOV AL,byte ptr [BP + -0x1]
1ec2:15f8  XOR AH,AH
1ec2:15fa  MOV SI,AX
1ec2:15fc  SHL AX,0x1
1ec2:15fe  ADD AX,SI
1ec2:1600  LES DI,[BP + 0x6]
1ec2:1603  ADD DI,AX
1ec2:1605  ADD DI,0x2
1ec2:1609  PUSH ES
1ec2:160a  PUSH DI
1ec2:160b  PUSH CS
1ec2:160c  CALL 0x2000:014f
1ec2:160f  CMP byte ptr [BP + -0x1],0xff
1ec2:1613  JNZ 0x2000:01e5
1ec2:1615  LEAVE
1ec2:1616  RETF 0x4
