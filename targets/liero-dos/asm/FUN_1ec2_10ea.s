; FUN_1ec2_10ea  entry=1ec2:10ea size=203
1ec2:10ea  ENTER 0x308,0x0
1ec2:10ee  MOV BX,SS
1ec2:10f0  MOV BX,ES
1ec2:10f2  MOV BX,DS
1ec2:10f4  CLD
1ec2:10f5  LEA DI,[BP + 0xfd00]
1ec2:10f9  LDS SI,[BP + 0x8]
1ec2:10fc  MOV CX,0x300
1ec2:10ff  MOVSB.REP ES:DI,SI
1ec2:1101  MOV BX,DS
1ec2:1103  MOV byte ptr [BP + 0xfcff],0x0
1ec2:1108  JMP 0x1000:fd2e
1ec2:110a  INC byte ptr [BP + 0xfcff]
1ec2:110e  MOV AL,byte ptr [BP + 0xfcff]
1ec2:1112  XOR AH,AH
1ec2:1114  MOV DI,AX
1ec2:1116  MOV SI,DI
1ec2:1118  SHL DI,0x1
1ec2:111a  ADD DI,SI
1ec2:111c  MOV AL,byte ptr [BP + DI + 0xfd00]
1ec2:1120  XOR AH,AH
1ec2:1122  MUL word ptr [BP + 0x6]
1ec2:1125  SHR AX,0x5
1ec2:1128  MOV word ptr [BP + 0xfcfc],AX
1ec2:112c  MOV AL,byte ptr [BP + 0xfcff]
1ec2:1130  XOR AH,AH
1ec2:1132  MOV DI,AX
1ec2:1134  MOV SI,DI
1ec2:1136  SHL DI,0x1
1ec2:1138  ADD DI,SI
1ec2:113a  MOV AL,byte ptr [BP + DI + 0xfd01]
1ec2:113e  XOR AH,AH
1ec2:1140  MUL word ptr [BP + 0x6]
1ec2:1143  SHR AX,0x5
1ec2:1146  MOV word ptr [BP + 0xfcfa],AX
1ec2:114a  MOV AL,byte ptr [BP + 0xfcff]
1ec2:114e  XOR AH,AH
1ec2:1150  MOV DI,AX
1ec2:1152  MOV SI,DI
1ec2:1154  SHL DI,0x1
1ec2:1156  ADD DI,SI
1ec2:1158  MOV AL,byte ptr [BP + DI + 0xfd02]
1ec2:115c  XOR AH,AH
1ec2:115e  MUL word ptr [BP + 0x6]
1ec2:1161  SHR AX,0x5
1ec2:1164  MOV word ptr [BP + 0xfcf8],AX
1ec2:1168  CMP word ptr [BP + 0xfcfc],0x3f
1ec2:116d  JLE 0x1000:fd95
1ec2:116f  MOV word ptr [BP + 0xfcfc],0x3f
1ec2:1175  CMP word ptr [BP + 0xfcfa],0x3f
1ec2:117a  JLE 0x1000:fda2
1ec2:117c  MOV word ptr [BP + 0xfcfa],0x3f
1ec2:1182  CMP word ptr [BP + 0xfcf8],0x3f
1ec2:1187  JLE 0x1000:fdaf
1ec2:1189  MOV word ptr [BP + 0xfcf8],0x3f
1ec2:118f  MOV AL,byte ptr [BP + 0xfcff]
1ec2:1193  PUSH AX
1ec2:1194  MOV AL,byte ptr [BP + 0xfcfc]
1ec2:1198  PUSH AX
1ec2:1199  MOV AL,byte ptr [BP + 0xfcfa]
1ec2:119d  PUSH AX
1ec2:119e  MOV AL,byte ptr [BP + 0xfcf8]
1ec2:11a2  PUSH AX
1ec2:11a3  PUSH CS
1ec2:11a4  CALL 0x1000:fcef
1ec2:11a7  CMP byte ptr [BP + 0xfcff],0xff
1ec2:11ac  JZ 0x1000:fdd1
1ec2:11ae  JMP 0x1000:fd2a
1ec2:11b1  LEAVE
1ec2:11b2  RETF 0x6
