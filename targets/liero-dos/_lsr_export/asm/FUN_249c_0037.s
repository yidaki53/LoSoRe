; FUN_249c_0037  entry=249c:0037 size=290
249c:0037  ENTER 0x10a,0x0
249c:003b  MOV BX,SS
249c:003d  MOV BX,ES
249c:003f  MOV BX,DS
249c:0041  CLD
249c:0042  LEA DI,[BP + 0xff00]
249c:0046  LDS SI,[BP + 0x6]
249c:0049  LODSB SI
249c:004a  STOSB ES:DI
249c:004b  XCHG AX,CX
249c:004c  XOR CH,CH
249c:004e  MOVSB.REP ES:DI,SI
249c:0050  MOV BX,DS
249c:0052  MOV byte ptr [BP + 0xfefc],0x7
249c:0057  MOV byte ptr [BP + 0xfefb],0x0
249c:005c  PUSH BP
249c:005d  CALL 0x2000:49d3
249c:0060  MOV AL,byte ptr [BP + 0xc]
249c:0063  XOR AH,AH
249c:0065  MOV DX,AX
249c:0067  MOV AL,byte ptr [BP + 0xa]
249c:006a  XOR AH,AH
249c:006c  IMUL AX,AX,0x50
249c:006f  ADD AX,DX
249c:0071  SHL AX,0x1
249c:0073  MOV word ptr [BP + 0xfef8],AX
249c:0077  MOV AL,byte ptr [BP + 0xc]
249c:007a  PUSH AX
249c:007b  MOV AL,byte ptr [BP + 0xa]
249c:007e  PUSH AX
249c:007f  PUSH CS
249c:0080  CALL 0x2000:49c0
249c:0083  MOV byte ptr [BP + 0xfeff],0x0
249c:0088  MOV AL,byte ptr [BP + 0xff00]
249c:008c  MOV byte ptr [BP + 0xfef7],AL
249c:0090  MOV AL,0x1
249c:0092  CMP AL,byte ptr [BP + 0xfef7]
249c:0096  JBE 0x2000:4a5b
249c:0098  JMP 0x2000:4aee
249c:009b  MOV byte ptr [BP + 0xfefa],AL
249c:009f  JMP 0x2000:4a65
249c:00a1  INC byte ptr [BP + 0xfefa]
249c:00a5  MOV AL,byte ptr [BP + 0xfefa]
249c:00a9  XOR AH,AH
249c:00ab  MOV DI,AX
249c:00ad  MOV AL,byte ptr [BP + DI + 0xff00]
249c:00b1  MOV byte ptr [BP + 0xfefe],AL
249c:00b5  MOV AL,byte ptr [BP + 0xfeff]
249c:00b9  CMP AL,0x0
249c:00bb  JNZ 0x2000:4ab5
249c:00bd  CMP byte ptr [BP + 0xfefe],0x0
249c:00c2  JNZ 0x2000:4a8b
249c:00c4  MOV byte ptr [BP + 0xfeff],0x1
249c:00c9  JMP 0x2000:4ab3
249c:00cb  MOV DL,byte ptr [BP + 0xfefe]
249c:00cf  MOV AX,0xb800
249c:00d2  PUSH AX
249c:00d3  MOV DI,word ptr [BP + 0xfef8]
249c:00d7  POP ES
249c:00d8  MOV byte ptr ES:[DI],DL
249c:00db  INC word ptr [BP + 0xfef8]
249c:00df  MOV DL,byte ptr [BP + 0xfefd]
249c:00e3  MOV AX,0xb800
249c:00e6  PUSH AX
249c:00e7  MOV DI,word ptr [BP + 0xfef8]
249c:00eb  POP ES
249c:00ec  MOV byte ptr ES:[DI],DL
249c:00ef  INC word ptr [BP + 0xfef8]
249c:00f3  JMP 0x2000:4ae1
249c:00f5  CMP AL,0x1
249c:00f7  JNZ 0x2000:4acc
249c:00f9  MOV byte ptr [BP + 0xfeff],0x2
249c:00fe  MOV AL,byte ptr [BP + 0xfefe]
249c:0102  MOV byte ptr [BP + 0xfefc],AL
249c:0106  PUSH BP
249c:0107  CALL 0x2000:49d3
249c:010a  JMP 0x2000:4ae1
249c:010c  CMP AL,0x2
249c:010e  JNZ 0x2000:4ae1
249c:0110  MOV byte ptr [BP + 0xfeff],0x0
249c:0115  MOV AL,byte ptr [BP + 0xfefe]
249c:0119  MOV byte ptr [BP + 0xfefb],AL
249c:011d  PUSH BP
249c:011e  CALL 0x2000:49d3
249c:0121  MOV AL,byte ptr [BP + 0xfefa]
249c:0125  CMP AL,byte ptr [BP + 0xfef7]
249c:0129  JZ 0x2000:4aee
249c:012b  JMP 0x2000:4a61
249c:012e  MOV AL,byte ptr [BP + 0xff00]
249c:0132  XOR AH,AH
249c:0134  MOV DX,AX
249c:0136  MOV AL,byte ptr [BP + 0xc]
249c:0139  XOR AH,AH
249c:013b  ADD AX,DX
249c:013d  PUSH AX
249c:013e  MOV AL,byte ptr [BP + 0xa]
249c:0141  PUSH AX
249c:0142  PUSH CS
249c:0143  CALL 0x2000:49c0
249c:0146  MOV DI,0x79f0
249c:0149  PUSH DS
249c:014a  PUSH DI
249c:014b  CALLF 0x2000:8700
249c:0150  CALLF 0x2000:52c4
249c:0155  LEAVE
249c:0156  RETF 0x8
