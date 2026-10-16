; FUN_1ec2_13e9  entry=1ec2:13e9 size=326
1ec2:13e9  ENTER 0x10a,0x0
1ec2:13ed  MOV BX,SS
1ec2:13ef  MOV BX,ES
1ec2:13f1  MOV BX,DS
1ec2:13f3  CLD
1ec2:13f4  LEA DI,[BP + 0xff00]
1ec2:13f8  LDS SI,[BP + 0x10]
1ec2:13fb  LODSB SI
1ec2:13fc  STOSB ES:DI
1ec2:13fd  XCHG AX,CX
1ec2:13fe  XOR CH,CH
1ec2:1400  MOVSB.REP ES:DI,SI
1ec2:1402  MOV BX,DS
1ec2:1404  LES DI,[BP + 0x6]
1ec2:1407  MOV AL,byte ptr ES:[DI + 0x273f]
1ec2:140c  MOV [0x65f0],AL
1ec2:140f  MOV AX,word ptr [BP + 0x16]
1ec2:1412  MOV word ptr [BP + 0xfef8],AX
1ec2:1416  MOV AL,byte ptr [BP + 0xe]
1ec2:1419  MOV byte ptr [BP + 0xfefc],AL
1ec2:141d  MOV AL,byte ptr [BP + 0xff00]
1ec2:1421  XOR AH,AH
1ec2:1423  MOV word ptr [BP + 0xfef6],AX
1ec2:1427  MOV AX,0x1
1ec2:142a  CMP AX,word ptr [BP + 0xfef6]
1ec2:142e  JLE 0x2000:0053
1ec2:1430  JMP 0x2000:014b
1ec2:1433  MOV word ptr [BP + 0xfefe],AX
1ec2:1437  JMP 0x2000:005d
1ec2:1439  INC word ptr [BP + 0xfefe]
1ec2:143d  MOV DI,word ptr [BP + 0xfefe]
1ec2:1441  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:1445  MOV byte ptr [BP + 0xfefd],AL
1ec2:1449  CMP byte ptr [BP + 0xfefd],0x0
1ec2:144e  JA 0x2000:0073
1ec2:1450  JMP 0x2000:012f
1ec2:1453  CMP byte ptr [BP + 0xfefd],0xff
1ec2:1458  JNZ 0x2000:00a0
1ec2:145a  INC word ptr [BP + 0xfefe]
1ec2:145e  CMP byte ptr [BP + 0xfefc],0x1
1ec2:1463  JNZ 0x2000:0090
1ec2:1465  MOV DI,word ptr [BP + 0xfefe]
1ec2:1469  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:146d  MOV byte ptr [BP + 0xe],AL
1ec2:1470  INC word ptr [BP + 0xfefe]
1ec2:1474  MOV DI,word ptr [BP + 0xfefe]
1ec2:1478  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:147c  MOV byte ptr [BP + 0xfefd],AL
1ec2:1480  SUB byte ptr [BP + 0xfefd],0x2
1ec2:1485  MOV AL,byte ptr [BP + 0xfefd]
1ec2:1489  XOR AH,AH
1ec2:148b  SHL AX,0x6
1ec2:148e  LES DI,[BP + 0x6]
1ec2:1491  ADD DI,AX
1ec2:1493  MOV AL,byte ptr ES:[DI + 0x3f]
1ec2:1497  MOV byte ptr [BP + 0xfefb],AL
1ec2:149b  MOV AL,byte ptr [BP + 0xfefb]
1ec2:149f  XOR AH,AH
1ec2:14a1  MOV DX,AX
1ec2:14a3  MOV AX,0x13f
1ec2:14a6  SUB AX,DX
1ec2:14a8  CMP AX,word ptr [BP + 0x16]
1ec2:14ab  JL 0x2000:00f2
1ec2:14ad  PUSH word ptr [BP + 0x16]
1ec2:14b0  PUSH word ptr [BP + 0x14]
1ec2:14b3  LES DI,[BP + 0xa]
1ec2:14b6  PUSH ES
1ec2:14b7  PUSH DI
1ec2:14b8  MOV AL,byte ptr [BP + 0xfefd]
1ec2:14bc  XOR AH,AH
1ec2:14be  SHL AX,0x6
1ec2:14c1  LES DI,[BP + 0x6]
1ec2:14c4  ADD DI,AX
1ec2:14c6  PUSH ES
1ec2:14c7  PUSH DI
1ec2:14c8  MOV AL,byte ptr [BP + 0xe]
1ec2:14cb  PUSH AX
1ec2:14cc  PUSH CS
1ec2:14cd  CALL 0x2000:ff06
1ec2:14d0  JMP 0x2000:0124
1ec2:14d2  MOV AL,[0x65f0]
1ec2:14d5  XOR AH,AH
1ec2:14d7  ADD word ptr [BP + 0x14],AX
1ec2:14da  MOV AX,word ptr [BP + 0xfef8]
1ec2:14de  MOV word ptr [BP + 0x16],AX
1ec2:14e1  PUSH word ptr [BP + 0x16]
1ec2:14e4  PUSH word ptr [BP + 0x14]
1ec2:14e7  LES DI,[BP + 0xa]
1ec2:14ea  PUSH ES
1ec2:14eb  PUSH DI
1ec2:14ec  MOV AL,byte ptr [BP + 0xfefd]
1ec2:14f0  XOR AH,AH
1ec2:14f2  SHL AX,0x6
1ec2:14f5  LES DI,[BP + 0x6]
1ec2:14f8  ADD DI,AX
1ec2:14fa  PUSH ES
1ec2:14fb  PUSH DI
1ec2:14fc  MOV AL,byte ptr [BP + 0xe]
1ec2:14ff  PUSH AX
1ec2:1500  PUSH CS
1ec2:1501  CALL 0x2000:ff06
1ec2:1504  MOV AL,byte ptr [BP + 0xfefb]
1ec2:1508  XOR AH,AH
1ec2:150a  ADD word ptr [BP + 0x16],AX
1ec2:150d  JMP 0x2000:013e
1ec2:150f  MOV AL,[0x65f0]
1ec2:1512  XOR AH,AH
1ec2:1514  ADD word ptr [BP + 0x14],AX
1ec2:1517  MOV AX,word ptr [BP + 0xfef8]
1ec2:151b  MOV word ptr [BP + 0x16],AX
1ec2:151e  MOV AX,word ptr [BP + 0xfefe]
1ec2:1522  CMP AX,word ptr [BP + 0xfef6]
1ec2:1526  JZ 0x2000:014b
1ec2:1528  JMP 0x2000:0059
1ec2:152b  LEAVE
1ec2:152c  RETF 0x12
