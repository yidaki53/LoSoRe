; FUN_3de3_0f2d  entry=3de3:0f2d size=67
3de3:0f2d  PUSH BP
3de3:0f2e  MOV BP,SP
3de3:0f30  XOR AX,AX
3de3:0f32  CALLF 0x4000:302f
3de3:0f37  MOV AL,[0xa8e2]
3de3:0f3a  XOR AH,AH
3de3:0f3c  MOV [0xaaec],AX
3de3:0f3f  MOV AX,[0xa8e3]
3de3:0f42  MOV DX,word ptr [0xa8e5]
3de3:0f46  MOV [0xa7ce],AX
3de3:0f49  MOV word ptr [0xa7d0],DX
3de3:0f4d  MOV DI,0xa9e8
3de3:0f50  PUSH DS
3de3:0f51  PUSH DI
3de3:0f52  MOV DI,0xa7d6
3de3:0f55  PUSH DS
3de3:0f56  PUSH DI
3de3:0f57  MOV AX,0xff
3de3:0f5a  PUSH AX
3de3:0f5b  CALLF 0x4000:372e
3de3:0f60  MOV AX,[0xaae8]
3de3:0f63  MOV DX,word ptr [0xaaea]
3de3:0f67  MOV [0xa7ca],AX
3de3:0f6a  MOV word ptr [0xa7cc],DX
3de3:0f6e  POP BP
3de3:0f6f  RETF
