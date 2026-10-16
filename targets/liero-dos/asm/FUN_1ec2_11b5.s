; FUN_1ec2_11b5  entry=1ec2:11b5 size=248
1ec2:11b5  ENTER 0x308,0x0
1ec2:11b9  MOV BX,SS
1ec2:11bb  MOV BX,ES
1ec2:11bd  MOV BX,DS
1ec2:11bf  CLD
1ec2:11c0  LEA DI,[BP + 0xfd00]
1ec2:11c4  LDS SI,[BP + 0x8]
1ec2:11c7  MOV CX,0x300
1ec2:11ca  MOVSB.REP ES:DI,SI
1ec2:11cc  MOV BX,DS
1ec2:11ce  MOV byte ptr [BP + 0xfcff],0x0
1ec2:11d3  JMP 0x1000:fdf9
1ec2:11d5  INC byte ptr [BP + 0xfcff]
1ec2:11d9  MOV AX,0x20
1ec2:11dc  SUB AX,word ptr [BP + 0x6]
1ec2:11df  MOV DX,AX
1ec2:11e1  MOV AL,byte ptr [BP + 0xfcff]
1ec2:11e5  XOR AH,AH
1ec2:11e7  MOV DI,AX
1ec2:11e9  MOV SI,DI
1ec2:11eb  SHL DI,0x1
1ec2:11ed  ADD DI,SI
1ec2:11ef  MOV AL,byte ptr [BP + DI + 0xfd00]
1ec2:11f3  XOR AH,AH
1ec2:11f5  MUL DX
1ec2:11f7  MOV DX,AX
1ec2:11f9  IMUL AX,word ptr [BP + 0x6],0x3f
1ec2:11fd  ADD AX,DX
1ec2:11ff  SHR AX,0x5
1ec2:1202  MOV word ptr [BP + 0xfcfc],AX
1ec2:1206  MOV AX,0x20
1ec2:1209  SUB AX,word ptr [BP + 0x6]
1ec2:120c  MOV DX,AX
1ec2:120e  MOV AL,byte ptr [BP + 0xfcff]
1ec2:1212  XOR AH,AH
1ec2:1214  MOV DI,AX
1ec2:1216  MOV SI,DI
1ec2:1218  SHL DI,0x1
1ec2:121a  ADD DI,SI
1ec2:121c  MOV AL,byte ptr [BP + DI + 0xfd01]
1ec2:1220  XOR AH,AH
1ec2:1222  MUL DX
1ec2:1224  MOV DX,AX
1ec2:1226  IMUL AX,word ptr [BP + 0x6],0x3f
1ec2:122a  ADD AX,DX
1ec2:122c  SHR AX,0x5
1ec2:122f  MOV word ptr [BP + 0xfcfa],AX
1ec2:1233  MOV AX,0x20
1ec2:1236  SUB AX,word ptr [BP + 0x6]
1ec2:1239  MOV DX,AX
1ec2:123b  MOV AL,byte ptr [BP + 0xfcff]
1ec2:123f  XOR AH,AH
1ec2:1241  MOV DI,AX
1ec2:1243  MOV SI,DI
1ec2:1245  SHL DI,0x1
1ec2:1247  ADD DI,SI
1ec2:1249  MOV AL,byte ptr [BP + DI + 0xfd02]
1ec2:124d  XOR AH,AH
1ec2:124f  MUL DX
1ec2:1251  MOV DX,AX
1ec2:1253  IMUL AX,word ptr [BP + 0x6],0x3f
1ec2:1257  ADD AX,DX
1ec2:1259  SHR AX,0x5
1ec2:125c  MOV word ptr [BP + 0xfcf8],AX
1ec2:1260  CMP word ptr [BP + 0xfcfc],0x3f
1ec2:1265  JLE 0x1000:fe8d
1ec2:1267  MOV word ptr [BP + 0xfcfc],0x3f
1ec2:126d  CMP word ptr [BP + 0xfcfa],0x3f
1ec2:1272  JLE 0x1000:fe9a
1ec2:1274  MOV word ptr [BP + 0xfcfa],0x3f
1ec2:127a  CMP word ptr [BP + 0xfcf8],0x3f
1ec2:127f  JLE 0x1000:fea7
1ec2:1281  MOV word ptr [BP + 0xfcf8],0x3f
1ec2:1287  MOV AL,byte ptr [BP + 0xfcff]
1ec2:128b  PUSH AX
1ec2:128c  MOV AL,byte ptr [BP + 0xfcfc]
1ec2:1290  PUSH AX
1ec2:1291  MOV AL,byte ptr [BP + 0xfcfa]
1ec2:1295  PUSH AX
1ec2:1296  MOV AL,byte ptr [BP + 0xfcf8]
1ec2:129a  PUSH AX
1ec2:129b  PUSH CS
1ec2:129c  CALL 0x1000:fcef
1ec2:129f  CMP byte ptr [BP + 0xfcff],0xff
1ec2:12a4  JZ 0x1000:fec9
1ec2:12a6  JMP 0x1000:fdf5
1ec2:12a9  LEAVE
1ec2:12aa  RETF 0x6
