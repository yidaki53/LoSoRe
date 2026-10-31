; FUN_428f_008e  entry=428f:008e size=20
428f:008e  PUSH BP
428f:008f  MOV BP,SP
428f:0091  MOV CX,word ptr [BP + 0xa]
428f:0094  MOV DH,byte ptr [BP + 0x8]
428f:0097  MOV DL,byte ptr [BP + 0x6]
428f:009a  MOV AH,0x2b
428f:009c  INT 0x21
428f:009e  POP BP
428f:009f  RETF 0x6
