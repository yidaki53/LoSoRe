; FUN_42b5_0776  entry=42b5:0776 size=36
42b5:0776  CMP word ptr [0x39c],0x0
42b5:077b  JNZ 0x4000:32d5
42b5:077d  CMP word ptr ES:[DI + 0x2],0xd7b1
42b5:0783  JNZ 0x4000:32e2
42b5:0785  MOV BX,word ptr ES:[DI + 0x8]
42b5:0789  MOV DX,word ptr ES:[DI + 0xa]
42b5:078d  LES DI,ES:[DI + 0xc]
42b5:0791  RET
42b5:0792  MOV word ptr [0x39c],0x68
42b5:0798  JMP 0x4000:32d5
