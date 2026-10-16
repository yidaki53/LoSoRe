; FUN_24dd_029f  entry=24dd:029f size=26
24dd:029f  PUSH BP
24dd:02a0  MOV BP,SP
24dd:02a2  MOV AX,word ptr [BP + 0x6]
24dd:02a5  LES CX,[BP + 0x8]
24dd:02a8  MOV BX,ES
24dd:02aa  CALL 0x2000:51ee
24dd:02ad  POP BP
24dd:02ae  JC 0x2000:5083
24dd:02b0  RETF 0x6
24dd:02b3  MOV AX,0xcc
24dd:02b6  JMP 0x2000:4edf
