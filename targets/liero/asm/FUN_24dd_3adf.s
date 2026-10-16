; FUN_24dd_3adf  entry=24dd:3adf size=66
24dd:3adf  PUSH BP
24dd:3ae0  MOV BP,SP
24dd:3ae2  SUB SP,0x40
24dd:3ae5  MOV CX,word ptr [BP + 0x6]
24dd:3ae8  OR CX,CX
24dd:3aea  JNS 0x2000:88ca
24dd:3aec  MOV CX,0x8
24dd:3aef  SUB CX,word ptr [BP + 0x8]
24dd:3af2  CMP CX,-0x2
24dd:3af5  JLE 0x2000:88ca
24dd:3af7  MOV CX,0xfffe
24dd:3afa  LEA DI,[BP + -0x40]
24dd:3afd  PUSH SS
24dd:3afe  POP ES
24dd:3aff  CALL 0x2000:8130
24dd:3b02  LES BX,[BP + 0xa]
24dd:3b05  MOV DX,word ptr [BP + 0x8]
24dd:3b08  SUB DX,CX
24dd:3b0a  JLE 0x2000:88e1
24dd:3b0c  PUSH CX
24dd:3b0d  CALL 0x2000:861a
24dd:3b10  POP CX
24dd:3b11  MOV AX,CX
24dd:3b13  LEA SI,[BP + -0x40]
24dd:3b16  MOV DX,SS
24dd:3b18  CALL 0x2000:8669
24dd:3b1b  MOV SP,BP
24dd:3b1d  POP BP
24dd:3b1e  RETF 0x4
