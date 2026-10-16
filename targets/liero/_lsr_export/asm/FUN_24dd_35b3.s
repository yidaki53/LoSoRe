; FUN_24dd_35b3  entry=24dd:35b3 size=33
24dd:35b3  XOR BX,BX
24dd:35b5  JCXZ 0x2000:83a3
24dd:35b7  MOV AL,byte ptr ES:[DI]
24dd:35ba  SUB AL,0x3a
24dd:35bc  ADD AL,0xa
24dd:35be  JNC 0x2000:83a3
24dd:35c0  INT 0x3c
24dd:35c2  CALLF 0xa000:4d2e
24dd:35c7  MOV word ptr [BP + -0x4],AX
24dd:35ca  INT 0x3a
24dd:35cc  INC SI
24dd:35cd  CLD
24dd:35ce  INC BX
24dd:35cf  INC DI
24dd:35d0  DEC CX
24dd:35d1  JMP 0x2000:8385
24dd:35d3  RET
