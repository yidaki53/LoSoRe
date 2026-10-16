; FUN_24dd_1277  entry=24dd:1277 size=589
24dd:1277  PUSH BP
24dd:1278  MOV BP,SP
24dd:127a  LEA SP,[BP + -0x8]
24dd:127d  MOV BX,word ptr [BP + 0x8]
24dd:1280  PUSH word ptr [BX + 0x6]
24dd:1283  PUSH word ptr [BX + 0x4]
24dd:1286  PUSH word ptr [BX + 0x2]
24dd:1289  PUSH word ptr [BX]
24dd:128b  SUB AX,AX
24dd:128d  PUSH AX
24dd:128e  PUSH SI
24dd:128f  PUSH DI
24dd:1290  CLD
24dd:1291  MOV DI,word ptr [BP + 0x6]
24dd:1294  MOV AL,byte ptr [BX + 0xa]
24dd:1297  XOR AL,byte ptr [DI + 0xa]
24dd:129a  MOV byte ptr [BP + -0x3],AL
24dd:129d  MOV SI,word ptr [DI + 0x8]
24dd:12a0  MOV AX,word ptr [BX + 0x8]
24dd:12a3  CMP SI,0x4001
24dd:12a7  JGE 0x2000:60b7
24dd:12a9  CMP AX,0x4001
24dd:12ac  JGE 0x2000:60cd
24dd:12ae  CMP SI,0xc001
24dd:12b2  JLE 0x2000:60a3
24dd:12b4  CMP AX,0xc001
24dd:12b7  JLE 0x2000:609a
24dd:12b9  SUB AX,SI
24dd:12bb  CMP AX,0x4001
24dd:12be  JGE 0x2000:609f
24dd:12c0  CMP AX,0xc001
24dd:12c3  JG 0x2000:60dc
24dd:12c5  MOV CH,0x10
24dd:12c7  CALL 0x2000:7131
24dd:12ca  MOV AX,0xc001
24dd:12cd  JMP 0x2000:60ab
24dd:12cf  MOV CH,0x8
24dd:12d1  JMP 0x2000:60a5
24dd:12d3  MOV CH,0x4
24dd:12d5  CALL 0x2000:7131
24dd:12d8  MOV AX,0x4001
24dd:12db  MOV CL,byte ptr [BP + -0x3]
24dd:12de  MOV DI,word ptr [BP + 0x4]
24dd:12e1  CALL 0x2000:53cd
24dd:12e4  JMP 0x2000:628c
24dd:12e7  MOV SI,DI
24dd:12e9  MOV DI,word ptr [BP + 0x4]
24dd:12ec  CALL 0x2000:5c27
24dd:12ef  JC 0x2000:60b4
24dd:12f1  CMP word ptr [BX + 0x8],0x4001
24dd:12f6  JL 0x2000:609a
24dd:12f8  CALL 0x2000:53df
24dd:12fb  JMP 0x2000:60b4
24dd:12fd  MOV SI,BX
24dd:12ff  MOV BX,0xffff
24dd:1302  MOV DI,word ptr [BP + 0x4]
24dd:1305  CALL 0x2000:5c27
24dd:1308  JC 0x2000:60b4
24dd:130a  JMP 0x2000:60a8
24dd:130c  MOV word ptr [BP + -0x2],AX
24dd:130f  SUB CX,CX
24dd:1311  MOV DX,word ptr [BP + -0xa]
24dd:1314  MOV SI,word ptr [DI + 0x6]
24dd:1317  CMP SI,DX
24dd:1319  JA 0x2000:60ee
24dd:131b  SUB DX,SI
24dd:131d  INC CX
24dd:131e  MOV AX,word ptr [BP + -0xc]
24dd:1321  DIV SI
24dd:1323  ADC AX,0x1
24dd:1326  ADC CL,CH
24dd:1328  MOV byte ptr [BP + -0x4],CL
24dd:132b  MOV word ptr [BP + -0x6],AX
24dd:132e  PUSH AX
24dd:132f  MOV AX,word ptr [DI]
24dd:1331  MOV BX,word ptr [DI + 0x2]
24dd:1334  JCXZ 0x2000:6117
24dd:1336  MOV DX,word ptr [DI + 0x4]
24dd:1339  SUB word ptr [BP + -0x10],AX
24dd:133c  SBB word ptr [BP + -0xe],BX
24dd:133f  SBB word ptr [BP + -0xc],DX
24dd:1342  SBB word ptr [BP + -0xa],SI
24dd:1345  LOOP 0x2000:6109
24dd:1347  POP SI
24dd:1348  MUL SI
24dd:134a  MOV word ptr [BP + -0x12],AX
24dd:134d  XCHG AX,DX
24dd:134e  XCHG AX,BX
24dd:134f  MUL SI
24dd:1351  ADD BX,AX
24dd:1353  ADC CX,DX
24dd:1355  MOV AX,word ptr [DI + 0x4]
24dd:1358  MUL SI
24dd:135a  ADD CX,AX
24dd:135c  ADC DX,0x0
24dd:135f  XCHG AX,DX
24dd:1360  XCHG AX,SI
24dd:1361  MUL word ptr [DI + 0x6]
24dd:1364  ADD AX,SI
24dd:1366  ADC DX,0x0
24dd:1369  SUB BX,word ptr [BP + -0x10]
24dd:136c  SBB CX,word ptr [BP + -0xe]
24dd:136f  SBB AX,word ptr [BP + -0xc]
24dd:1372  SBB DX,word ptr [BP + -0xa]
24dd:1375  MOV word ptr [BP + -0x10],BX
24dd:1378  MOV word ptr [BP + -0xe],CX
24dd:137b  MOV word ptr [BP + -0xc],AX
24dd:137e  MOV SI,word ptr [DI + 0x6]
24dd:1381  DIV SI
24dd:1383  XCHG AX,CX
24dd:1384  DIV SI
24dd:1386  SUB DX,DX
24dd:1388  STC
24dd:1389  ADC AX,DX
24dd:138b  ADC CX,DX
24dd:138d  SUB DX,AX
24dd:138f  MOV word ptr [BP + -0x8],DX
24dd:1392  SBB word ptr [BP + -0x6],CX
24dd:1395  SBB byte ptr [BP + -0x4],0x0
24dd:1399  PUSH AX
24dd:139a  MOV AX,word ptr [DI]
24dd:139c  MOV BX,word ptr [DI + 0x2]
24dd:139f  JCXZ 0x2000:6182
24dd:13a1  MOV DX,word ptr [DI + 0x4]
24dd:13a4  SUB word ptr [BP + -0x12],AX
24dd:13a7  SBB word ptr [BP + -0x10],BX
24dd:13aa  SBB word ptr [BP + -0xe],DX
24dd:13ad  SBB word ptr [BP + -0xc],SI
24dd:13b0  LOOP 0x2000:6174
24dd:13b2  POP SI
24dd:13b3  MUL SI
24dd:13b5  XCHG AX,DX
24dd:13b6  XCHG AX,BX
24dd:13b7  MUL SI
24dd:13b9  ADD BX,AX
24dd:13bb  ADC CX,DX
24dd:13bd  MOV AX,word ptr [DI + 0x4]
24dd:13c0  MUL SI
24dd:13c2  ADD CX,AX
24dd:13c4  ADC DX,0x0
24dd:13c7  XCHG AX,DX
24dd:13c8  XCHG AX,SI
24dd:13c9  MUL word ptr [DI + 0x6]
24dd:13cc  ADD AX,SI
24dd:13ce  ADC DX,0x0
24dd:13d1  SUB BX,word ptr [BP + -0x12]
24dd:13d4  SBB CX,word ptr [BP + -0x10]
24dd:13d7  SBB AX,word ptr [BP + -0xe]
24dd:13da  SBB DX,word ptr [BP + -0xc]
24dd:13dd  MOV word ptr [BP + -0x12],BX
24dd:13e0  MOV word ptr [BP + -0x10],CX
24dd:13e3  MOV word ptr [BP + -0xe],AX
24dd:13e6  MOV SI,word ptr [DI + 0x6]
24dd:13e9  DIV SI
24dd:13eb  XCHG AX,CX
24dd:13ec  DIV SI
24dd:13ee  SUB DX,DX
24dd:13f0  STC
24dd:13f1  ADC AX,DX
24dd:13f3  ADC CX,DX
24dd:13f5  MOV word ptr [BP + -0xa],AX
24dd:13f8  ADD word ptr [BP + -0x8],CX
24dd:13fb  ADC word ptr [BP + -0x6],DX
24dd:13fe  ADC byte ptr [BP + -0x4],DL
24dd:1401  XCHG AX,SI
24dd:1402  MOV DX,word ptr [DI + 0x2]
24dd:1405  XCHG AX,DX
24dd:1406  MOV BX,word ptr [DI + 0x4]
24dd:1409  JCXZ 0x2000:61e6
24dd:140b  SUB word ptr [BP + -0x12],AX
24dd:140e  SBB word ptr [BP + -0x10],BX
24dd:1411  SBB word ptr [BP + -0xe],DX
24dd:1414  LOOP 0x2000:61db
24dd:1416  MUL SI
24dd:1418  XCHG AX,DX
24dd:1419  XCHG AX,BX
24dd:141a  MUL SI
24dd:141c  ADD BX,AX
24dd:141e  ADC CX,DX
24dd:1420  MOV AX,word ptr [DI + 0x6]
24dd:1423  MUL SI
24dd:1425  ADD AX,CX
24dd:1427  ADC DX,0x0
24dd:142a  SUB BX,word ptr [BP + -0x12]
24dd:142d  SBB AX,word ptr [BP + -0x10]
24dd:1430  SBB DX,word ptr [BP + -0xe]
24dd:1433  MOV word ptr [BP + -0x12],BX
24dd:1436  MOV word ptr [BP + -0x10],AX
24dd:1439  MOV SI,word ptr [DI + 0x4]
24dd:143c  ADD SI,SI
24dd:143e  MOV SI,word ptr [DI + 0x6]
24dd:1441  ADC SI,0x0
24dd:1444  JNC 0x2000:621a
24dd:1446  XCHG DX,BX
24dd:1448  JMP 0x2000:622b
24dd:144a  SHL BX,0x1
24dd:144c  RCL AX,0x1
24dd:144e  RCL DX,0x1
24dd:1450  DIV SI
24dd:1452  XCHG AX,BX
24dd:1453  DIV SI
24dd:1455  SHR BX,0x1
24dd:1457  RCR AX,0x1
24dd:1459  RCR DH,0x1
24dd:145b  MOV CX,0xffff
24dd:145e  MOV SI,CX
24dd:1460  MOV DL,CL
24dd:1462  NOT BX
24dd:1464  NOT AX
24dd:1466  NEG DH
24dd:1468  CMC
24dd:1469  ADC AX,0x0
24dd:146c  ADC BX,word ptr [BP + -0xa]
24dd:146f  ADC CX,word ptr [BP + -0x8]
24dd:1472  ADC SI,word ptr [BP + -0x6]
24dd:1475  ADC DL,byte ptr [BP + -0x4]
24dd:1478  SHR DL,0x1
24dd:147a  JNC 0x2000:6259
24dd:147c  RCR SI,0x1
24dd:147e  RCR CX,0x1
24dd:1480  RCR BX,0x1
24dd:1482  RCR AX,0x1
24dd:1484  RCR DH,0x1
24dd:1486  INC word ptr [BP + -0x2]
24dd:1489  SUB DI,DI
24dd:148b  ADD DH,DH
24dd:148d  ADC AX,DI
24dd:148f  ADC BX,DI
24dd:1491  ADC CX,DI
24dd:1493  ADC SI,DI
24dd:1495  ADC DL,0x0
24dd:1498  MOV DX,word ptr [BP + -0x2]
24dd:149b  JZ 0x2000:6271
24dd:149d  MOV SI,0x8000
24dd:14a0  INC DX
24dd:14a1  CMP DX,0x4001
24dd:14a5  JL 0x2000:627a
24dd:14a7  JMP 0x2000:60a8
24dd:14aa  MOV DI,word ptr [BP + 0x4]
24dd:14ad  CLD
24dd:14ae  STOSW ES:DI
24dd:14af  XCHG AX,BX
24dd:14b0  STOSW ES:DI
24dd:14b1  XCHG AX,CX
24dd:14b2  STOSW ES:DI
24dd:14b3  XCHG AX,SI
24dd:14b4  STOSW ES:DI
24dd:14b5  XCHG AX,DX
24dd:14b6  STOSW ES:DI
24dd:14b7  MOV AL,byte ptr [BP + -0x3]
24dd:14ba  CBW
24dd:14bb  STOSW ES:DI
24dd:14bc  POP DI
24dd:14bd  POP SI
24dd:14be  MOV SP,BP
24dd:14c0  POP BP
24dd:14c1  RET 0x6
