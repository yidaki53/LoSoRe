; FUN_24dd_1190  entry=24dd:1190 size=231
24dd:1190  PUSH BP
24dd:1191  PUSH DI
24dd:1192  MOV BP,word ptr [0xd8]
24dd:1196  SUB DI,DI
24dd:1198  MOV CX,DI
24dd:119a  MOV SI,DI
24dd:119c  TEST byte ptr [BP + 0xf],0x80
24dd:11a0  JZ 0x2000:5f78
24dd:11a2  MOV CX,word ptr [BP + 0x0]
24dd:11a5  MOV SI,word ptr [BP + 0x2]
24dd:11a8  TEST byte ptr [BP + 0x3],0x80
24dd:11ac  JZ 0x2000:5f8d
24dd:11ae  ADD CX,word ptr [BP + 0xc]
24dd:11b1  ADC SI,word ptr [BP + 0xe]
24dd:11b4  ADC DI,DI
24dd:11b6  TEST byte ptr [BP + 0xf],0x80
24dd:11ba  JZ 0x2000:5f8d
24dd:11bc  DEC DI
24dd:11bd  SUB BX,BX
24dd:11bf  MOV AX,word ptr [BP + 0xc]
24dd:11c2  MUL word ptr [BP + 0x4]
24dd:11c5  ADD CX,AX
24dd:11c7  ADC SI,DX
24dd:11c9  ADC DI,0x0
24dd:11cc  MOV AX,word ptr [BP + 0x10]
24dd:11cf  OR AX,AX
24dd:11d1  JZ 0x2000:5fba
24dd:11d3  MUL word ptr [BP + 0x0]
24dd:11d6  ADD CX,AX
24dd:11d8  ADC SI,DX
24dd:11da  ADC DI,0x0
24dd:11dd  MOV AX,word ptr [BP + 0x10]
24dd:11e0  MUL word ptr [BP + 0x2]
24dd:11e3  ADD SI,AX
24dd:11e5  ADC DI,DX
24dd:11e7  ADC BX,0x0
24dd:11ea  MOV AX,word ptr [BP + 0xc]
24dd:11ed  MUL word ptr [BP + 0x6]
24dd:11f0  ADD SI,AX
24dd:11f2  ADC DI,DX
24dd:11f4  ADC BX,0x0
24dd:11f7  MOV AX,word ptr [BP + 0xe]
24dd:11fa  MUL word ptr [BP + 0x4]
24dd:11fd  ADD SI,AX
24dd:11ff  ADC DI,DX
24dd:1201  ADC BX,0x0
24dd:1204  MOV AX,word ptr [BP + 0x12]
24dd:1207  OR AX,AX
24dd:1209  JZ 0x2000:5fe5
24dd:120b  MUL word ptr [BP + 0x0]
24dd:120e  ADD SI,AX
24dd:1210  ADC DI,DX
24dd:1212  ADC BX,0x0
24dd:1215  SUB CX,CX
24dd:1217  PUSH SI
24dd:1218  MOV SI,CX
24dd:121a  MOV AX,word ptr [BP + 0xe]
24dd:121d  MUL word ptr [BP + 0x6]
24dd:1220  ADD DI,AX
24dd:1222  ADC BX,DX
24dd:1224  ADC CX,0x0
24dd:1227  MOV AX,word ptr [BP + 0x10]
24dd:122a  OR AX,AX
24dd:122c  JZ 0x2000:6015
24dd:122e  MUL word ptr [BP + 0x4]
24dd:1231  ADD DI,AX
24dd:1233  ADC BX,DX
24dd:1235  ADC CX,0x0
24dd:1238  MOV AX,word ptr [BP + 0x10]
24dd:123b  MUL word ptr [BP + 0x6]
24dd:123e  ADD BX,AX
24dd:1240  ADC CX,DX
24dd:1242  ADC SI,0x0
24dd:1245  MOV AX,word ptr [BP + 0x12]
24dd:1248  OR AX,AX
24dd:124a  JZ 0x2000:6040
24dd:124c  MUL word ptr [BP + 0x2]
24dd:124f  ADD DI,AX
24dd:1251  ADC BX,DX
24dd:1253  ADC CX,0x0
24dd:1256  ADC SI,0x0
24dd:1259  MOV AX,word ptr [BP + 0x12]
24dd:125c  MUL word ptr [BP + 0x4]
24dd:125f  ADD BX,AX
24dd:1261  ADC CX,DX
24dd:1263  ADC SI,0x0
24dd:1266  MOV AX,word ptr [BP + 0x12]
24dd:1269  MUL word ptr [BP + 0x6]
24dd:126c  ADD CX,AX
24dd:126e  ADC SI,DX
24dd:1270  MOV DX,SI
24dd:1272  XCHG AX,DI
24dd:1273  POP SI
24dd:1274  POP DI
24dd:1275  POP BP
24dd:1276  RET
