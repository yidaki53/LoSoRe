; FUN_3de3_002d  entry=3de3:002d size=100
3de3:002d  PUSH BP
3de3:002e  MOV BP,SP
3de3:0030  MOV AX,0x104
3de3:0033  CALLF 0x4000:302f
3de3:0038  SUB SP,0x104
3de3:003c  LES DI,[BP + 0x6]
3de3:003f  PUSH ES
3de3:0040  PUSH DI
3de3:0041  LEA DI,[BP + 0xff00]
3de3:0045  PUSH SS
3de3:0046  PUSH DI
3de3:0047  MOV AX,0xff
3de3:004a  PUSH AX
3de3:004b  CALLF 0x4000:372e
3de3:0050  CMP byte ptr [BP + 0xff00],0x0
3de3:0055  JZ 0x3000:debb
3de3:0057  MOV AL,byte ptr [BP + 0xff00]
3de3:005b  XOR AH,AH
3de3:005d  MOV word ptr [BP + 0xfefc],AX
3de3:0061  MOV AX,0x1
3de3:0064  CMP AX,word ptr [BP + 0xfefc]
3de3:0068  JG 0x3000:debb
3de3:006a  MOV word ptr [BP + 0xfefe],AX
3de3:006e  JMP 0x3000:dea4
3de3:0070  INC word ptr [BP + 0xfefe]
3de3:0074  MOV DI,word ptr [BP + 0xfefe]
3de3:0078  MOV AL,byte ptr [BP + DI + 0xff00]
3de3:007c  PUSH AX
3de3:007d  PUSH CS
3de3:007e  CALL 0x3000:de30
3de3:0081  MOV AX,word ptr [BP + 0xfefe]
3de3:0085  CMP AX,word ptr [BP + 0xfefc]
3de3:0089  JNZ 0x3000:dea0
3de3:008b  MOV SP,BP
3de3:008d  POP BP
3de3:008e  RETF 0x4
