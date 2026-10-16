; FUN_202c_0bc0  entry=202c:0bc0 size=843
202c:0bc0  ENTER 0xe,0x0
202c:0bc4  MOV AX,[0x6600]
202c:0bc7  MOV DX,word ptr [0x6602]
202c:0bcb  MOV [0x6412],AX
202c:0bce  MOV word ptr [0x6414],DX
202c:0bd2  PUSH 0x7
202c:0bd4  CALLF 0x2000:9424
202c:0bd9  ADD AX,0xc
202c:0bdc  LES DI,[0x6674]
202c:0be0  LES DI,ES:[DI]
202c:0be3  MOV byte ptr ES:[DI],AL
202c:0be6  MOV word ptr [BP + -0x2],0x1
202c:0beb  JMP 0x2000:0eb0
202c:0bed  INC word ptr [BP + -0x2]
202c:0bf0  PUSH 0x7
202c:0bf2  CALLF 0x2000:9424
202c:0bf7  MOV DX,AX
202c:0bf9  MOV AX,word ptr [BP + -0x2]
202c:0bfc  DEC AX
202c:0bfd  SHL AX,0x2
202c:0c00  LES DI,[0x6674]
202c:0c04  ADD DI,AX
202c:0c06  LES DI,ES:[DI]
202c:0c09  MOV AL,byte ptr ES:[DI]
202c:0c0c  XOR AH,AH
202c:0c0e  ADD AX,DX
202c:0c10  ADD AX,0xc
202c:0c13  SHR AX,0x1
202c:0c15  MOV DL,AL
202c:0c17  MOV AX,word ptr [BP + -0x2]
202c:0c1a  SHL AX,0x2
202c:0c1d  LES DI,[0x6674]
202c:0c21  ADD DI,AX
202c:0c23  LES DI,ES:[DI]
202c:0c26  MOV byte ptr ES:[DI],DL
202c:0c29  CMP word ptr [BP + -0x2],0x15d
202c:0c2e  JNZ 0x2000:0ead
202c:0c30  MOV word ptr [BP + -0x2],0x1
202c:0c35  JMP 0x2000:0efa
202c:0c37  INC word ptr [BP + -0x2]
202c:0c3a  PUSH 0x7
202c:0c3c  CALLF 0x2000:9424
202c:0c41  MOV DX,AX
202c:0c43  MOV AX,word ptr [BP + -0x2]
202c:0c46  DEC AX
202c:0c47  LES DI,[0x6674]
202c:0c4b  LES DI,ES:[DI]
202c:0c4e  ADD DI,AX
202c:0c50  MOV AL,byte ptr ES:[DI]
202c:0c53  XOR AH,AH
202c:0c55  ADD AX,DX
202c:0c57  ADD AX,0xc
202c:0c5a  SHR AX,0x1
202c:0c5c  MOV DL,AL
202c:0c5e  MOV AX,word ptr [BP + -0x2]
202c:0c61  LES DI,[0x6674]
202c:0c65  LES DI,ES:[DI]
202c:0c68  ADD DI,AX
202c:0c6a  MOV byte ptr ES:[DI],DL
202c:0c6d  CMP word ptr [BP + -0x2],0x1f7
202c:0c72  JNZ 0x2000:0ef7
202c:0c74  MOV word ptr [BP + -0x2],0x1
202c:0c79  JMP 0x2000:0f3e
202c:0c7b  INC word ptr [BP + -0x2]
202c:0c7e  MOV word ptr [BP + -0x4],0x1
202c:0c83  JMP 0x2000:0f48
202c:0c85  INC word ptr [BP + -0x4]
202c:0c88  PUSH 0x8
202c:0c8a  CALLF 0x2000:9424
202c:0c8f  ADD AX,0xc
202c:0c92  MOV CX,AX
202c:0c94  MOV AX,word ptr [BP + -0x4]
202c:0c97  DEC AX
202c:0c98  MOV DX,AX
202c:0c9a  MOV AX,word ptr [BP + -0x2]
202c:0c9d  SHL AX,0x2
202c:0ca0  LES DI,[0x6674]
202c:0ca4  ADD DI,AX
202c:0ca6  LES DI,ES:[DI]
202c:0ca9  ADD DI,DX
202c:0cab  MOV AL,byte ptr ES:[DI]
202c:0cae  XOR AH,AH
202c:0cb0  ADD AX,CX
202c:0cb2  MOV CX,AX
202c:0cb4  MOV DX,word ptr [BP + -0x4]
202c:0cb7  MOV AX,word ptr [BP + -0x2]
202c:0cba  DEC AX
202c:0cbb  SHL AX,0x2
202c:0cbe  LES DI,[0x6674]
202c:0cc2  ADD DI,AX
202c:0cc4  LES DI,ES:[DI]
202c:0cc7  ADD DI,DX
202c:0cc9  MOV AL,byte ptr ES:[DI]
202c:0ccc  XOR AH,AH
202c:0cce  ADD AX,CX
202c:0cd0  XOR DX,DX
202c:0cd2  MOV CX,0x3
202c:0cd5  DIV CX
202c:0cd7  MOV CL,AL
202c:0cd9  MOV DX,word ptr [BP + -0x4]
202c:0cdc  MOV AX,word ptr [BP + -0x2]
202c:0cdf  SHL AX,0x2
202c:0ce2  LES DI,[0x6674]
202c:0ce6  ADD DI,AX
202c:0ce8  LES DI,ES:[DI]
202c:0ceb  ADD DI,DX
202c:0ced  MOV byte ptr ES:[DI],CL
202c:0cf0  CMP word ptr [BP + -0x4],0x1f7
202c:0cf5  JNZ 0x2000:0f45
202c:0cf7  CMP word ptr [BP + -0x2],0x15d
202c:0cfc  JZ 0x2000:0fc1
202c:0cfe  JMP 0x2000:0f3b
202c:0d01  PUSH 0x64
202c:0d03  CALLF 0x2000:9424
202c:0d08  MOV word ptr [BP + -0xe],AX
202c:0d0b  MOV AX,0x1
202c:0d0e  CMP AX,word ptr [BP + -0xe]
202c:0d11  JLE 0x2000:0fd6
202c:0d13  JMP 0x2000:1162
202c:0d16  MOV word ptr [BP + -0x2],AX
202c:0d19  JMP 0x2000:0fde
202c:0d1b  INC word ptr [BP + -0x2]
202c:0d1e  PUSH 0x1f8
202c:0d21  CALLF 0x2000:9424
202c:0d26  SUB AX,0x8
202c:0d29  MOV word ptr [BP + -0x4],AX
202c:0d2c  PUSH 0x15e
202c:0d2f  CALLF 0x2000:9424
202c:0d34  SUB AX,0x8
202c:0d37  MOV word ptr [BP + -0x6],AX
202c:0d3a  PUSH 0x4
202c:0d3c  CALLF 0x2000:9424
202c:0d41  ADD AX,0x45
202c:0d44  MOV word ptr [BP + -0x8],AX
202c:0d47  XOR AX,AX
202c:0d49  MOV word ptr [BP + -0xa],AX
202c:0d4c  JMP 0x2000:1011
202c:0d4e  INC word ptr [BP + -0xa]
202c:0d51  XOR AX,AX
202c:0d53  MOV word ptr [BP + -0xc],AX
202c:0d56  JMP 0x2000:101b
202c:0d58  INC word ptr [BP + -0xc]
202c:0d5b  MOV CX,word ptr [BP + -0xa]
202c:0d5e  MOV AX,word ptr [BP + -0xc]
202c:0d61  SHL AX,0x4
202c:0d64  MOV DX,AX
202c:0d66  MOV AX,word ptr [BP + -0x8]
202c:0d69  SHL AX,0x8
202c:0d6c  LES DI,[0x6678]
202c:0d70  ADD DI,AX
202c:0d72  ADD DI,DX
202c:0d74  ADD DI,CX
202c:0d76  CMP byte ptr ES:[DI],0x0
202c:0d7a  JA 0x2000:103f
202c:0d7c  JMP 0x2000:1145
202c:0d7f  MOV AX,word ptr [BP + -0x4]
202c:0d82  ADD AX,word ptr [BP + -0xa]
202c:0d85  CMP AX,0xffff
202c:0d88  JG 0x2000:104d
202c:0d8a  JMP 0x2000:1145
202c:0d8d  MOV AX,word ptr [BP + -0x4]
202c:0d90  ADD AX,word ptr [BP + -0xa]
202c:0d93  CMP AX,0x1f8
202c:0d96  JL 0x2000:105b
202c:0d98  JMP 0x2000:1145
202c:0d9b  MOV AX,word ptr [BP + -0x6]
202c:0d9e  ADD AX,word ptr [BP + -0xc]
202c:0da1  CMP AX,0xffff
202c:0da4  JG 0x2000:1069
202c:0da6  JMP 0x2000:1145
202c:0da9  MOV AX,word ptr [BP + -0x6]
202c:0dac  ADD AX,word ptr [BP + -0xc]
202c:0daf  CMP AX,0x15e
202c:0db2  JL 0x2000:1077
202c:0db4  JMP 0x2000:1145
202c:0db7  MOV AX,word ptr [BP + -0x4]
202c:0dba  ADD AX,word ptr [BP + -0xa]
202c:0dbd  MOV DX,AX
202c:0dbf  MOV AX,word ptr [BP + -0x6]
202c:0dc2  ADD AX,word ptr [BP + -0xc]
202c:0dc5  SHL AX,0x2
202c:0dc8  LES DI,[0x6674]
202c:0dcc  ADD DI,AX
202c:0dce  LES DI,ES:[DI]
202c:0dd1  ADD DI,DX
202c:0dd3  MOV AL,byte ptr ES:[DI]
202c:0dd6  CMP AL,0xb0
202c:0dd8  JC 0x2000:1108
202c:0dda  CMP AL,0xb4
202c:0ddc  JA 0x2000:1108
202c:0dde  MOV CX,word ptr [BP + -0xa]
202c:0de1  MOV AX,word ptr [BP + -0xc]
202c:0de4  SHL AX,0x4
202c:0de7  MOV DX,AX
202c:0de9  MOV AX,word ptr [BP + -0x8]
202c:0dec  SHL AX,0x8
202c:0def  LES DI,[0x6678]
202c:0df3  ADD DI,AX
202c:0df5  ADD DI,DX
202c:0df7  ADD DI,CX
202c:0df9  MOV AL,byte ptr ES:[DI]
202c:0dfc  XOR AH,AH
202c:0dfe  MOV CX,AX
202c:0e00  MOV AX,word ptr [BP + -0x4]
202c:0e03  ADD AX,word ptr [BP + -0xa]
202c:0e06  MOV DX,AX
202c:0e08  MOV AX,word ptr [BP + -0x6]
202c:0e0b  ADD AX,word ptr [BP + -0xc]
202c:0e0e  SHL AX,0x2
202c:0e11  LES DI,[0x6674]
202c:0e15  ADD DI,AX
202c:0e17  LES DI,ES:[DI]
202c:0e1a  ADD DI,DX
202c:0e1c  MOV AL,byte ptr ES:[DI]
202c:0e1f  XOR AH,AH
202c:0e21  ADD AX,CX
202c:0e23  SHR AX,0x1
202c:0e25  MOV CL,AL
202c:0e27  MOV AX,word ptr [BP + -0x4]
202c:0e2a  ADD AX,word ptr [BP + -0xa]
202c:0e2d  MOV DX,AX
202c:0e2f  MOV AX,word ptr [BP + -0x6]
202c:0e32  ADD AX,word ptr [BP + -0xc]
202c:0e35  SHL AX,0x2
202c:0e38  LES DI,[0x6674]
202c:0e3c  ADD DI,AX
202c:0e3e  LES DI,ES:[DI]
202c:0e41  ADD DI,DX
202c:0e43  MOV byte ptr ES:[DI],CL
202c:0e46  JMP 0x2000:1145
202c:0e48  MOV CX,word ptr [BP + -0xa]
202c:0e4b  MOV AX,word ptr [BP + -0xc]
202c:0e4e  SHL AX,0x4
202c:0e51  MOV DX,AX
202c:0e53  MOV AX,word ptr [BP + -0x8]
202c:0e56  SHL AX,0x8
202c:0e59  LES DI,[0x6678]
202c:0e5d  ADD DI,AX
202c:0e5f  ADD DI,DX
202c:0e61  ADD DI,CX
202c:0e63  MOV CL,byte ptr ES:[DI]
202c:0e66  MOV AX,word ptr [BP + -0x4]
202c:0e69  ADD AX,word ptr [BP + -0xa]
202c:0e6c  MOV DX,AX
202c:0e6e  MOV AX,word ptr [BP + -0x6]
202c:0e71  ADD AX,word ptr [BP + -0xc]
202c:0e74  SHL AX,0x2
202c:0e77  LES DI,[0x6674]
202c:0e7b  ADD DI,AX
202c:0e7d  LES DI,ES:[DI]
202c:0e80  ADD DI,DX
202c:0e82  MOV byte ptr ES:[DI],CL
202c:0e85  CMP word ptr [BP + -0xc],0xf
202c:0e89  JZ 0x2000:114e
202c:0e8b  JMP 0x2000:1018
202c:0e8e  CMP word ptr [BP + -0xa],0xf
202c:0e92  JZ 0x2000:1157
202c:0e94  JMP 0x2000:100e
202c:0e97  MOV AX,word ptr [BP + -0x2]
202c:0e9a  CMP AX,word ptr [BP + -0xe]
202c:0e9d  JZ 0x2000:1162
202c:0e9f  JMP 0x2000:0fdb
202c:0ea2  PUSH 0xf
202c:0ea4  CALLF 0x2000:9424
202c:0ea9  MOV word ptr [BP + -0xe],AX
202c:0eac  MOV AX,0x1
202c:0eaf  CMP AX,word ptr [BP + -0xe]
202c:0eb2  JG 0x2000:11c7
202c:0eb4  MOV word ptr [BP + -0x2],AX
202c:0eb7  JMP 0x2000:117c
202c:0eb9  INC word ptr [BP + -0x2]
202c:0ebc  PUSH 0x1f8
202c:0ebf  CALLF 0x2000:9424
202c:0ec4  SUB AX,0x8
202c:0ec7  MOV word ptr [BP + -0x4],AX
202c:0eca  PUSH 0x15e
202c:0ecd  CALLF 0x2000:9424
202c:0ed2  SUB AX,0x8
202c:0ed5  MOV word ptr [BP + -0x6],AX
202c:0ed8  PUSH 0x4
202c:0eda  CALLF 0x2000:9424
202c:0edf  ADD AX,0x38
202c:0ee2  MOV word ptr [BP + -0x8],AX
202c:0ee5  PUSH word ptr [BP + -0x4]
202c:0ee8  PUSH word ptr [BP + -0x6]
202c:0eeb  MOV AX,word ptr [BP + -0x8]
202c:0eee  SHL AX,0x8
202c:0ef1  LES DI,[0x6678]
202c:0ef5  ADD DI,AX
202c:0ef7  PUSH ES
202c:0ef8  PUSH DI
202c:0ef9  PUSH 0x0
202c:0efb  PUSH CS
202c:0efc  CALL 0x2000:05ed
202c:0eff  MOV AX,word ptr [BP + -0x2]
202c:0f02  CMP AX,word ptr [BP + -0xe]
202c:0f05  JNZ 0x2000:1179
202c:0f07  LEAVE
202c:0f08  RET 0x2
