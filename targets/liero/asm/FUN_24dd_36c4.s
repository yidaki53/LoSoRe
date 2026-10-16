; FUN_24dd_36c4  entry=24dd:36c4 size=73
24dd:36c4  PUSH BP
24dd:36c5  MOV BP,SP
24dd:36c7  LES DI,[BP + 0x6]
24dd:36ca  MOV AX,word ptr ES:[DI + 0x2]
24dd:36ce  CMP AX,0xd7b1
24dd:36d1  JZ 0x2000:84b5
24dd:36d3  CMP AX,0xd7b2
24dd:36d6  JZ 0x2000:84b5
24dd:36d8  CMP AX,0xd7b0
24dd:36db  JZ 0x2000:84bd
24dd:36dd  MOV word ptr [0x6410],0x66
24dd:36e3  JMP 0x2000:84d9
24dd:36e5  PUSH DX
24dd:36e6  PUSH ES
24dd:36e7  PUSH DI
24dd:36e8  PUSH CS
24dd:36e9  CALL 0x2000:84e1
24dd:36ec  POP DX
24dd:36ed  XOR AX,AX
24dd:36ef  MOV word ptr ES:[DI + 0x2],DX
24dd:36f3  MOV word ptr ES:[DI + 0x8],AX
24dd:36f7  MOV word ptr ES:[DI + 0xa],AX
24dd:36fb  MOV BX,0x10
24dd:36fe  CALL 0x2000:851d
24dd:3701  JZ 0x2000:84d9
24dd:3703  MOV word ptr ES:[DI + 0x2],0xd7b0
24dd:3709  POP BP
24dd:370a  RETF 0x4
