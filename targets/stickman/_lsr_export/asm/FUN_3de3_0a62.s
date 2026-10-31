; FUN_3de3_0a62  entry=3de3:0a62 size=213
3de3:0a62  PUSH BP
3de3:0a63  MOV BP,SP
3de3:0a65  MOV AX,0x6
3de3:0a68  CALLF 0x4000:302f
3de3:0a6d  SUB SP,0x6
3de3:0a70  CALLF 0x4000:0824
3de3:0a75  OR AL,AL
3de3:0a77  JZ 0x3000:e8bc
3de3:0a79  MOV byte ptr [BP + -0x1],0x1
3de3:0a7d  CALLF 0x4000:1796
3de3:0a82  MOV [0xa7d2],AX
3de3:0a85  MOV word ptr [0xa7d4],DX
3de3:0a89  JMP 0x3000:e960
3de3:0a8c  MOV byte ptr [BP + -0x1],0x0
3de3:0a90  CALLF 0x4000:1796
3de3:0a95  MOV word ptr [BP + -0x6],AX
3de3:0a98  MOV word ptr [BP + -0x4],DX
3de3:0a9b  MOV AX,word ptr [BP + -0x6]
3de3:0a9e  MOV DX,word ptr [BP + -0x4]
3de3:0aa1  CMP DX,word ptr [0xa7d4]
3de3:0aa5  JL 0x3000:e8df
3de3:0aa7  JG 0x3000:e8f1
3de3:0aa9  CMP AX,word ptr [0xa7d2]
3de3:0aad  JNC 0x3000:e8f1
3de3:0aaf  MOV AX,word ptr [BP + -0x6]
3de3:0ab2  MOV DX,word ptr [BP + -0x4]
3de3:0ab5  ADD AX,0xf85d
3de3:0ab8  ADC DX,0x17
3de3:0abb  MOV word ptr [BP + -0x6],AX
3de3:0abe  MOV word ptr [BP + -0x4],DX
3de3:0ac1  MOV AX,[0xa7d2]
3de3:0ac4  MOV DX,word ptr [0xa7d4]
3de3:0ac8  ADD AX,word ptr [0x132]
3de3:0acc  ADC DX,word ptr [0x134]
3de3:0ad0  SUB AX,0x111
3de3:0ad3  SBB DX,0x0
3de3:0ad6  CMP DX,word ptr [BP + -0x4]
3de3:0ad9  JL 0x3000:e912
3de3:0adb  JG 0x3000:e93c
3de3:0add  CMP AX,word ptr [BP + -0x6]
3de3:0ae0  JNC 0x3000:e93c
3de3:0ae2  MOV AX,[0x14a]
3de3:0ae5  MOV DX,word ptr [0x14c]
3de3:0ae9  CMP DX,word ptr [0xa7d4]
3de3:0aed  JNZ 0x3000:e925
3de3:0aef  CMP AX,word ptr [0xa7d2]
3de3:0af3  JZ 0x3000:e93c
3de3:0af5  MOV AX,[0xa7d2]
3de3:0af8  MOV DX,word ptr [0xa7d4]
3de3:0afc  MOV [0x14a],AX
3de3:0aff  MOV word ptr [0x14c],DX
3de3:0b03  MOV DI,0xa12
3de3:0b06  PUSH CS
3de3:0b07  PUSH DI
3de3:0b08  PUSH CS
3de3:0b09  CALL 0x3000:de5d
3de3:0b0c  MOV AX,[0xa7d2]
3de3:0b0f  MOV DX,word ptr [0xa7d4]
3de3:0b13  ADD AX,word ptr [0x132]
3de3:0b17  ADC DX,word ptr [0x134]
3de3:0b1b  CMP DX,word ptr [BP + -0x4]
3de3:0b1e  JL 0x3000:e957
3de3:0b20  JG 0x3000:e960
3de3:0b22  CMP AX,word ptr [BP + -0x6]
3de3:0b25  JNC 0x3000:e960
3de3:0b27  MOV DI,0xa49
3de3:0b2a  PUSH CS
3de3:0b2b  PUSH DI
3de3:0b2c  PUSH CS
3de3:0b2d  CALL 0x3000:e0a8
3de3:0b30  MOV AL,byte ptr [BP + -0x1]
3de3:0b33  MOV SP,BP
3de3:0b35  POP BP
3de3:0b36  RETF
