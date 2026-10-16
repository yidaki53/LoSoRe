; FUN_24dd_39c3  entry=24dd:39c3 size=44
24dd:39c3  PUSH BP
24dd:39c4  MOV BP,SP
24dd:39c6  LES BX,[BP + 0x8]
24dd:39c9  MOV AL,byte ptr ES:[BX]
24dd:39cc  XOR AH,AH
24dd:39ce  LES BX,[BP + 0xc]
24dd:39d1  MOV DX,word ptr [BP + 0x6]
24dd:39d4  SUB DX,AX
24dd:39d6  JLE 0x2000:87ad
24dd:39d8  PUSH AX
24dd:39d9  CALL 0x2000:861a
24dd:39dc  POP AX
24dd:39dd  OR AX,AX
24dd:39df  JZ 0x2000:87bb
24dd:39e1  MOV SI,word ptr [BP + 0x8]
24dd:39e4  MOV DX,word ptr [BP + 0xa]
24dd:39e7  INC SI
24dd:39e8  CALL 0x2000:8669
24dd:39eb  POP BP
24dd:39ec  RETF 0x6
