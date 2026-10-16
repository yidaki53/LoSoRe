; FUN_1e7d_018a  entry=1e7d:018a size=192
1e7d:018a  ENTER 0x30a,0x0
1e7d:018e  LEA DI,[BP + 0xfcf6]
1e7d:0192  PUSH SS
1e7d:0193  PUSH DI
1e7d:0194  LEA DI,[BP + 0xfdf6]
1e7d:0198  PUSH SS
1e7d:0199  PUSH DI
1e7d:019a  LEA DI,[BP + 0xfef6]
1e7d:019e  PUSH SS
1e7d:019f  PUSH DI
1e7d:01a0  MOV DI,0x182
1e7d:01a3  PUSH CS
1e7d:01a4  PUSH DI
1e7d:01a5  CALLF 0x2000:8c65
1e7d:01aa  CALLF 0x2000:4d57
1e7d:01af  CALL 0x1000:e7d0
1e7d:01b2  LEA DI,[BP + 0xfefe]
1e7d:01b6  PUSH SS
1e7d:01b7  PUSH DI
1e7d:01b8  PUSH 0xff
1e7d:01bb  CALLF 0x2000:8c7f
1e7d:01c0  LEA DI,[BP + 0xfefe]
1e7d:01c4  PUSH SS
1e7d:01c5  PUSH DI
1e7d:01c6  PUSH 0x41
1e7d:01c8  PUSH 0x1
1e7d:01ca  CALL 0x1000:e852
1e7d:01cd  LES DI,[BP + 0x12]
1e7d:01d0  MOV word ptr ES:[DI],AX
1e7d:01d3  LEA DI,[BP + 0xfefe]
1e7d:01d7  PUSH SS
1e7d:01d8  PUSH DI
1e7d:01d9  PUSH 0x49
1e7d:01db  PUSH 0x0
1e7d:01dd  CALL 0x1000:e852
1e7d:01e0  LES DI,[BP + 0xe]
1e7d:01e3  MOV byte ptr ES:[DI],AL
1e7d:01e6  LEA DI,[BP + 0xfefe]
1e7d:01ea  PUSH SS
1e7d:01eb  PUSH DI
1e7d:01ec  PUSH 0x44
1e7d:01ee  PUSH 0x0
1e7d:01f0  CALL 0x1000:e852
1e7d:01f3  LES DI,[BP + 0xa]
1e7d:01f6  MOV byte ptr ES:[DI],AL
1e7d:01f9  LEA DI,[BP + 0xfefe]
1e7d:01fd  PUSH SS
1e7d:01fe  PUSH DI
1e7d:01ff  PUSH 0x48
1e7d:0201  PUSH 0x0
1e7d:0203  CALL 0x1000:e852
1e7d:0206  LES DI,[BP + 0x6]
1e7d:0209  MOV byte ptr ES:[DI],AL
1e7d:020c  MOV byte ptr [BP + -0x1],0x1
1e7d:0210  CMP byte ptr [BP + 0xfefe],0x0
1e7d:0215  JNZ 0x1000:e9eb
1e7d:0217  MOV byte ptr [BP + -0x1],0x0
1e7d:021b  LES DI,[BP + 0x12]
1e7d:021e  CMP word ptr ES:[DI],0xff
1e7d:0223  JNZ 0x1000:e9f9
1e7d:0225  MOV byte ptr [BP + -0x1],0x0
1e7d:0229  LES DI,[BP + 0xe]
1e7d:022c  CMP byte ptr ES:[DI],0xff
1e7d:0230  JNZ 0x1000:ea06
1e7d:0232  MOV byte ptr [BP + -0x1],0x0
1e7d:0236  LES DI,[BP + 0xa]
1e7d:0239  CMP byte ptr ES:[DI],0xff
1e7d:023d  JNZ 0x1000:ea13
1e7d:023f  MOV byte ptr [BP + -0x1],0x0
1e7d:0243  MOV AL,byte ptr [BP + -0x1]
1e7d:0246  LEAVE
1e7d:0247  RETF 0x10
