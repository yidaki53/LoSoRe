; FUN_1000_a8f7  entry=1000:a8f7 size=189
1000:a8f7  PUSH BP
1000:a8f8  MOV BP,SP
1000:a8fa  MOV AX,0x10c
1000:a8fd  CALLF 0x2000:5300
1000:a902  SUB SP,0x10c
1000:a906  MOV BX,SS
1000:a908  MOV BX,ES
1000:a90a  MOV BX,DS
1000:a90c  CLD
1000:a90d  LEA DI,[BP + 0xff00]
1000:a911  LDS SI,[BP + 0xa]
1000:a914  LODSB SI
1000:a915  STOSB ES:DI
1000:a916  XCHG AX,CX
1000:a917  XOR CH,CH
1000:a919  MOVSB.REP ES:DI,SI
1000:a91b  MOV BX,DS
1000:a91d  LES DI,[BP + 0x6]
1000:a920  XOR AX,AX
1000:a922  MOV word ptr ES:[DI],AX
1000:a925  MOV word ptr ES:[DI + 0x2],AX
1000:a929  MOV AL,byte ptr [BP + 0xff00]
1000:a92d  XOR AH,AH
1000:a92f  XOR DX,DX
1000:a931  MOV word ptr [BP + 0xfef4],AX
1000:a935  MOV word ptr [BP + 0xfef6],DX
1000:a939  MOV AX,0x1
1000:a93c  XOR DX,DX
1000:a93e  CMP DX,word ptr [BP + 0xfef6]
1000:a942  JG 0x1000:a9b0
1000:a944  JL 0x1000:a94c
1000:a946  CMP AX,word ptr [BP + 0xfef4]
1000:a94a  JA 0x1000:a9b0
1000:a94c  MOV word ptr [BP + 0xfef8],AX
1000:a950  MOV word ptr [BP + 0xfefa],DX
1000:a954  JMP 0x1000:a960
1000:a956  ADD word ptr [BP + 0xfef8],0x1
1000:a95b  ADC word ptr [BP + 0xfefa],0x0
1000:a960  LES DI,[BP + 0x6]
1000:a963  MOV AX,word ptr ES:[DI]
1000:a966  MOV DX,word ptr ES:[DI + 0x2]
1000:a96a  MOV CX,0xa
1000:a96d  XOR BX,BX
1000:a96f  CALLF 0x2000:8b50
1000:a974  MOV word ptr [BP + 0xfefc],AX
1000:a978  MOV word ptr [BP + 0xfefe],DX
1000:a97c  MOV DI,word ptr [BP + 0xfef8]
1000:a980  MOV AL,byte ptr [BP + DI + 0xff00]
1000:a984  XOR AH,AH
1000:a986  SUB AX,0x30
1000:a989  CWD
1000:a98a  ADD AX,word ptr [BP + 0xfefc]
1000:a98e  ADC DX,word ptr [BP + 0xfefe]
1000:a992  LES DI,[BP + 0x6]
1000:a995  MOV word ptr ES:[DI],AX
1000:a998  MOV word ptr ES:[DI + 0x2],DX
1000:a99c  MOV AX,word ptr [BP + 0xfef8]
1000:a9a0  MOV DX,word ptr [BP + 0xfefa]
1000:a9a4  CMP DX,word ptr [BP + 0xfef6]
1000:a9a8  JNZ 0x1000:a956
1000:a9aa  CMP AX,word ptr [BP + 0xfef4]
1000:a9ae  JNZ 0x1000:a956
1000:a9b0  LEAVE
1000:a9b1  RET 0xa
