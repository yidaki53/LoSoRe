; FUN_235c_0bbc  entry=235c:0bbc size=865
235c:0bbc  ENTER 0x2,0x0
235c:0bc0  XOR AX,AX
235c:0bc2  MOV word ptr [BP + -0x2],AX
235c:0bc5  JMP 0x2000:418a
235c:0bc7  INC word ptr [BP + -0x2]
235c:0bca  MOV AL,byte ptr [BP + -0x2]
235c:0bcd  PUSH AX
235c:0bce  CALL 0x2000:3edd
235c:0bd1  CMP word ptr [BP + -0x2],0x7
235c:0bd5  JNZ 0x2000:4187
235c:0bd7  MOV byte ptr [0x67ce],0x0
235c:0bdc  CMP byte ptr [0x67cd],0x0
235c:0be1  JNZ 0x2000:41a6
235c:0be3  JMP 0x2000:4340
235c:0be6  PUSH 0x1000
235c:0be9  CALLF 0x2000:505a
235c:0bee  MOV [0x6e58],AX
235c:0bf1  MOV word ptr [0x6e5a],DX
235c:0bf5  PUSH word ptr [0x6e5a]
235c:0bf9  PUSH word ptr [0x6e58]
235c:0bfd  CALL 0x2000:40bf
235c:0c00  MOV CX,0x2
235c:0c03  XOR BX,BX
235c:0c05  CALLF 0x2000:8b8d
235c:0c0a  XOR CX,CX
235c:0c0c  MOV BX,0x1
235c:0c0f  CALLF 0x2000:8b8d
235c:0c14  MOV AX,CX
235c:0c16  MOV DX,BX
235c:0c18  ADD AX,0x400
235c:0c1b  ADC DX,0x0
235c:0c1e  CMP DX,0x1
235c:0c21  JL 0x2000:41ea
235c:0c23  JG 0x2000:41fa
235c:0c25  CMP AX,0x0
235c:0c28  JNC 0x2000:41fa
235c:0c2a  MOV AX,[0x6e58]
235c:0c2d  MOV DX,word ptr [0x6e5a]
235c:0c31  MOV [0x6e60],AX
235c:0c34  MOV word ptr [0x6e62],DX
235c:0c38  JMP 0x2000:4215
235c:0c3a  LES DI,[0x6e58]
235c:0c3e  LEA AX,[DI + 0x800]
235c:0c43  LES DI,[0x6e58]
235c:0c47  MOV DX,ES
235c:0c49  PUSH DX
235c:0c4a  PUSH AX
235c:0c4b  CALL 0x2000:40f3
235c:0c4e  MOV [0x6e60],AX
235c:0c51  MOV word ptr [0x6e62],DX
235c:0c55  MOV word ptr [BP + -0x2],0x1
235c:0c5a  JMP 0x2000:421f
235c:0c5c  INC word ptr [BP + -0x2]
235c:0c5f  MOV AX,word ptr [BP + -0x2]
235c:0c62  SHL AX,0xa
235c:0c65  LES DI,[0x6e60]
235c:0c69  ADD DI,AX
235c:0c6b  ADD DI,0xfc00
235c:0c6f  PUSH ES
235c:0c70  PUSH DI
235c:0c71  CALL 0x2000:40f3
235c:0c74  MOV DI,word ptr [BP + -0x2]
235c:0c77  SHL DI,0x2
235c:0c7a  MOV word ptr [DI + 0x6e60],AX
235c:0c7e  MOV word ptr [DI + 0x6e62],DX
235c:0c82  CMP word ptr [BP + -0x2],0x2
235c:0c86  JNZ 0x2000:421c
235c:0c88  PUSH word ptr [0x6e62]
235c:0c8c  PUSH word ptr [0x6e60]
235c:0c90  CALL 0x2000:40bf
235c:0c93  MOV [0x6e70],AX
235c:0c96  MOV word ptr [0x6e72],DX
235c:0c9a  MOV AX,[0x6e70]
235c:0c9d  MOV DX,word ptr [0x6e72]
235c:0ca1  XOR CX,CX
235c:0ca3  MOV BX,0x1
235c:0ca6  CALLF 0x2000:8b8d
235c:0cab  MOV [0x6e74],AL
235c:0cae  MOV AX,[0x6e70]
235c:0cb1  MOV DX,word ptr [0x6e72]
235c:0cb5  MOV CX,0x2
235c:0cb8  XOR BX,BX
235c:0cba  CALLF 0x2000:8b8d
235c:0cbf  XOR CX,CX
235c:0cc1  MOV BX,0x1
235c:0cc4  CALLF 0x2000:8b8d
235c:0cc9  MOV AX,CX
235c:0ccb  MOV DX,BX
235c:0ccd  MOV [0x6e76],AX
235c:0cd0  MOV word ptr [BP + -0x2],0x1
235c:0cd5  JMP 0x2000:429a
235c:0cd7  INC word ptr [BP + -0x2]
235c:0cda  MOV DI,word ptr [BP + -0x2]
235c:0cdd  SHL DI,0x2
235c:0ce0  PUSH word ptr [DI + 0x6e62]
235c:0ce4  PUSH word ptr [DI + 0x6e60]
235c:0ce8  CALL 0x2000:40bf
235c:0ceb  MOV DI,word ptr [BP + -0x2]
235c:0cee  SHL DI,0x2
235c:0cf1  MOV word ptr [DI + 0x6e74],AX
235c:0cf5  MOV word ptr [DI + 0x6e76],DX
235c:0cf9  CMP word ptr [BP + -0x2],0x2
235c:0cfd  JNZ 0x2000:4297
235c:0cff  MOV word ptr [BP + -0x2],0x1
235c:0d04  JMP 0x2000:42c9
235c:0d06  INC word ptr [BP + -0x2]
235c:0d09  MOV DI,word ptr [BP + -0x2]
235c:0d0c  SHL DI,0x2
235c:0d0f  MOV AX,word ptr [DI + 0x6e74]
235c:0d13  MOV DX,word ptr [DI + 0x6e76]
235c:0d17  XOR CX,CX
235c:0d19  MOV BX,0x1
235c:0d1c  CALLF 0x2000:8b8d
235c:0d21  MOV DI,word ptr [BP + -0x2]
235c:0d24  MOV byte ptr [DI + 0x6e7f],AL
235c:0d28  CMP word ptr [BP + -0x2],0x2
235c:0d2c  JNZ 0x2000:42c6
235c:0d2e  MOV word ptr [BP + -0x2],0x1
235c:0d33  JMP 0x2000:42f8
235c:0d35  INC word ptr [BP + -0x2]
235c:0d38  MOV DI,word ptr [BP + -0x2]
235c:0d3b  SHL DI,0x2
235c:0d3e  MOV AX,word ptr [DI + 0x6e74]
235c:0d42  MOV DX,word ptr [DI + 0x6e76]
235c:0d46  MOV CX,0x2
235c:0d49  XOR BX,BX
235c:0d4b  CALLF 0x2000:8b8d
235c:0d50  XOR CX,CX
235c:0d52  MOV BX,0x1
235c:0d55  CALLF 0x2000:8b8d
235c:0d5a  MOV AX,CX
235c:0d5c  MOV DX,BX
235c:0d5e  MOV DI,word ptr [BP + -0x2]
235c:0d61  SHL DI,0x1
235c:0d63  MOV word ptr [DI + 0x6e80],AX
235c:0d67  CMP word ptr [BP + -0x2],0x2
235c:0d6b  JNZ 0x2000:42f5
235c:0d6d  LES DI,[0x6e60]
235c:0d71  PUSH ES
235c:0d72  PUSH DI
235c:0d73  PUSH 0x800
235c:0d76  PUSH 0x0
235c:0d78  CALLF 0x2000:96d5
235c:0d7d  JMP 0x2000:44bc
235c:0d80  PUSH 0x800
235c:0d83  CALLF 0x2000:505a
235c:0d88  MOV [0x6e58],AX
235c:0d8b  MOV word ptr [0x6e5a],DX
235c:0d8f  PUSH word ptr [0x6e5a]
235c:0d93  PUSH word ptr [0x6e58]
235c:0d97  CALL 0x2000:40bf
235c:0d9a  XOR CX,CX
235c:0d9c  MOV BX,0x1
235c:0d9f  CALLF 0x2000:8b8d
235c:0da4  MOV AX,CX
235c:0da6  MOV DX,BX
235c:0da8  ADD AX,0x400
235c:0dab  ADC DX,0x0
235c:0dae  CMP DX,0x1
235c:0db1  JL 0x2000:437a
235c:0db3  JG 0x2000:438a
235c:0db5  CMP AX,0x0
235c:0db8  JNC 0x2000:438a
235c:0dba  MOV AX,[0x6e58]
235c:0dbd  MOV DX,word ptr [0x6e5a]
235c:0dc1  MOV [0x6e5c],AX
235c:0dc4  MOV word ptr [0x6e5e],DX
235c:0dc8  JMP 0x2000:43a5
235c:0dca  LES DI,[0x6e58]
235c:0dce  LEA AX,[DI + 0x400]
235c:0dd3  LES DI,[0x6e58]
235c:0dd7  MOV DX,ES
235c:0dd9  PUSH DX
235c:0dda  PUSH AX
235c:0ddb  CALL 0x2000:40f3
235c:0dde  MOV [0x6e5c],AX
235c:0de1  MOV word ptr [0x6e5e],DX
235c:0de5  MOV word ptr [BP + -0x2],0x1
235c:0dea  JMP 0x2000:43af
235c:0dec  INC word ptr [BP + -0x2]
235c:0def  MOV AX,word ptr [BP + -0x2]
235c:0df2  SHL AX,0x9
235c:0df5  LES DI,[0x6e5c]
235c:0df9  ADD DI,AX
235c:0dfb  ADD DI,0xfe00
235c:0dff  PUSH ES
235c:0e00  PUSH DI
235c:0e01  CALL 0x2000:40f3
235c:0e04  MOV DI,word ptr [BP + -0x2]
235c:0e07  SHL DI,0x2
235c:0e0a  MOV word ptr [DI + 0x6e60],AX
235c:0e0e  MOV word ptr [DI + 0x6e62],DX
235c:0e12  CMP word ptr [BP + -0x2],0x2
235c:0e16  JNZ 0x2000:43ac
235c:0e18  PUSH word ptr [0x6e5e]
235c:0e1c  PUSH word ptr [0x6e5c]
235c:0e20  CALL 0x2000:40bf
235c:0e23  MOV [0x6e70],AX
235c:0e26  MOV word ptr [0x6e72],DX
235c:0e2a  MOV AX,[0x6e70]
235c:0e2d  MOV DX,word ptr [0x6e72]
235c:0e31  XOR CX,CX
235c:0e33  MOV BX,0x1
235c:0e36  CALLF 0x2000:8b8d
235c:0e3b  MOV [0x6e74],AL
235c:0e3e  MOV AX,[0x6e70]
235c:0e41  MOV DX,word ptr [0x6e72]
235c:0e45  XOR CX,CX
235c:0e47  MOV BX,0x1
235c:0e4a  CALLF 0x2000:8b8d
235c:0e4f  MOV AX,CX
235c:0e51  MOV DX,BX
235c:0e53  MOV [0x6e76],AX
235c:0e56  MOV word ptr [BP + -0x2],0x1
235c:0e5b  JMP 0x2000:4420
235c:0e5d  INC word ptr [BP + -0x2]
235c:0e60  MOV DI,word ptr [BP + -0x2]
235c:0e63  SHL DI,0x2
235c:0e66  PUSH word ptr [DI + 0x6e62]
235c:0e6a  PUSH word ptr [DI + 0x6e60]
235c:0e6e  CALL 0x2000:40bf
235c:0e71  MOV DI,word ptr [BP + -0x2]
235c:0e74  SHL DI,0x2
235c:0e77  MOV word ptr [DI + 0x6e74],AX
235c:0e7b  MOV word ptr [DI + 0x6e76],DX
235c:0e7f  CMP word ptr [BP + -0x2],0x2
235c:0e83  JNZ 0x2000:441d
235c:0e85  MOV word ptr [BP + -0x2],0x1
235c:0e8a  JMP 0x2000:444f
235c:0e8c  INC word ptr [BP + -0x2]
235c:0e8f  MOV DI,word ptr [BP + -0x2]
235c:0e92  SHL DI,0x2
235c:0e95  MOV AX,word ptr [DI + 0x6e74]
235c:0e99  MOV DX,word ptr [DI + 0x6e76]
235c:0e9d  XOR CX,CX
235c:0e9f  MOV BX,0x1
235c:0ea2  CALLF 0x2000:8b8d
235c:0ea7  MOV DI,word ptr [BP + -0x2]
235c:0eaa  MOV byte ptr [DI + 0x6e7f],AL
235c:0eae  CMP word ptr [BP + -0x2],0x2
235c:0eb2  JNZ 0x2000:444c
235c:0eb4  MOV word ptr [BP + -0x2],0x1
235c:0eb9  JMP 0x2000:447e
235c:0ebb  INC word ptr [BP + -0x2]
235c:0ebe  MOV DI,word ptr [BP + -0x2]
235c:0ec1  SHL DI,0x2
235c:0ec4  MOV AX,word ptr [DI + 0x6e74]
235c:0ec8  MOV DX,word ptr [DI + 0x6e76]
235c:0ecc  XOR CX,CX
235c:0ece  MOV BX,0x1
235c:0ed1  CALLF 0x2000:8b8d
235c:0ed6  MOV AX,CX
235c:0ed8  MOV DX,BX
235c:0eda  MOV DI,word ptr [BP + -0x2]
235c:0edd  SHL DI,0x1
235c:0edf  MOV word ptr [DI + 0x6e80],AX
235c:0ee3  CMP word ptr [BP + -0x2],0x2
235c:0ee7  JNZ 0x2000:447b
235c:0ee9  LES DI,[0x6e5c]
235c:0eed  PUSH ES
235c:0eee  PUSH DI
235c:0eef  PUSH 0x400
235c:0ef2  PUSH -0x80
235c:0ef4  CALLF 0x2000:96d5
235c:0ef9  CALL 0x2000:413c
235c:0efc  MOV DI,0x6a58
235c:0eff  PUSH DS
235c:0f00  PUSH DI
235c:0f01  PUSH 0x400
235c:0f04  PUSH 0x0
235c:0f06  CALLF 0x2000:96d5
235c:0f0b  PUSH 0x1
235c:0f0d  CALL 0x2000:406d
235c:0f10  XOR AX,AX
235c:0f12  MOV [0x67c2],AX
235c:0f15  MOV [0x67c4],AX
235c:0f18  CALL 0x2000:3961
235c:0f1b  LEAVE
235c:0f1c  RETF
