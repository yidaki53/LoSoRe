; FUN_1ea2_01a8  entry=1ea2:01a8 size=72
1ea2:01a8  PUSH BP
1ea2:01a9  MOV BP,SP
1ea2:01ab  CLI
1ea2:01ac  PUSH DS
1ea2:01ad  LDS SI,[BP + 0x10]
1ea2:01b0  LES DI,[BP + 0x6]
1ea2:01b3  MOV BX,0x140
1ea2:01b6  SUB BX,word ptr [BP + 0xc]
1ea2:01b9  MOV AX,word ptr [BP + 0xe]
1ea2:01bc  SUB AX,word ptr [BP + 0xc]
1ea2:01bf  SHR word ptr [BP + 0xc],0x1
1ea2:01c2  JNC 0x1000:ebf9
1ea2:01c4  MOV DX,word ptr [BP + 0xa]
1ea2:01c7  XOR CX,CX
1ea2:01c9  ADD CX,word ptr [BP + 0xc]
1ea2:01cc  MOVSB ES:DI,SI
1ea2:01cd  MOVSW.REP ES:DI,SI
1ea2:01cf  ADD DI,BX
1ea2:01d1  ADD SI,AX
1ea2:01d3  DEC DX
1ea2:01d4  JNZ 0x1000:ebe9
1ea2:01d6  POP DS
1ea2:01d7  JMP 0x1000:ec0b
1ea2:01d9  MOV DX,word ptr [BP + 0xa]
1ea2:01dc  XOR CX,CX
1ea2:01de  ADD CX,word ptr [BP + 0xc]
1ea2:01e1  MOVSW.REP ES:DI,SI
1ea2:01e3  ADD DI,BX
1ea2:01e5  ADD SI,AX
1ea2:01e7  DEC DX
1ea2:01e8  JNZ 0x1000:ebfe
1ea2:01ea  POP DS
1ea2:01eb  STI
1ea2:01ec  LEAVE
1ea2:01ed  RETF 0xe
