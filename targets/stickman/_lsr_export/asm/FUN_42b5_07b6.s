; FUN_42b5_07b6  entry=42b5:07b6 size=36
42b5:07b6  CMP word ptr [0x39c],0x0
42b5:07bb  JNZ 0x4000:3315
42b5:07bd  CMP word ptr ES:[DI + 0x2],0xd7b2
42b5:07c3  JNZ 0x4000:3322
42b5:07c5  MOV BX,word ptr ES:[DI + 0x8]
42b5:07c9  MOV DX,word ptr ES:[DI + 0x4]
42b5:07cd  LES DI,ES:[DI + 0xc]
42b5:07d1  RET
42b5:07d2  MOV word ptr [0x39c],0x69
42b5:07d8  JMP 0x4000:3315
