; FUN_202c_0673  entry=202c:0673 size=147
202c:0673  ENTER 0x10a,0x0
202c:0677  MOV BX,SS
202c:0679  MOV BX,ES
202c:067b  MOV BX,DS
202c:067d  CLD
202c:067e  LEA DI,[BP + 0xfefe]
202c:0682  LDS SI,[BP + 0x6]
202c:0685  LODSB SI
202c:0686  STOSB ES:DI
202c:0687  XCHG AX,CX
202c:0688  XOR CH,CH
202c:068a  MOVSB.REP ES:DI,SI
202c:068c  MOV BX,DS
202c:068e  MOV word ptr [BP + 0xfefa],0x1
202c:0694  MOV AL,byte ptr [BP + 0xfefe]
202c:0698  XOR AH,AH
202c:069a  MOV word ptr [BP + 0xfef6],AX
202c:069e  MOV AX,0x1
202c:06a1  CMP AX,word ptr [BP + 0xfef6]
202c:06a5  JG 0x2000:09b6
202c:06a7  MOV word ptr [BP + 0xfefc],AX
202c:06ab  JMP 0x2000:0971
202c:06ad  INC word ptr [BP + 0xfefc]
202c:06b1  MOV DI,word ptr [BP + 0xfefc]
202c:06b5  MOV AL,byte ptr [BP + DI + 0xfefe]
202c:06b9  MOV byte ptr [BP + 0xfef9],AL
202c:06bd  CMP byte ptr [BP + 0xfef9],0xff
202c:06c2  JNZ 0x2000:0989
202c:06c4  ADD word ptr [BP + 0xfefc],0x2
202c:06c9  MOV DI,word ptr [BP + 0xfefc]
202c:06cd  MOV AL,byte ptr [BP + DI + 0xfefe]
202c:06d1  MOV byte ptr [BP + 0xfef9],AL
202c:06d5  MOV AL,byte ptr [BP + 0xfef9]
202c:06d9  XOR AH,AH
202c:06db  DEC AX
202c:06dc  DEC AX
202c:06dd  MOV DI,AX
202c:06df  SHL DI,0x6
202c:06e2  MOV AL,byte ptr [DI + 0x19e5]
202c:06e6  XOR AH,AH
202c:06e8  ADD word ptr [BP + 0xfefa],AX
202c:06ec  MOV AX,word ptr [BP + 0xfefc]
202c:06f0  CMP AX,word ptr [BP + 0xfef6]
202c:06f4  JNZ 0x2000:096d
202c:06f6  MOV AX,word ptr [BP + 0xfefa]
202c:06fa  INC AX
202c:06fb  INC AX
202c:06fc  MOV word ptr [BP + -0x2],AX
202c:06ff  MOV AX,word ptr [BP + -0x2]
202c:0702  LEAVE
202c:0703  RETF 0x4
