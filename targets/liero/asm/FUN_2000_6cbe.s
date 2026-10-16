; FUN_2000_6cbe  entry=2000:6cbe size=57
24dd:1eee  PUSH BP
24dd:1eef  MOV BP,SP
24dd:1ef1  PUSH SI
24dd:1ef2  PUSH DI
24dd:1ef3  MOV SI,DI
24dd:1ef5  CALL 0x2000:53f8
24dd:1ef8  MOV SI,word ptr [0xd8]
24dd:1efc  CALL 0x2000:6cf7
24dd:1eff  MOV SI,0x1dbd
24dd:1f02  CALL 0x2000:5412
24dd:1f05  MOV SI,word ptr [0xd8]
24dd:1f09  PUSH SI
24dd:1f0a  LEA SI,[SI + 0xc]
24dd:1f0d  PUSH SI
24dd:1f0e  PUSH SI
24dd:1f0f  CALL 0x2000:5e77
24dd:1f12  PUSH SI
24dd:1f13  PUSH word ptr [BP + -0x2]
24dd:1f16  PUSH word ptr [BP + -0x2]
24dd:1f19  CALL 0x2000:5e77
24dd:1f1c  ADD word ptr [0xd8],0x18
24dd:1f21  POP DI
24dd:1f22  POP SI
24dd:1f23  MOV SP,BP
24dd:1f25  POP BP
24dd:1f26  RET
