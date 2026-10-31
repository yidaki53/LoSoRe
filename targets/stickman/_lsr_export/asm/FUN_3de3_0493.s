; FUN_3de3_0493  entry=3de3:0493 size=172
3de3:0493  PUSH BP
3de3:0494  MOV BP,SP
3de3:0496  MOV AX,0x8
3de3:0499  CALLF 0x4000:302f
3de3:049e  SUB SP,0x8
3de3:04a1  LES DI,[BP + 0x4]
3de3:04a4  MOV word ptr ES:[DI],0x7bc
3de3:04a9  LES DI,[BP + 0x4]
3de3:04ac  MOV word ptr ES:[DI + 0x2],0x1
3de3:04b2  LES DI,[BP + 0x4]
3de3:04b5  MOV word ptr ES:[DI + 0x4],0x1
3de3:04bb  MOV AX,word ptr [BP + 0x8]
3de3:04be  MOV DX,word ptr [BP + 0xa]
3de3:04c1  MOV CX,0x5180
3de3:04c4  MOV BX,0x1
3de3:04c7  CALLF 0x4000:367f
3de3:04cc  MOV AX,CX
3de3:04ce  MOV DX,BX
3de3:04d0  MOV word ptr [BP + 0x8],AX
3de3:04d3  MOV word ptr [BP + 0xa],DX
3de3:04d6  MOV AX,word ptr [BP + 0x8]
3de3:04d9  MOV DX,word ptr [BP + 0xa]
3de3:04dc  MOV CX,0xe10
3de3:04df  XOR BX,BX
3de3:04e1  CALLF 0x4000:367f
3de3:04e6  LES DI,[BP + 0x4]
3de3:04e9  MOV word ptr ES:[DI + 0x6],AX
3de3:04ed  MOV AX,word ptr [BP + 0x8]
3de3:04f0  MOV DX,word ptr [BP + 0xa]
3de3:04f3  MOV CX,0xe10
3de3:04f6  XOR BX,BX
3de3:04f8  CALLF 0x4000:367f
3de3:04fd  MOV AX,CX
3de3:04ff  MOV DX,BX
3de3:0501  MOV word ptr [BP + 0x8],AX
3de3:0504  MOV word ptr [BP + 0xa],DX
3de3:0507  MOV AX,word ptr [BP + 0x8]
3de3:050a  MOV DX,word ptr [BP + 0xa]
3de3:050d  MOV CX,0x3c
3de3:0510  XOR BX,BX
3de3:0512  CALLF 0x4000:367f
3de3:0517  LES DI,[BP + 0x4]
3de3:051a  MOV word ptr ES:[DI + 0x8],AX
3de3:051e  MOV AX,word ptr [BP + 0x8]
3de3:0521  MOV DX,word ptr [BP + 0xa]
3de3:0524  MOV CX,0x3c
3de3:0527  XOR BX,BX
3de3:0529  CALLF 0x4000:367f
3de3:052e  MOV AX,CX
3de3:0530  MOV DX,BX
3de3:0532  LES DI,[BP + 0x4]
3de3:0535  MOV word ptr ES:[DI + 0xa],AX
3de3:0539  MOV SP,BP
3de3:053b  POP BP
3de3:053c  RET 0x8
