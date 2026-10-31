; FUN_3de3_1256  entry=3de3:1256 size=544
3de3:1256  PUSH BP
3de3:1257  MOV BP,SP
3de3:1259  MOV AX,0x4
3de3:125c  CALLF 0x4000:302f
3de3:1261  SUB SP,0x4
3de3:1264  MOV DI,0xa8d6
3de3:1267  PUSH DS
3de3:1268  PUSH DI
3de3:1269  MOV DI,0xa8d8
3de3:126c  PUSH DS
3de3:126d  PUSH DI
3de3:126e  MOV DI,0xa8da
3de3:1271  PUSH DS
3de3:1272  PUSH DI
3de3:1273  LEA DI,[BP + -0x4]
3de3:1276  PUSH SS
3de3:1277  PUSH DI
3de3:1278  CALLF 0x4000:295c
3de3:127d  MOV DI,0xa8dc
3de3:1280  PUSH DS
3de3:1281  PUSH DI
3de3:1282  MOV DI,0xa8de
3de3:1285  PUSH DS
3de3:1286  PUSH DI
3de3:1287  MOV DI,0xa8e0
3de3:128a  PUSH DS
3de3:128b  PUSH DI
3de3:128c  LEA DI,[BP + -0x4]
3de3:128f  PUSH SS
3de3:1290  PUSH DI
3de3:1291  CALLF 0x4000:2992
3de3:1296  MOV AX,[0xa8de]
3de3:1299  XOR DX,DX
3de3:129b  ADD AX,word ptr [0xa7ca]
3de3:129f  ADC DX,word ptr [0xa7cc]
3de3:12a3  MOV [0xa8de],AX
3de3:12a6  CMP word ptr [0xa8de],0x3b
3de3:12ab  JA 0x3000:f0e0
3de3:12ad  JMP 0x3000:f1b1
3de3:12b0  MOV AX,[0xa8de]
3de3:12b3  XOR DX,DX
3de3:12b5  MOV CX,0x3c
3de3:12b8  DIV CX
3de3:12ba  ADD AX,word ptr [0xa8dc]
3de3:12be  MOV [0xa8dc],AX
3de3:12c1  MOV AX,[0xa8de]
3de3:12c4  XOR DX,DX
3de3:12c6  MOV CX,0x3c
3de3:12c9  DIV CX
3de3:12cb  XCHG AX,DX
3de3:12cc  MOV [0xa8de],AX
3de3:12cf  CMP word ptr [0xa8dc],0x17
3de3:12d4  JBE 0x3000:f125
3de3:12d6  MOV AX,[0xa8dc]
3de3:12d9  XOR DX,DX
3de3:12db  MOV CX,0x18
3de3:12de  DIV CX
3de3:12e0  ADD AX,word ptr [0xa8da]
3de3:12e4  MOV [0xa8da],AX
3de3:12e7  MOV AX,[0xa8dc]
3de3:12ea  XOR DX,DX
3de3:12ec  MOV CX,0x18
3de3:12ef  DIV CX
3de3:12f1  XCHG AX,DX
3de3:12f2  MOV [0xa8dc],AX
3de3:12f5  MOV AX,[0xa8d8]
3de3:12f8  CMP AX,0x4
3de3:12fb  JZ 0x3000:f13c
3de3:12fd  CMP AX,0x5
3de3:1300  JZ 0x3000:f13c
3de3:1302  CMP AX,0x9
3de3:1305  JZ 0x3000:f13c
3de3:1307  CMP AX,0xb
3de3:130a  JNZ 0x3000:f14b
3de3:130c  CMP word ptr [0xa8da],0x1e
3de3:1311  MOV AL,0x0
3de3:1313  JBE 0x3000:f146
3de3:1315  INC AX
3de3:1316  MOV byte ptr [BP + -0x1],AL
3de3:1319  JMP 0x3000:f18a
3de3:131b  CMP AX,0x2
3de3:131e  JNZ 0x3000:f17d
3de3:1320  MOV AX,[0xa8d6]
3de3:1323  XOR DX,DX
3de3:1325  MOV CX,0x4
3de3:1328  DIV CX
3de3:132a  XCHG AX,DX
3de3:132b  OR AX,AX
3de3:132d  JNZ 0x3000:f16e
3de3:132f  CMP word ptr [0xa8da],0x1d
3de3:1334  MOV AL,0x0
3de3:1336  JBE 0x3000:f169
3de3:1338  INC AX
3de3:1339  MOV byte ptr [BP + -0x1],AL
3de3:133c  JMP 0x3000:f17b
3de3:133e  CMP word ptr [0xa8da],0x1c
3de3:1343  MOV AL,0x0
3de3:1345  JBE 0x3000:f178
3de3:1347  INC AX
3de3:1348  MOV byte ptr [BP + -0x1],AL
3de3:134b  JMP 0x3000:f18a
3de3:134d  CMP word ptr [0xa8da],0x1f
3de3:1352  MOV AL,0x0
3de3:1354  JBE 0x3000:f187
3de3:1356  INC AX
3de3:1357  MOV byte ptr [BP + -0x1],AL
3de3:135a  CMP byte ptr [BP + -0x1],0x0
3de3:135e  JZ 0x3000:f1b1
3de3:1360  MOV word ptr [0xa8da],0x1
3de3:1366  MOV AX,[0xa8d8]
3de3:1369  INC AX
3de3:136a  MOV [0xa8d8],AX
3de3:136d  CMP word ptr [0xa8d8],0xc
3de3:1372  JBE 0x3000:f1b1
3de3:1374  MOV word ptr [0xa8d8],0x1
3de3:137a  MOV AX,[0xa8d6]
3de3:137d  INC AX
3de3:137e  MOV [0xa8d6],AX
3de3:1381  MOV AX,[0xa8d6]
3de3:1384  SUB AX,0x76c
3de3:1387  MOV [0xa8d6],AX
3de3:138a  MOV AX,[0xa8d6]
3de3:138d  XOR DX,DX
3de3:138f  MOV [0xa7c6],AX
3de3:1392  MOV word ptr [0xa7c8],DX
3de3:1396  MOV AX,[0xa7c6]
3de3:1399  MOV DX,word ptr [0xa7c8]
3de3:139d  MOV CX,0xc
3de3:13a0  XOR BX,BX
3de3:13a2  CALLF 0x4000:3664
3de3:13a7  MOV [0xa7c6],AX
3de3:13aa  MOV word ptr [0xa7c8],DX
3de3:13ae  MOV AX,[0xa8d8]
3de3:13b1  XOR DX,DX
3de3:13b3  ADD AX,word ptr [0xa7c6]
3de3:13b7  ADC DX,word ptr [0xa7c8]
3de3:13bb  MOV [0xa7c6],AX
3de3:13be  MOV word ptr [0xa7c8],DX
3de3:13c2  MOV AX,[0xa7c6]
3de3:13c5  MOV DX,word ptr [0xa7c8]
3de3:13c9  MOV CX,0x1f
3de3:13cc  XOR BX,BX
3de3:13ce  CALLF 0x4000:3664
3de3:13d3  MOV [0xa7c6],AX
3de3:13d6  MOV word ptr [0xa7c8],DX
3de3:13da  MOV AX,[0xa8da]
3de3:13dd  XOR DX,DX
3de3:13df  ADD AX,word ptr [0xa7c6]
3de3:13e3  ADC DX,word ptr [0xa7c8]
3de3:13e7  MOV [0xa7c6],AX
3de3:13ea  MOV word ptr [0xa7c8],DX
3de3:13ee  MOV AX,[0xa7c6]
3de3:13f1  MOV DX,word ptr [0xa7c8]
3de3:13f5  MOV CX,0x18
3de3:13f8  XOR BX,BX
3de3:13fa  CALLF 0x4000:3664
3de3:13ff  MOV [0xa7c6],AX
3de3:1402  MOV word ptr [0xa7c8],DX
3de3:1406  MOV AX,[0xa8dc]
3de3:1409  XOR DX,DX
3de3:140b  ADD AX,word ptr [0xa7c6]
3de3:140f  ADC DX,word ptr [0xa7c8]
3de3:1413  MOV [0xa7c6],AX
3de3:1416  MOV word ptr [0xa7c8],DX
3de3:141a  MOV AX,[0xa7c6]
3de3:141d  MOV DX,word ptr [0xa7c8]
3de3:1421  MOV CX,0x3c
3de3:1424  XOR BX,BX
3de3:1426  CALLF 0x4000:3664
3de3:142b  MOV [0xa7c6],AX
3de3:142e  MOV word ptr [0xa7c8],DX
3de3:1432  MOV AX,[0xa8de]
3de3:1435  XOR DX,DX
3de3:1437  ADD AX,word ptr [0xa7c6]
3de3:143b  ADC DX,word ptr [0xa7c8]
3de3:143f  MOV [0xa7c6],AX
3de3:1442  MOV word ptr [0xa7c8],DX
3de3:1446  MOV AX,[0xa7c6]
3de3:1449  MOV DX,word ptr [0xa7c8]
3de3:144d  MOV CX,0x3c
3de3:1450  XOR BX,BX
3de3:1452  CALLF 0x4000:3664
3de3:1457  MOV [0xa7c6],AX
3de3:145a  MOV word ptr [0xa7c8],DX
3de3:145e  MOV AX,[0xa8e0]
3de3:1461  XOR DX,DX
3de3:1463  ADD AX,word ptr [0xa7c6]
3de3:1467  ADC DX,word ptr [0xa7c8]
3de3:146b  MOV [0xa7c6],AX
3de3:146e  MOV word ptr [0xa7c8],DX
3de3:1472  MOV SP,BP
3de3:1474  POP BP
3de3:1475  RETF
