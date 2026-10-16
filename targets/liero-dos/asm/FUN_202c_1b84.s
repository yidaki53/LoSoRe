; FUN_202c_1b84  entry=202c:1b84 size=5999
202c:1b84  ENTER 0x34,0x0
202c:1b88  XOR AX,AX
202c:1b8a  MOV word ptr [BP + -0x2],AX
202c:1b8d  IMUL AX,word ptr [BP + -0x2],0x7
202c:1b91  LES DI,[0x668c]
202c:1b95  ADD DI,AX
202c:1b97  CMP byte ptr ES:[DI + 0x4],0x0
202c:1b9c  JBE 0x2000:1e6a
202c:1b9e  CMP word ptr [BP + -0x2],0x2bc
202c:1ba3  JGE 0x2000:1e6a
202c:1ba5  INC word ptr [BP + -0x2]
202c:1ba8  JMP 0x2000:1e4d
202c:1baa  MOV AL,byte ptr [BP + 0xa]
202c:1bad  AND AL,0x7f
202c:1baf  MOV byte ptr [BP + -0x23],AL
202c:1bb2  CMP byte ptr [0x4b8],0x0
202c:1bb7  JZ 0x2000:1ecb
202c:1bb9  MOV AL,byte ptr [BP + -0x23]
202c:1bbc  XOR AH,AH
202c:1bbe  MOV DI,AX
202c:1bc0  CMP byte ptr [DI + 0x1391],0x0
202c:1bc5  JBE 0x2000:1ecb
202c:1bc7  MOV AL,byte ptr [BP + -0x23]
202c:1bca  XOR AH,AH
202c:1bcc  MOV DI,AX
202c:1bce  MOV AL,byte ptr [DI + 0x139f]
202c:1bd2  XOR AH,AH
202c:1bd4  PUSH AX
202c:1bd5  CALLF 0x2000:9424
202c:1bda  MOV DX,AX
202c:1bdc  MOV AL,byte ptr [BP + -0x23]
202c:1bdf  XOR AH,AH
202c:1be1  MOV DI,AX
202c:1be3  MOV AL,byte ptr [DI + 0x1391]
202c:1be7  XOR AH,AH
202c:1be9  ADD AX,DX
202c:1beb  MOV DI,AX
202c:1bed  SHL DI,0x2
202c:1bf0  PUSH word ptr [DI + 0x6736]
202c:1bf4  PUSH word ptr [DI + 0x6734]
202c:1bf8  MOV AL,byte ptr [BP + -0x23]
202c:1bfb  XOR AH,AH
202c:1bfd  MOV DI,AX
202c:1bff  MOV AL,byte ptr [DI + 0x1391]
202c:1c03  PUSH AX
202c:1c04  PUSH 0x0
202c:1c06  CALLF 0x2000:3f1c
202c:1c0b  MOV AX,word ptr [BP + 0x8]
202c:1c0e  CMP AX,word ptr [0x67b0]
202c:1c12  JLE 0x2000:1f16
202c:1c14  MOV AX,[0x67b0]
202c:1c17  ADD AX,0x9e
202c:1c1a  CMP AX,word ptr [BP + 0x8]
202c:1c1d  JLE 0x2000:1f16
202c:1c1f  MOV AX,word ptr [BP + 0x6]
202c:1c22  CMP AX,word ptr [0x67b4]
202c:1c26  JLE 0x2000:1f16
202c:1c28  MOV AX,[0x67b4]
202c:1c2b  ADD AX,0x9e
202c:1c2e  CMP AX,word ptr [BP + 0x6]
202c:1c31  JLE 0x2000:1f16
202c:1c33  MOV AL,byte ptr [BP + -0x23]
202c:1c36  XOR AH,AH
202c:1c38  MOV DI,AX
202c:1c3a  MOV AL,byte ptr [DI + 0x1435]
202c:1c3e  XOR AH,AH
202c:1c40  CMP AX,word ptr [0x67ba]
202c:1c44  JLE 0x2000:1f16
202c:1c46  MOV AL,byte ptr [BP + -0x23]
202c:1c49  XOR AH,AH
202c:1c4b  MOV DI,AX
202c:1c4d  MOV AL,byte ptr [DI + 0x1435]
202c:1c51  XOR AH,AH
202c:1c53  MOV [0x67ba],AX
202c:1c56  MOV AX,word ptr [BP + 0x8]
202c:1c59  CMP AX,word ptr [0x67b2]
202c:1c5d  JLE 0x2000:1f61
202c:1c5f  MOV AX,[0x67b2]
202c:1c62  ADD AX,0x9e
202c:1c65  CMP AX,word ptr [BP + 0x8]
202c:1c68  JLE 0x2000:1f61
202c:1c6a  MOV AX,word ptr [BP + 0x6]
202c:1c6d  CMP AX,word ptr [0x67b6]
202c:1c71  JLE 0x2000:1f61
202c:1c73  MOV AX,[0x67b6]
202c:1c76  ADD AX,0x9e
202c:1c79  CMP AX,word ptr [BP + 0x6]
202c:1c7c  JLE 0x2000:1f61
202c:1c7e  MOV AL,byte ptr [BP + -0x23]
202c:1c81  XOR AH,AH
202c:1c83  MOV DI,AX
202c:1c85  MOV AL,byte ptr [DI + 0x1435]
202c:1c89  XOR AH,AH
202c:1c8b  CMP AX,word ptr [0x67be]
202c:1c8f  JLE 0x2000:1f61
202c:1c91  MOV AL,byte ptr [BP + -0x23]
202c:1c94  XOR AH,AH
202c:1c96  MOV DI,AX
202c:1c98  MOV AL,byte ptr [DI + 0x1435]
202c:1c9c  XOR AH,AH
202c:1c9e  MOV [0x67be],AX
202c:1ca1  MOV DL,byte ptr [BP + 0xa]
202c:1ca4  IMUL AX,word ptr [BP + -0x2],0x7
202c:1ca8  LES DI,[0x668c]
202c:1cac  ADD DI,AX
202c:1cae  MOV byte ptr ES:[DI + 0x4],DL
202c:1cb2  MOV AX,word ptr [BP + 0x8]
202c:1cb5  SUB AX,0x8
202c:1cb8  MOV DX,AX
202c:1cba  IMUL AX,word ptr [BP + -0x2],0x7
202c:1cbe  LES DI,[0x668c]
202c:1cc2  ADD DI,AX
202c:1cc4  MOV word ptr ES:[DI],DX
202c:1cc7  MOV AX,word ptr [BP + 0x6]
202c:1cca  SUB AX,0x8
202c:1ccd  MOV DX,AX
202c:1ccf  IMUL AX,word ptr [BP + -0x2],0x7
202c:1cd3  LES DI,[0x668c]
202c:1cd7  ADD DI,AX
202c:1cd9  MOV word ptr ES:[DI + 0x2],DX
202c:1cdd  IMUL AX,word ptr [BP + -0x2],0x7
202c:1ce1  LES DI,[0x668c]
202c:1ce5  ADD DI,AX
202c:1ce7  MOV byte ptr ES:[DI + 0x5],0x0
202c:1cec  MOV AL,byte ptr [BP + -0x23]
202c:1cef  XOR AH,AH
202c:1cf1  MOV DI,AX
202c:1cf3  MOV DL,byte ptr [DI + 0x13ad]
202c:1cf7  IMUL AX,word ptr [BP + -0x2],0x7
202c:1cfb  LES DI,[0x668c]
202c:1cff  ADD DI,AX
202c:1d01  MOV byte ptr ES:[DI + 0x6],DL
202c:1d05  MOV AL,byte ptr [BP + -0x23]
202c:1d08  XOR AH,AH
202c:1d0a  MOV DI,AX
202c:1d0c  CMP byte ptr [DI + 0x1443],0x0
202c:1d11  JBE 0x2000:1ff2
202c:1d13  MOV AL,byte ptr [BP + -0x23]
202c:1d16  XOR AH,AH
202c:1d18  MOV DI,AX
202c:1d1a  MOV AL,byte ptr [DI + 0x1443]
202c:1d1e  CMP AL,byte ptr [0x67c0]
202c:1d22  JBE 0x2000:1ff2
202c:1d24  MOV AL,byte ptr [BP + -0x23]
202c:1d27  XOR AH,AH
202c:1d29  MOV DI,AX
202c:1d2b  MOV AL,byte ptr [DI + 0x1443]
202c:1d2f  MOV [0x67c0],AL
202c:1d32  MOV AL,byte ptr [BP + -0x23]
202c:1d35  XOR AH,AH
202c:1d37  MOV DI,AX
202c:1d39  CMP byte ptr [DI + 0x13e5],0x0
202c:1d3e  JA 0x2000:2003
202c:1d40  JMP 0x2000:3162
202c:1d43  IMUL AX,word ptr [BP + -0x2],0x7
202c:1d47  LES DI,[0x668c]
202c:1d4b  ADD DI,AX
202c:1d4d  MOV word ptr [BP + -0x28],DI
202c:1d50  MOV word ptr [BP + -0x26],ES
202c:1d53  MOV AX,word ptr ES:[DI]
202c:1d56  ADD AX,0x8
202c:1d59  CWD
202c:1d5a  MOV word ptr [BP + -0x1a],AX
202c:1d5d  MOV word ptr [BP + -0x18],DX
202c:1d60  MOV AX,word ptr ES:[DI + 0x2]
202c:1d64  ADD AX,0x8
202c:1d67  CWD
202c:1d68  MOV word ptr [BP + -0x1e],AX
202c:1d6b  MOV word ptr [BP + -0x1c],DX
202c:1d6e  MOV AL,byte ptr [BP + -0x23]
202c:1d71  XOR AH,AH
202c:1d73  MOV DI,AX
202c:1d75  MOV AL,byte ptr [DI + 0x13d7]
202c:1d79  XOR AH,AH
202c:1d7b  XOR DX,DX
202c:1d7d  MOV word ptr [BP + -0xa],AX
202c:1d80  MOV word ptr [BP + -0x8],DX
202c:1d83  LES DI,[0x6670]
202c:1d87  CMP byte ptr ES:[DI + 0x9a],0x0
202c:1d8d  JNZ 0x2000:2052
202c:1d8f  JMP 0x2000:2421
202c:1d92  MOV AX,word ptr [BP + -0x1a]
202c:1d95  MOV DX,word ptr [BP + -0x18]
202c:1d98  ADD AX,word ptr [BP + -0xa]
202c:1d9b  ADC DX,word ptr [BP + -0x8]
202c:1d9e  MOV CX,AX
202c:1da0  MOV BX,DX
202c:1da2  LES DI,[0x6670]
202c:1da6  MOV AX,word ptr ES:[DI + 0x6]
202c:1daa  CWD
202c:1dab  CMP DX,BX
202c:1dad  JL 0x2000:207b
202c:1daf  JLE 0x2000:2074
202c:1db1  JMP 0x2000:2421
202c:1db4  CMP AX,CX
202c:1db6  JC 0x2000:207b
202c:1db8  JMP 0x2000:2421
202c:1dbb  MOV AX,word ptr [BP + -0x1a]
202c:1dbe  MOV DX,word ptr [BP + -0x18]
202c:1dc1  SUB AX,word ptr [BP + -0xa]
202c:1dc4  SBB DX,word ptr [BP + -0x8]
202c:1dc7  MOV CX,AX
202c:1dc9  MOV BX,DX
202c:1dcb  LES DI,[0x6670]
202c:1dcf  MOV AX,word ptr ES:[DI + 0x6]
202c:1dd3  CWD
202c:1dd4  CMP DX,BX
202c:1dd6  JG 0x2000:20a4
202c:1dd8  JGE 0x2000:209d
202c:1dda  JMP 0x2000:2421
202c:1ddd  CMP AX,CX
202c:1ddf  JA 0x2000:20a4
202c:1de1  JMP 0x2000:2421
202c:1de4  MOV AX,word ptr [BP + -0x1e]
202c:1de7  MOV DX,word ptr [BP + -0x1c]
202c:1dea  ADD AX,word ptr [BP + -0xa]
202c:1ded  ADC DX,word ptr [BP + -0x8]
202c:1df0  MOV CX,AX
202c:1df2  MOV BX,DX
202c:1df4  LES DI,[0x6670]
202c:1df8  MOV AX,word ptr ES:[DI + 0xa]
202c:1dfc  CWD
202c:1dfd  CMP DX,BX
202c:1dff  JL 0x2000:20cd
202c:1e01  JLE 0x2000:20c6
202c:1e03  JMP 0x2000:2421
202c:1e06  CMP AX,CX
202c:1e08  JC 0x2000:20cd
202c:1e0a  JMP 0x2000:2421
202c:1e0d  MOV AX,word ptr [BP + -0x1e]
202c:1e10  MOV DX,word ptr [BP + -0x1c]
202c:1e13  SUB AX,word ptr [BP + -0xa]
202c:1e16  SBB DX,word ptr [BP + -0x8]
202c:1e19  MOV CX,AX
202c:1e1b  MOV BX,DX
202c:1e1d  LES DI,[0x6670]
202c:1e21  MOV AX,word ptr ES:[DI + 0xa]
202c:1e25  CWD
202c:1e26  CMP DX,BX
202c:1e28  JG 0x2000:20f6
202c:1e2a  JGE 0x2000:20ef
202c:1e2c  JMP 0x2000:2421
202c:1e2f  CMP AX,CX
202c:1e31  JA 0x2000:20f6
202c:1e33  JMP 0x2000:2421
202c:1e36  LES DI,[0x6670]
202c:1e3a  MOV AX,word ptr ES:[DI + 0x6]
202c:1e3e  CWD
202c:1e3f  SUB AX,word ptr [BP + -0x1a]
202c:1e42  SBB DX,word ptr [BP + -0x18]
202c:1e45  MOV word ptr [BP + -0x12],AX
202c:1e48  MOV word ptr [BP + -0x10],DX
202c:1e4b  MOV AX,word ptr [BP + -0x12]
202c:1e4e  MOV DX,word ptr [BP + -0x10]
202c:1e51  OR DX,DX
202c:1e53  JNS 0x2000:211c
202c:1e55  NOT DX
202c:1e57  NEG AX
202c:1e59  SBB DX,-0x1
202c:1e5c  MOV CX,AX
202c:1e5e  MOV BX,DX
202c:1e60  MOV AX,word ptr [BP + -0xa]
202c:1e63  MOV DX,word ptr [BP + -0x8]
202c:1e66  SUB AX,CX
202c:1e68  SBB DX,BX
202c:1e6a  MOV word ptr [BP + -0xe],AX
202c:1e6d  MOV word ptr [BP + -0xc],DX
202c:1e70  MOV AX,word ptr [BP + -0xe]
202c:1e73  MOV DX,word ptr [BP + -0xc]
202c:1e76  MOV word ptr [BP + -0x16],AX
202c:1e79  MOV word ptr [BP + -0x14],DX
202c:1e7c  LES DI,[0x6670]
202c:1e80  MOV AX,word ptr ES:[DI + 0x30]
202c:1e84  MOV DX,word ptr ES:[DI + 0x32]
202c:1e88  OR DX,DX
202c:1e8a  JNS 0x2000:2153
202c:1e8c  NOT DX
202c:1e8e  NEG AX
202c:1e90  SBB DX,-0x1
202c:1e93  CMP DX,0x2
202c:1e96  JL 0x2000:215f
202c:1e98  JG 0x2000:21cd
202c:1e9a  CMP AX,0x0
202c:1e9d  JNC 0x2000:21cd
202c:1e9f  CMP word ptr [BP + -0x10],0x0
202c:1ea3  JG 0x2000:216d
202c:1ea5  JL 0x2000:2196
202c:1ea7  CMP word ptr [BP + -0x12],0x0
202c:1eab  JBE 0x2000:2196
202c:1ead  MOV AL,byte ptr [BP + -0x23]
202c:1eb0  XOR AH,AH
202c:1eb2  MOV DI,AX
202c:1eb4  SHL DI,0x2
202c:1eb7  MOV AX,word ptr [DI + 0x13f0]
202c:1ebb  MOV DX,word ptr [DI + 0x13f2]
202c:1ebf  MOV CX,word ptr [BP + -0xe]
202c:1ec2  MOV BX,word ptr [BP + -0xc]
202c:1ec5  CALLF 0x2000:8b50
202c:1eca  LES DI,[0x6670]
202c:1ece  ADD word ptr ES:[DI + 0x30],AX
202c:1ed2  ADC word ptr ES:[DI + 0x32],DX
202c:1ed6  CMP word ptr [BP + -0x10],0x0
202c:1eda  JL 0x2000:21a4
202c:1edc  JG 0x2000:21cd
202c:1ede  CMP word ptr [BP + -0x12],0x0
202c:1ee2  JNC 0x2000:21cd
202c:1ee4  MOV AL,byte ptr [BP + -0x23]
202c:1ee7  XOR AH,AH
202c:1ee9  MOV DI,AX
202c:1eeb  SHL DI,0x2
202c:1eee  MOV AX,word ptr [DI + 0x13f0]
202c:1ef2  MOV DX,word ptr [DI + 0x13f2]
202c:1ef6  MOV CX,word ptr [BP + -0xe]
202c:1ef9  MOV BX,word ptr [BP + -0xc]
202c:1efc  CALLF 0x2000:8b50
202c:1f01  LES DI,[0x6670]
202c:1f05  SUB word ptr ES:[DI + 0x30],AX
202c:1f09  SBB word ptr ES:[DI + 0x32],DX
202c:1f0d  LES DI,[0x6670]
202c:1f11  MOV AX,word ptr ES:[DI + 0xa]
202c:1f15  CWD
202c:1f16  SUB AX,word ptr [BP + -0x1e]
202c:1f19  SBB DX,word ptr [BP + -0x1c]
202c:1f1c  MOV word ptr [BP + -0x12],AX
202c:1f1f  MOV word ptr [BP + -0x10],DX
202c:1f22  MOV AX,word ptr [BP + -0x12]
202c:1f25  MOV DX,word ptr [BP + -0x10]
202c:1f28  OR DX,DX
202c:1f2a  JNS 0x2000:21f3
202c:1f2c  NOT DX
202c:1f2e  NEG AX
202c:1f30  SBB DX,-0x1
202c:1f33  MOV CX,AX
202c:1f35  MOV BX,DX
202c:1f37  MOV AX,word ptr [BP + -0xa]
202c:1f3a  MOV DX,word ptr [BP + -0x8]
202c:1f3d  SUB AX,CX
202c:1f3f  SBB DX,BX
202c:1f41  MOV word ptr [BP + -0xe],AX
202c:1f44  MOV word ptr [BP + -0xc],DX
202c:1f47  MOV AX,word ptr [BP + -0x16]
202c:1f4a  MOV DX,word ptr [BP + -0x14]
202c:1f4d  ADD AX,word ptr [BP + -0xe]
202c:1f50  ADC DX,word ptr [BP + -0xc]
202c:1f53  MOV word ptr [BP + -0x16],AX
202c:1f56  MOV word ptr [BP + -0x14],DX
202c:1f59  LES DI,[0x6670]
202c:1f5d  MOV AX,word ptr ES:[DI + 0x34]
202c:1f61  MOV DX,word ptr ES:[DI + 0x36]
202c:1f65  OR DX,DX
202c:1f67  JNS 0x2000:2230
202c:1f69  NOT DX
202c:1f6b  NEG AX
202c:1f6d  SBB DX,-0x1
202c:1f70  CMP DX,0x2
202c:1f73  JL 0x2000:223c
202c:1f75  JG 0x2000:22aa
202c:1f77  CMP AX,0x0
202c:1f7a  JNC 0x2000:22aa
202c:1f7c  CMP word ptr [BP + -0x10],0x0
202c:1f80  JG 0x2000:224a
202c:1f82  JL 0x2000:2273
202c:1f84  CMP word ptr [BP + -0x12],0x0
202c:1f88  JBE 0x2000:2273
202c:1f8a  MOV AL,byte ptr [BP + -0x23]
202c:1f8d  XOR AH,AH
202c:1f8f  MOV DI,AX
202c:1f91  SHL DI,0x2
202c:1f94  MOV AX,word ptr [DI + 0x13f0]
202c:1f98  MOV DX,word ptr [DI + 0x13f2]
202c:1f9c  MOV CX,word ptr [BP + -0xe]
202c:1f9f  MOV BX,word ptr [BP + -0xc]
202c:1fa2  CALLF 0x2000:8b50
202c:1fa7  LES DI,[0x6670]
202c:1fab  ADD word ptr ES:[DI + 0x34],AX
202c:1faf  ADC word ptr ES:[DI + 0x36],DX
202c:1fb3  CMP word ptr [BP + -0x10],0x0
202c:1fb7  JL 0x2000:2281
202c:1fb9  JG 0x2000:22aa
202c:1fbb  CMP word ptr [BP + -0x12],0x0
202c:1fbf  JNC 0x2000:22aa
202c:1fc1  MOV AL,byte ptr [BP + -0x23]
202c:1fc4  XOR AH,AH
202c:1fc6  MOV DI,AX
202c:1fc8  SHL DI,0x2
202c:1fcb  MOV AX,word ptr [DI + 0x13f0]
202c:1fcf  MOV DX,word ptr [DI + 0x13f2]
202c:1fd3  MOV CX,word ptr [BP + -0xe]
202c:1fd6  MOV BX,word ptr [BP + -0xc]
202c:1fd9  CALLF 0x2000:8b50
202c:1fde  LES DI,[0x6670]
202c:1fe2  SUB word ptr ES:[DI + 0x34],AX
202c:1fe6  SBB word ptr ES:[DI + 0x36],DX
202c:1fea  MOV AX,word ptr [BP + -0x16]
202c:1fed  MOV DX,word ptr [BP + -0x14]
202c:1ff0  MOV CX,0x1
202c:1ff3  XOR BX,BX
202c:1ff5  CALLF 0x2000:8c33
202c:1ffa  MOV word ptr [BP + -0x16],AX
202c:1ffd  MOV word ptr [BP + -0x14],DX
202c:2000  MOV AL,byte ptr [BP + -0x23]
202c:2003  XOR AH,AH
202c:2005  MOV DI,AX
202c:2007  MOV AL,byte ptr [DI + 0x13d7]
202c:200b  XOR AH,AH
202c:200d  XOR DX,DX
202c:200f  PUSH DX
202c:2010  PUSH AX
202c:2011  MOV AL,byte ptr [BP + -0x23]
202c:2014  XOR AH,AH
202c:2016  MOV DI,AX
202c:2018  MOV AL,byte ptr [DI + 0x13e5]
202c:201c  XOR AH,AH
202c:201e  XOR DX,DX
202c:2020  MOV CX,word ptr [BP + -0x16]
202c:2023  MOV BX,word ptr [BP + -0x14]
202c:2026  CALLF 0x2000:8b50
202c:202b  POP CX
202c:202c  POP BX
202c:202d  CALLF 0x2000:8b8d
202c:2032  MOV word ptr [BP + -0xe],AX
202c:2035  MOV word ptr [BP + -0xc],DX
202c:2038  LES DI,[0x6670]
202c:203c  CMP word ptr ES:[DI + 0x50],0x0
202c:2041  JG 0x2000:2306
202c:2043  JMP 0x2000:2421
202c:2046  MOV AX,word ptr [BP + -0xe]
202c:2049  LES DI,[0x6670]
202c:204d  SUB word ptr ES:[DI + 0x50],AX
202c:2051  LES DI,[0x6670]
202c:2055  CMP word ptr ES:[DI + 0x50],0x0
202c:205a  JG 0x2000:233f
202c:205c  LES DI,[BP + -0x28]
202c:205f  MOV AL,byte ptr ES:[DI + 0x4]
202c:2063  AND AL,0x80
202c:2065  CMP AL,0x80
202c:2067  JNZ 0x2000:2335
202c:2069  LES DI,[0x6670]
202c:206d  MOV byte ptr ES:[DI + 0x96],0x0
202c:2073  JMP 0x2000:233f
202c:2075  LES DI,[0x6670]
202c:2079  MOV byte ptr ES:[DI + 0x96],0x1
202c:207f  MOV AX,[0x66aa]
202c:2082  CWD
202c:2083  MOV CX,word ptr [BP + -0x16]
202c:2086  MOV BX,word ptr [BP + -0x14]
202c:2089  CALLF 0x2000:8b50
202c:208e  MOV CX,0x64
202c:2091  XOR BX,BX
202c:2093  CALLF 0x2000:8b8d
202c:2098  MOV word ptr [BP + -0x2c],AX
202c:209b  MOV word ptr [BP + -0x2a],DX
202c:209e  MOV AX,0x1
202c:20a1  XOR DX,DX
202c:20a3  CMP DX,word ptr [BP + -0x2a]
202c:20a6  JG 0x2000:23e0
202c:20a8  JL 0x2000:236f
202c:20aa  CMP AX,word ptr [BP + -0x2c]
202c:20ad  JA 0x2000:23e0
202c:20af  MOV word ptr [BP + -0xe],AX
202c:20b2  MOV word ptr [BP + -0xc],DX
202c:20b5  JMP 0x2000:237f
202c:20b7  ADD word ptr [BP + -0xe],0x1
202c:20bb  ADC word ptr [BP + -0xc],0x0
202c:20bf  PUSH 0x7
202c:20c1  PUSH 0x0
202c:20c3  LES DI,[0x6670]
202c:20c7  PUSH word ptr ES:[DI + 0x6]
202c:20cb  LES DI,[0x6670]
202c:20cf  PUSH word ptr ES:[DI + 0xa]
202c:20d3  LES DI,[0x6670]
202c:20d7  MOV AX,word ptr ES:[DI + 0x30]
202c:20db  MOV DX,word ptr ES:[DI + 0x32]
202c:20df  MOV CX,0x3
202c:20e2  XOR BX,BX
202c:20e4  CALLF 0x2000:8b8d
202c:20e9  PUSH DX
202c:20ea  PUSH AX
202c:20eb  LES DI,[0x6670]
202c:20ef  MOV AX,word ptr ES:[DI + 0x34]
202c:20f3  MOV DX,word ptr ES:[DI + 0x36]
202c:20f7  MOV CX,0x3
202c:20fa  XOR BX,BX
202c:20fc  CALLF 0x2000:8b8d
202c:2101  PUSH DX
202c:2102  PUSH AX
202c:2103  PUSH 0x80
202c:2106  CALLF 0x2000:9424
202c:210b  PUSH AX
202c:210c  PUSH CS
202c:210d  CALL 0x2000:191d
202c:2110  MOV AX,word ptr [BP + -0xe]
202c:2113  MOV DX,word ptr [BP + -0xc]
202c:2116  CMP DX,word ptr [BP + -0x2a]
202c:2119  JNZ 0x2000:2377
202c:211b  CMP AX,word ptr [BP + -0x2c]
202c:211e  JNZ 0x2000:2377
202c:2120  CMP byte ptr [0x4b8],0x0
202c:2125  JZ 0x2000:2421
202c:2127  PUSH 0x3
202c:2129  CALLF 0x2000:9424
202c:212e  OR AX,AX
202c:2130  JNZ 0x2000:2421
202c:2132  MOV AL,[0x4b6]
202c:2135  PUSH AX
202c:2136  CALLF 0x2000:3fde
202c:213b  OR AL,AL
202c:213d  JNZ 0x2000:2421
202c:213f  PUSH 0x3
202c:2141  CALLF 0x2000:9424
202c:2146  ADD AX,0x13
202c:2149  MOV DI,AX
202c:214b  SHL DI,0x2
202c:214e  PUSH word ptr [DI + 0x6736]
202c:2152  PUSH word ptr [DI + 0x6734]
202c:2156  MOV AL,[0x4b6]
202c:2159  PUSH AX
202c:215a  PUSH 0x0
202c:215c  CALLF 0x2000:3f1c
202c:2161  LES DI,[0x6670]
202c:2165  CMP byte ptr ES:[DI + 0x144],0x0
202c:216b  JNZ 0x2000:2430
202c:216d  JMP 0x2000:281d
202c:2170  MOV AX,word ptr [BP + -0x1a]
202c:2173  MOV DX,word ptr [BP + -0x18]
202c:2176  ADD AX,word ptr [BP + -0xa]
202c:2179  ADC DX,word ptr [BP + -0x8]
202c:217c  MOV CX,AX
202c:217e  MOV BX,DX
202c:2180  LES DI,[0x6670]
202c:2184  MOV AX,word ptr ES:[DI + 0xb0]
202c:2189  CWD
202c:218a  CMP DX,BX
202c:218c  JL 0x2000:245a
202c:218e  JLE 0x2000:2453
202c:2190  JMP 0x2000:281d
202c:2193  CMP AX,CX
202c:2195  JC 0x2000:245a
202c:2197  JMP 0x2000:281d
202c:219a  MOV AX,word ptr [BP + -0x1a]
202c:219d  MOV DX,word ptr [BP + -0x18]
202c:21a0  SUB AX,word ptr [BP + -0xa]
202c:21a3  SBB DX,word ptr [BP + -0x8]
202c:21a6  MOV CX,AX
202c:21a8  MOV BX,DX
202c:21aa  LES DI,[0x6670]
202c:21ae  MOV AX,word ptr ES:[DI + 0xb0]
202c:21b3  CWD
202c:21b4  CMP DX,BX
202c:21b6  JG 0x2000:2484
202c:21b8  JGE 0x2000:247d
202c:21ba  JMP 0x2000:281d
202c:21bd  CMP AX,CX
202c:21bf  JA 0x2000:2484
202c:21c1  JMP 0x2000:281d
202c:21c4  MOV AX,word ptr [BP + -0x1e]
202c:21c7  MOV DX,word ptr [BP + -0x1c]
202c:21ca  ADD AX,word ptr [BP + -0xa]
202c:21cd  ADC DX,word ptr [BP + -0x8]
202c:21d0  MOV CX,AX
202c:21d2  MOV BX,DX
202c:21d4  LES DI,[0x6670]
202c:21d8  MOV AX,word ptr ES:[DI + 0xb4]
202c:21dd  CWD
202c:21de  CMP DX,BX
202c:21e0  JL 0x2000:24ae
202c:21e2  JLE 0x2000:24a7
202c:21e4  JMP 0x2000:281d
202c:21e7  CMP AX,CX
202c:21e9  JC 0x2000:24ae
202c:21eb  JMP 0x2000:281d
202c:21ee  MOV AX,word ptr [BP + -0x1e]
202c:21f1  MOV DX,word ptr [BP + -0x1c]
202c:21f4  SUB AX,word ptr [BP + -0xa]
202c:21f7  SBB DX,word ptr [BP + -0x8]
202c:21fa  MOV CX,AX
202c:21fc  MOV BX,DX
202c:21fe  LES DI,[0x6670]
202c:2202  MOV AX,word ptr ES:[DI + 0xb4]
202c:2207  CWD
202c:2208  CMP DX,BX
202c:220a  JG 0x2000:24d8
202c:220c  JGE 0x2000:24d1
202c:220e  JMP 0x2000:281d
202c:2211  CMP AX,CX
202c:2213  JA 0x2000:24d8
202c:2215  JMP 0x2000:281d
202c:2218  LES DI,[0x6670]
202c:221c  MOV AX,word ptr ES:[DI + 0xb0]
202c:2221  CWD
202c:2222  SUB AX,word ptr [BP + -0x1a]
202c:2225  SBB DX,word ptr [BP + -0x18]
202c:2228  MOV word ptr [BP + -0x12],AX
202c:222b  MOV word ptr [BP + -0x10],DX
202c:222e  MOV AX,word ptr [BP + -0x12]
202c:2231  MOV DX,word ptr [BP + -0x10]
202c:2234  OR DX,DX
202c:2236  JNS 0x2000:24ff
202c:2238  NOT DX
202c:223a  NEG AX
202c:223c  SBB DX,-0x1
202c:223f  MOV CX,AX
202c:2241  MOV BX,DX
202c:2243  MOV AX,word ptr [BP + -0xa]
202c:2246  MOV DX,word ptr [BP + -0x8]
202c:2249  SUB AX,CX
202c:224b  SBB DX,BX
202c:224d  MOV word ptr [BP + -0xe],AX
202c:2250  MOV word ptr [BP + -0xc],DX
202c:2253  MOV AX,word ptr [BP + -0xe]
202c:2256  MOV DX,word ptr [BP + -0xc]
202c:2259  MOV word ptr [BP + -0x16],AX
202c:225c  MOV word ptr [BP + -0x14],DX
202c:225f  LES DI,[0x6670]
202c:2263  MOV AX,word ptr ES:[DI + 0xda]
202c:2268  MOV DX,word ptr ES:[DI + 0xdc]
202c:226d  OR DX,DX
202c:226f  JNS 0x2000:2538
202c:2271  NOT DX
202c:2273  NEG AX
202c:2275  SBB DX,-0x1
202c:2278  CMP DX,0x2
202c:227b  JL 0x2000:2544
202c:227d  JG 0x2000:25b6
202c:227f  CMP AX,0x0
202c:2282  JNC 0x2000:25b6
202c:2284  CMP word ptr [BP + -0x10],0x0
202c:2288  JG 0x2000:2552
202c:228a  JL 0x2000:257d
202c:228c  CMP word ptr [BP + -0x12],0x0
202c:2290  JBE 0x2000:257d
202c:2292  MOV AL,byte ptr [BP + -0x23]
202c:2295  XOR AH,AH
202c:2297  MOV DI,AX
202c:2299  SHL DI,0x2
202c:229c  MOV AX,word ptr [DI + 0x13f0]
202c:22a0  MOV DX,word ptr [DI + 0x13f2]
202c:22a4  MOV CX,word ptr [BP + -0xe]
202c:22a7  MOV BX,word ptr [BP + -0xc]
202c:22aa  CALLF 0x2000:8b50
202c:22af  LES DI,[0x6670]
202c:22b3  ADD word ptr ES:[DI + 0xda],AX
202c:22b8  ADC word ptr ES:[DI + 0xdc],DX
202c:22bd  CMP word ptr [BP + -0x10],0x0
202c:22c1  JL 0x2000:258b
202c:22c3  JG 0x2000:25b6
202c:22c5  CMP word ptr [BP + -0x12],0x0
202c:22c9  JNC 0x2000:25b6
202c:22cb  MOV AL,byte ptr [BP + -0x23]
202c:22ce  XOR AH,AH
202c:22d0  MOV DI,AX
202c:22d2  SHL DI,0x2
202c:22d5  MOV AX,word ptr [DI + 0x13f0]
202c:22d9  MOV DX,word ptr [DI + 0x13f2]
202c:22dd  MOV CX,word ptr [BP + -0xe]
202c:22e0  MOV BX,word ptr [BP + -0xc]
202c:22e3  CALLF 0x2000:8b50
202c:22e8  LES DI,[0x6670]
202c:22ec  SUB word ptr ES:[DI + 0xda],AX
202c:22f1  SBB word ptr ES:[DI + 0xdc],DX
202c:22f6  LES DI,[0x6670]
202c:22fa  MOV AX,word ptr ES:[DI + 0xb4]
202c:22ff  CWD
202c:2300  SUB AX,word ptr [BP + -0x1e]
202c:2303  SBB DX,word ptr [BP + -0x1c]
202c:2306  MOV word ptr [BP + -0x12],AX
202c:2309  MOV word ptr [BP + -0x10],DX
202c:230c  MOV AX,word ptr [BP + -0x12]
202c:230f  MOV DX,word ptr [BP + -0x10]
202c:2312  OR DX,DX
202c:2314  JNS 0x2000:25dd
202c:2316  NOT DX
202c:2318  NEG AX
202c:231a  SBB DX,-0x1
202c:231d  MOV CX,AX
202c:231f  MOV BX,DX
202c:2321  MOV AX,word ptr [BP + -0xa]
202c:2324  MOV DX,word ptr [BP + -0x8]
202c:2327  SUB AX,CX
202c:2329  SBB DX,BX
202c:232b  MOV word ptr [BP + -0xe],AX
202c:232e  MOV word ptr [BP + -0xc],DX
202c:2331  MOV AX,word ptr [BP + -0x16]
202c:2334  MOV DX,word ptr [BP + -0x14]
202c:2337  ADD AX,word ptr [BP + -0xe]
202c:233a  ADC DX,word ptr [BP + -0xc]
202c:233d  MOV word ptr [BP + -0x16],AX
202c:2340  MOV word ptr [BP + -0x14],DX
202c:2343  LES DI,[0x6670]
202c:2347  MOV AX,word ptr ES:[DI + 0xde]
202c:234c  MOV DX,word ptr ES:[DI + 0xe0]
202c:2351  OR DX,DX
202c:2353  JNS 0x2000:261c
202c:2355  NOT DX
202c:2357  NEG AX
202c:2359  SBB DX,-0x1
202c:235c  CMP DX,0x2
202c:235f  JL 0x2000:2628
202c:2361  JG 0x2000:269a
202c:2363  CMP AX,0x0
202c:2366  JNC 0x2000:269a
202c:2368  CMP word ptr [BP + -0x10],0x0
202c:236c  JG 0x2000:2636
202c:236e  JL 0x2000:2661
202c:2370  CMP word ptr [BP + -0x12],0x0
202c:2374  JBE 0x2000:2661
202c:2376  MOV AL,byte ptr [BP + -0x23]
202c:2379  XOR AH,AH
202c:237b  MOV DI,AX
202c:237d  SHL DI,0x2
202c:2380  MOV AX,word ptr [DI + 0x13f0]
202c:2384  MOV DX,word ptr [DI + 0x13f2]
202c:2388  MOV CX,word ptr [BP + -0xe]
202c:238b  MOV BX,word ptr [BP + -0xc]
202c:238e  CALLF 0x2000:8b50
202c:2393  LES DI,[0x6670]
202c:2397  ADD word ptr ES:[DI + 0xde],AX
202c:239c  ADC word ptr ES:[DI + 0xe0],DX
202c:23a1  CMP word ptr [BP + -0x10],0x0
202c:23a5  JL 0x2000:266f
202c:23a7  JG 0x2000:269a
202c:23a9  CMP word ptr [BP + -0x12],0x0
202c:23ad  JNC 0x2000:269a
202c:23af  MOV AL,byte ptr [BP + -0x23]
202c:23b2  XOR AH,AH
202c:23b4  MOV DI,AX
202c:23b6  SHL DI,0x2
202c:23b9  MOV AX,word ptr [DI + 0x13f0]
202c:23bd  MOV DX,word ptr [DI + 0x13f2]
202c:23c1  MOV CX,word ptr [BP + -0xe]
202c:23c4  MOV BX,word ptr [BP + -0xc]
202c:23c7  CALLF 0x2000:8b50
202c:23cc  LES DI,[0x6670]
202c:23d0  SUB word ptr ES:[DI + 0xde],AX
202c:23d5  SBB word ptr ES:[DI + 0xe0],DX
202c:23da  MOV AX,word ptr [BP + -0x16]
202c:23dd  MOV DX,word ptr [BP + -0x14]
202c:23e0  MOV CX,0x1
202c:23e3  XOR BX,BX
202c:23e5  CALLF 0x2000:8c33
202c:23ea  MOV word ptr [BP + -0x16],AX
202c:23ed  MOV word ptr [BP + -0x14],DX
202c:23f0  MOV AL,byte ptr [BP + -0x23]
202c:23f3  XOR AH,AH
202c:23f5  MOV DI,AX
202c:23f7  MOV AL,byte ptr [DI + 0x13d7]
202c:23fb  XOR AH,AH
202c:23fd  XOR DX,DX
202c:23ff  PUSH DX
202c:2400  PUSH AX
202c:2401  MOV AL,byte ptr [BP + -0x23]
202c:2404  XOR AH,AH
202c:2406  MOV DI,AX
202c:2408  MOV AL,byte ptr [DI + 0x13e5]
202c:240c  XOR AH,AH
202c:240e  XOR DX,DX
202c:2410  MOV CX,word ptr [BP + -0x16]
202c:2413  MOV BX,word ptr [BP + -0x14]
202c:2416  CALLF 0x2000:8b50
202c:241b  POP CX
202c:241c  POP BX
202c:241d  CALLF 0x2000:8b8d
202c:2422  MOV word ptr [BP + -0xe],AX
202c:2425  MOV word ptr [BP + -0xc],DX
202c:2428  LES DI,[0x6670]
202c:242c  CMP word ptr ES:[DI + 0xfa],0x0
202c:2432  JG 0x2000:26f7
202c:2434  JMP 0x2000:281d
202c:2437  MOV AX,word ptr [BP + -0xe]
202c:243a  LES DI,[0x6670]
202c:243e  SUB word ptr ES:[DI + 0xfa],AX
202c:2443  LES DI,[0x6670]
202c:2447  CMP word ptr ES:[DI + 0xfa],0x0
202c:244d  JG 0x2000:2732
202c:244f  LES DI,[BP + -0x28]
202c:2452  MOV AL,byte ptr ES:[DI + 0x4]
202c:2456  AND AL,0x80
202c:2458  CMP AL,0x80
202c:245a  JNZ 0x2000:2728
202c:245c  LES DI,[0x6670]
202c:2460  MOV byte ptr ES:[DI + 0x140],0x1
202c:2466  JMP 0x2000:2732
202c:2468  LES DI,[0x6670]
202c:246c  MOV byte ptr ES:[DI + 0x140],0x0
202c:2472  MOV AX,[0x66aa]
202c:2475  CWD
202c:2476  MOV CX,word ptr [BP + -0x16]
202c:2479  MOV BX,word ptr [BP + -0x14]
202c:247c  CALLF 0x2000:8b50
202c:2481  MOV CX,0x64
202c:2484  XOR BX,BX
202c:2486  CALLF 0x2000:8b8d
202c:248b  MOV word ptr [BP + -0x2c],AX
202c:248e  MOV word ptr [BP + -0x2a],DX
202c:2491  MOV AX,0x1
202c:2494  XOR DX,DX
202c:2496  CMP DX,word ptr [BP + -0x2a]
202c:2499  JLE 0x2000:275e
202c:249b  JMP 0x2000:27dc
202c:249e  JL 0x2000:2765
202c:24a0  CMP AX,word ptr [BP + -0x2c]
202c:24a3  JA 0x2000:27dc
202c:24a5  MOV word ptr [BP + -0xe],AX
202c:24a8  MOV word ptr [BP + -0xc],DX
202c:24ab  JMP 0x2000:2775
202c:24ad  ADD word ptr [BP + -0xe],0x1
202c:24b1  ADC word ptr [BP + -0xc],0x0
202c:24b5  PUSH 0x7
202c:24b7  PUSH 0x0
202c:24b9  LES DI,[0x6670]
202c:24bd  PUSH word ptr ES:[DI + 0xb0]
202c:24c2  LES DI,[0x6670]
202c:24c6  PUSH word ptr ES:[DI + 0xb4]
202c:24cb  LES DI,[0x6670]
202c:24cf  MOV AX,word ptr ES:[DI + 0xda]
202c:24d4  MOV DX,word ptr ES:[DI + 0xdc]
202c:24d9  MOV CX,0x3
202c:24dc  XOR BX,BX
202c:24de  CALLF 0x2000:8b8d
202c:24e3  PUSH DX
202c:24e4  PUSH AX
202c:24e5  LES DI,[0x6670]
202c:24e9  MOV AX,word ptr ES:[DI + 0xde]
202c:24ee  MOV DX,word ptr ES:[DI + 0xe0]
202c:24f3  MOV CX,0x3
202c:24f6  XOR BX,BX
202c:24f8  CALLF 0x2000:8b8d
202c:24fd  PUSH DX
202c:24fe  PUSH AX
202c:24ff  PUSH 0x80
202c:2502  CALLF 0x2000:9424
202c:2507  PUSH AX
202c:2508  PUSH CS
202c:2509  CALL 0x2000:191d
202c:250c  MOV AX,word ptr [BP + -0xe]
202c:250f  MOV DX,word ptr [BP + -0xc]
202c:2512  CMP DX,word ptr [BP + -0x2a]
202c:2515  JNZ 0x2000:276d
202c:2517  CMP AX,word ptr [BP + -0x2c]
202c:251a  JNZ 0x2000:276d
202c:251c  CMP byte ptr [0x4b8],0x0
202c:2521  JZ 0x2000:281d
202c:2523  PUSH 0x3
202c:2525  CALLF 0x2000:9424
202c:252a  OR AX,AX
202c:252c  JNZ 0x2000:281d
202c:252e  MOV AL,[0x4b7]
202c:2531  PUSH AX
202c:2532  CALLF 0x2000:3fde
202c:2537  OR AL,AL
202c:2539  JNZ 0x2000:281d
202c:253b  PUSH 0x3
202c:253d  CALLF 0x2000:9424
202c:2542  ADD AX,0x13
202c:2545  MOV DI,AX
202c:2547  SHL DI,0x2
202c:254a  PUSH word ptr [DI + 0x6736]
202c:254e  PUSH word ptr [DI + 0x6734]
202c:2552  MOV AL,[0x4b7]
202c:2555  PUSH AX
202c:2556  PUSH 0x0
202c:2558  CALLF 0x2000:3f1c
202c:255d  MOV AL,byte ptr [BP + -0x23]
202c:2560  XOR AH,AH
202c:2562  MOV DI,AX
202c:2564  SHL DI,0x2
202c:2567  MOV AX,word ptr [DI + 0x13f0]
202c:256b  MOV DX,word ptr [DI + 0x13f2]
202c:256f  MOV CX,0x3
202c:2572  XOR BX,BX
202c:2574  CALLF 0x2000:8b8d
202c:2579  MOV word ptr [BP + -0x22],AX
202c:257c  MOV word ptr [BP + -0x20],DX
202c:257f  XOR AX,AX
202c:2581  MOV word ptr [BP + -0x16],AX
202c:2584  MOV word ptr [BP + -0x14],AX
202c:2587  JMP 0x2000:2851
202c:2589  ADD word ptr [BP + -0x16],0x1
202c:258d  ADC word ptr [BP + -0x14],0x0
202c:2591  IMUL AX,word ptr [BP + -0x16],0x14
202c:2595  LES DI,[0x6688]
202c:2599  ADD DI,AX
202c:259b  CMP byte ptr ES:[DI + 0x10],0x0
202c:25a0  JA 0x2000:2865
202c:25a2  JMP 0x2000:2ecc
202c:25a5  IMUL AX,word ptr [BP + -0x16],0x14
202c:25a9  LES DI,[0x6688]
202c:25ad  ADD DI,AX
202c:25af  MOV AL,byte ptr ES:[DI + 0x10]
202c:25b3  AND AL,0x7f
202c:25b5  XOR AH,AH
202c:25b7  MOV DI,AX
202c:25b9  CMP byte ptr [DI + 0xfc5],0x1
202c:25be  JZ 0x2000:2883
202c:25c0  JMP 0x2000:2ecc
202c:25c3  MOV AX,word ptr [BP + -0x1a]
202c:25c6  MOV DX,word ptr [BP + -0x18]
202c:25c9  ADD AX,word ptr [BP + -0xa]
202c:25cc  ADC DX,word ptr [BP + -0x8]
202c:25cf  MOV CX,AX
202c:25d1  MOV BX,DX
202c:25d3  IMUL AX,word ptr [BP + -0x16],0x14
202c:25d7  LES DI,[0x6688]
202c:25db  ADD DI,AX
202c:25dd  MOV AX,word ptr ES:[DI + 0x2]
202c:25e1  CWD
202c:25e2  CMP DX,BX
202c:25e4  JL 0x2000:28b2
202c:25e6  JLE 0x2000:28ab
202c:25e8  JMP 0x2000:2ecc
202c:25eb  CMP AX,CX
202c:25ed  JC 0x2000:28b2
202c:25ef  JMP 0x2000:2ecc
202c:25f2  MOV AX,word ptr [BP + -0x1a]
202c:25f5  MOV DX,word ptr [BP + -0x18]
202c:25f8  SUB AX,word ptr [BP + -0xa]
202c:25fb  SBB DX,word ptr [BP + -0x8]
202c:25fe  MOV CX,AX
202c:2600  MOV BX,DX
202c:2602  IMUL AX,word ptr [BP + -0x16],0x14
202c:2606  LES DI,[0x6688]
202c:260a  ADD DI,AX
202c:260c  MOV AX,word ptr ES:[DI + 0x2]
202c:2610  CWD
202c:2611  CMP DX,BX
202c:2613  JG 0x2000:28e1
202c:2615  JGE 0x2000:28da
202c:2617  JMP 0x2000:2ecc
202c:261a  CMP AX,CX
202c:261c  JA 0x2000:28e1
202c:261e  JMP 0x2000:2ecc
202c:2621  MOV AX,word ptr [BP + -0x1e]
202c:2624  MOV DX,word ptr [BP + -0x1c]
202c:2627  ADD AX,word ptr [BP + -0xa]
202c:262a  ADC DX,word ptr [BP + -0x8]
202c:262d  MOV CX,AX
202c:262f  MOV BX,DX
202c:2631  IMUL AX,word ptr [BP + -0x16],0x14
202c:2635  LES DI,[0x6688]
202c:2639  ADD DI,AX
202c:263b  MOV AX,word ptr ES:[DI + 0x6]
202c:263f  CWD
202c:2640  CMP DX,BX
202c:2642  JL 0x2000:2910
202c:2644  JLE 0x2000:2909
202c:2646  JMP 0x2000:2ecc
202c:2649  CMP AX,CX
202c:264b  JC 0x2000:2910
202c:264d  JMP 0x2000:2ecc
202c:2650  MOV AX,word ptr [BP + -0x1e]
202c:2653  MOV DX,word ptr [BP + -0x1c]
202c:2656  SUB AX,word ptr [BP + -0xa]
202c:2659  SBB DX,word ptr [BP + -0x8]
202c:265c  MOV CX,AX
202c:265e  MOV BX,DX
202c:2660  IMUL AX,word ptr [BP + -0x16],0x14
202c:2664  LES DI,[0x6688]
202c:2668  ADD DI,AX
202c:266a  MOV AX,word ptr ES:[DI + 0x6]
202c:266e  CWD
202c:266f  CMP DX,BX
202c:2671  JG 0x2000:293f
202c:2673  JGE 0x2000:2938
202c:2675  JMP 0x2000:2ecc
202c:2678  CMP AX,CX
202c:267a  JA 0x2000:293f
202c:267c  JMP 0x2000:2ecc
202c:267f  IMUL AX,word ptr [BP + -0x16],0x14
202c:2683  LES DI,[0x6688]
202c:2687  ADD DI,AX
202c:2689  MOV AX,word ptr ES:[DI + 0x2]
202c:268d  CWD
202c:268e  SUB AX,word ptr [BP + -0x1a]
202c:2691  SBB DX,word ptr [BP + -0x18]
202c:2694  MOV word ptr [BP + -0x12],AX
202c:2697  MOV word ptr [BP + -0x10],DX
202c:269a  MOV AX,word ptr [BP + -0x12]
202c:269d  MOV DX,word ptr [BP + -0x10]
202c:26a0  OR DX,DX
202c:26a2  JNS 0x2000:296b
202c:26a4  NOT DX
202c:26a6  NEG AX
202c:26a8  SBB DX,-0x1
202c:26ab  MOV CX,AX
202c:26ad  MOV BX,DX
202c:26af  MOV AX,word ptr [BP + -0xa]
202c:26b2  MOV DX,word ptr [BP + -0x8]
202c:26b5  SUB AX,CX
202c:26b7  SBB DX,BX
202c:26b9  MOV word ptr [BP + -0xe],AX
202c:26bc  MOV word ptr [BP + -0xc],DX
202c:26bf  CMP word ptr [BP + -0xc],0x0
202c:26c3  JG 0x2000:298d
202c:26c5  JL 0x2000:29f7
202c:26c7  CMP word ptr [BP + -0xe],0x0
202c:26cb  JBE 0x2000:29f7
202c:26cd  CMP word ptr [BP + -0x10],0x0
202c:26d1  JG 0x2000:299b
202c:26d3  JL 0x2000:29c2
202c:26d5  CMP word ptr [BP + -0x12],0x0
202c:26d9  JBE 0x2000:29c2
202c:26db  MOV AX,word ptr [BP + -0xe]
202c:26de  MOV DX,word ptr [BP + -0xc]
202c:26e1  MOV CX,word ptr [BP + -0x22]
202c:26e4  MOV BX,word ptr [BP + -0x20]
202c:26e7  CALLF 0x2000:8b50
202c:26ec  MOV CX,AX
202c:26ee  MOV BX,DX
202c:26f0  IMUL AX,word ptr [BP + -0x16],0x14
202c:26f4  LES DI,[0x6688]
202c:26f8  ADD DI,AX
202c:26fa  ADD word ptr ES:[DI + 0x8],CX
202c:26fe  ADC word ptr ES:[DI + 0xa],BX
202c:2702  CMP word ptr [BP + -0x10],0x0
202c:2706  JL 0x2000:29d0
202c:2708  JG 0x2000:29f7
202c:270a  CMP word ptr [BP + -0x12],0x0
202c:270e  JNC 0x2000:29f7
202c:2710  MOV AX,word ptr [BP + -0xe]
202c:2713  MOV DX,word ptr [BP + -0xc]
202c:2716  MOV CX,word ptr [BP + -0x22]
202c:2719  MOV BX,word ptr [BP + -0x20]
202c:271c  CALLF 0x2000:8b50
202c:2721  MOV CX,AX
202c:2723  MOV BX,DX
202c:2725  IMUL AX,word ptr [BP + -0x16],0x14
202c:2729  LES DI,[0x6688]
202c:272d  ADD DI,AX
202c:272f  SUB word ptr ES:[DI + 0x8],CX
202c:2733  SBB word ptr ES:[DI + 0xa],BX
202c:2737  IMUL AX,word ptr [BP + -0x16],0x14
202c:273b  LES DI,[0x6688]
202c:273f  ADD DI,AX
202c:2741  MOV AX,word ptr ES:[DI + 0x6]
202c:2745  CWD
202c:2746  SUB AX,word ptr [BP + -0x1e]
202c:2749  SBB DX,word ptr [BP + -0x1c]
202c:274c  MOV word ptr [BP + -0x12],AX
202c:274f  MOV word ptr [BP + -0x10],DX
202c:2752  MOV AX,word ptr [BP + -0x12]
202c:2755  MOV DX,word ptr [BP + -0x10]
202c:2758  OR DX,DX
202c:275a  JNS 0x2000:2a23
202c:275c  NOT DX
202c:275e  NEG AX
202c:2760  SBB DX,-0x1
202c:2763  MOV CX,AX
202c:2765  MOV BX,DX
202c:2767  MOV AX,word ptr [BP + -0xa]
202c:276a  MOV DX,word ptr [BP + -0x8]
202c:276d  SUB AX,CX
202c:276f  SBB DX,BX
202c:2771  MOV word ptr [BP + -0xe],AX
202c:2774  MOV word ptr [BP + -0xc],DX
202c:2777  CMP word ptr [BP + -0xc],0x0
202c:277b  JG 0x2000:2a45
202c:277d  JL 0x2000:2aaf
202c:277f  CMP word ptr [BP + -0xe],0x0
202c:2783  JBE 0x2000:2aaf
202c:2785  CMP word ptr [BP + -0x10],0x0
202c:2789  JG 0x2000:2a53
202c:278b  JL 0x2000:2a7a
202c:278d  CMP word ptr [BP + -0x12],0x0
202c:2791  JBE 0x2000:2a7a
202c:2793  MOV AX,word ptr [BP + -0xe]
202c:2796  MOV DX,word ptr [BP + -0xc]
202c:2799  MOV CX,word ptr [BP + -0x22]
202c:279c  MOV BX,word ptr [BP + -0x20]
202c:279f  CALLF 0x2000:8b50
202c:27a4  MOV CX,AX
202c:27a6  MOV BX,DX
202c:27a8  IMUL AX,word ptr [BP + -0x16],0x14
202c:27ac  LES DI,[0x6688]
202c:27b0  ADD DI,AX
202c:27b2  ADD word ptr ES:[DI + 0xc],CX
202c:27b6  ADC word ptr ES:[DI + 0xe],BX
202c:27ba  CMP word ptr [BP + -0x10],0x0
202c:27be  JL 0x2000:2a88
202c:27c0  JG 0x2000:2aaf
202c:27c2  CMP word ptr [BP + -0x12],0x0
202c:27c6  JNC 0x2000:2aaf
202c:27c8  MOV AX,word ptr [BP + -0xe]
202c:27cb  MOV DX,word ptr [BP + -0xc]
202c:27ce  MOV CX,word ptr [BP + -0x22]
202c:27d1  MOV BX,word ptr [BP + -0x20]
202c:27d4  CALLF 0x2000:8b50
202c:27d9  MOV CX,AX
202c:27db  MOV BX,DX
202c:27dd  IMUL AX,word ptr [BP + -0x16],0x14
202c:27e1  LES DI,[0x6688]
202c:27e5  ADD DI,AX
202c:27e7  SUB word ptr ES:[DI + 0xc],CX
202c:27eb  SBB word ptr ES:[DI + 0xe],BX
202c:27ef  IMUL AX,word ptr [BP + -0x16],0x14
202c:27f3  LES DI,[0x6688]
202c:27f7  ADD DI,AX
202c:27f9  MOV AL,byte ptr ES:[DI + 0x10]
202c:27fd  AND AL,0x7f
202c:27ff  CMP AL,0x23
202c:2801  JZ 0x2000:2ac6
202c:2803  JMP 0x2000:2ecc
202c:2806  IMUL AX,word ptr [BP + -0x16],0x14
202c:280a  LES DI,[0x6688]
202c:280e  ADD DI,AX
202c:2810  MOV word ptr [BP + -0x2c],DI
202c:2813  MOV word ptr [BP + -0x2a],ES
202c:2816  MOV AL,byte ptr ES:[DI + 0x10]
202c:281a  AND AL,0x7f
202c:281c  XOR AH,AH
202c:281e  XOR DX,DX
202c:2820  MOV word ptr [BP + -0xe],AX
202c:2823  MOV word ptr [BP + -0xc],DX
202c:2826  MOV byte ptr ES:[DI + 0x10],0x0
202c:282b  MOV DI,word ptr [BP + -0xe]
202c:282e  CMP byte ptr [DI + 0xe35],0x0
202c:2833  JBE 0x2000:2b15
202c:2835  LES DI,[BP + -0x2c]
202c:2838  MOV AL,byte ptr ES:[DI + 0x10]
202c:283c  AND AL,0x80
202c:283e  MOV DI,word ptr [BP + -0xe]
202c:2841  OR AL,byte ptr [DI + 0xe35]
202c:2845  PUSH AX
202c:2846  LES DI,[BP + -0x2c]
202c:2849  PUSH word ptr ES:[DI + 0x2]
202c:284d  PUSH word ptr ES:[DI + 0x6]
202c:2851  PUSH CS
202c:2852  CALL 0x2000:1e44
202c:2855  CMP byte ptr [0x4b8],0x0
202c:285a  JZ 0x2000:2b4b
202c:285c  MOV DI,word ptr [BP + -0xe]
202c:285f  CMP byte ptr [DI + 0xbb5],0x0
202c:2864  JBE 0x2000:2b4b
202c:2866  MOV DI,word ptr [BP + -0xe]
202c:2869  MOV AL,byte ptr [DI + 0xbb5]
202c:286d  XOR AH,AH
202c:286f  MOV DI,AX
202c:2871  SHL DI,0x2
202c:2874  PUSH word ptr [DI + 0x6736]
202c:2878  PUSH word ptr [DI + 0x6734]
202c:287c  MOV DI,word ptr [BP + -0xe]
202c:287f  MOV AL,byte ptr [DI + 0xbb5]
202c:2883  PUSH AX
202c:2884  PUSH 0x0
202c:2886  CALLF 0x2000:3f1c
202c:288b  MOV DI,word ptr [BP + -0xe]
202c:288e  MOV AL,byte ptr [DI + 0x11f5]
202c:2892  XOR AH,AH
202c:2894  XOR DX,DX
202c:2896  MOV word ptr [BP + -0x12],AX
202c:2899  MOV word ptr [BP + -0x10],DX
202c:289c  CMP word ptr [BP + -0x10],0x0
202c:28a0  JG 0x2000:2b70
202c:28a2  JGE 0x2000:2b67
202c:28a4  JMP 0x2000:2c50
202c:28a7  CMP word ptr [BP + -0x12],0x0
202c:28ab  JA 0x2000:2b70
202c:28ad  JMP 0x2000:2c50
202c:28b0  MOV AX,word ptr [BP + -0x12]
202c:28b3  MOV DX,word ptr [BP + -0x10]
202c:28b6  MOV word ptr [BP + -0x30],AX
202c:28b9  MOV word ptr [BP + -0x2e],DX
202c:28bc  MOV AX,0x1
202c:28bf  XOR DX,DX
202c:28c1  CMP DX,word ptr [BP + -0x2e]
202c:28c4  JLE 0x2000:2b89
202c:28c6  JMP 0x2000:2c50
202c:28c9  JL 0x2000:2b93
202c:28cb  CMP AX,word ptr [BP + -0x30]
202c:28ce  JBE 0x2000:2b93
202c:28d0  JMP 0x2000:2c50
202c:28d3  MOV word ptr [BP + -0xe],AX
202c:28d6  MOV word ptr [BP + -0xc],DX
202c:28d9  JMP 0x2000:2ba3
202c:28db  ADD word ptr [BP + -0xe],0x1
202c:28df  ADC word ptr [BP + -0xc],0x0
202c:28e3  MOV DI,word ptr [BP + -0xe]
202c:28e6  CMP byte ptr [DI + 0x126d],0x0
202c:28eb  JNZ 0x2000:2bf5
202c:28ed  LES DI,[BP + -0x2c]
202c:28f0  MOV AL,byte ptr ES:[DI + 0x10]
202c:28f4  AND AL,0x80
202c:28f6  MOV DI,word ptr [BP + -0xe]
202c:28f9  OR AL,byte ptr [DI + 0x1245]
202c:28fd  PUSH AX
202c:28fe  PUSH 0x2
202c:2900  CALLF 0x2000:9424
202c:2905  MOV DX,AX
202c:2907  MOV DI,word ptr [BP + -0xe]
202c:290a  MOV AL,byte ptr [DI + 0x121d]
202c:290e  XOR AH,AH
202c:2910  SUB AX,DX
202c:2912  PUSH AX
202c:2913  LES DI,[BP + -0x2c]
202c:2916  PUSH word ptr ES:[DI + 0x2]
202c:291a  PUSH word ptr ES:[DI + 0x6]
202c:291e  PUSH 0x0
202c:2920  PUSH 0x0
202c:2922  PUSH 0x0
202c:2924  PUSH 0x0
202c:2926  PUSH 0x80
202c:2929  CALLF 0x2000:9424
202c:292e  PUSH AX
202c:292f  PUSH CS
202c:2930  CALL 0x2000:191d
202c:2933  JMP 0x2000:2c3a
202c:2935  LES DI,[BP + -0x2c]
202c:2938  MOV AL,byte ptr ES:[DI + 0x10]
202c:293c  AND AL,0x80
202c:293e  MOV DI,word ptr [BP + -0xe]
202c:2941  OR AL,byte ptr [DI + 0x1245]
202c:2945  PUSH AX
202c:2946  PUSH 0x2
202c:2948  CALLF 0x2000:9424
202c:294d  MOV DX,AX
202c:294f  MOV DI,word ptr [BP + -0xe]
202c:2952  MOV AL,byte ptr [DI + 0x121d]
202c:2956  XOR AH,AH
202c:2958  SUB AX,DX
202c:295a  PUSH AX
202c:295b  LES DI,[BP + -0x2c]
202c:295e  PUSH word ptr ES:[DI + 0x2]
202c:2962  PUSH word ptr ES:[DI + 0x6]
202c:2966  PUSH word ptr ES:[DI + 0xa]
202c:296a  PUSH word ptr ES:[DI + 0x8]
202c:296e  PUSH word ptr ES:[DI + 0xe]
202c:2972  PUSH word ptr ES:[DI + 0xc]
202c:2976  PUSH CS
202c:2977  CALL 0x2000:1776
202c:297a  MOV AX,word ptr [BP + -0xe]
202c:297d  MOV DX,word ptr [BP + -0xc]
202c:2980  CMP DX,word ptr [BP + -0x2e]
202c:2983  JZ 0x2000:2c48
202c:2985  JMP 0x2000:2b9b
202c:2988  CMP AX,word ptr [BP + -0x30]
202c:298b  JZ 0x2000:2c50
202c:298d  JMP 0x2000:2b9b
202c:2990  MOV DI,word ptr [BP + -0xe]
202c:2993  MOV AL,byte ptr [DI + 0xe5d]
202c:2997  XOR AH,AH
202c:2999  XOR DX,DX
202c:299b  MOV word ptr [BP + -0x12],AX
202c:299e  MOV word ptr [BP + -0x10],DX
202c:29a1  CMP word ptr [BP + -0x10],0x0
202c:29a5  JG 0x2000:2c75
202c:29a7  JGE 0x2000:2c6c
202c:29a9  JMP 0x2000:2ecc
202c:29ac  CMP word ptr [BP + -0x12],0x0
202c:29b0  JA 0x2000:2c75
202c:29b2  JMP 0x2000:2ecc
202c:29b5  LES DI,[BP + -0x2c]
202c:29b8  MOV AX,word ptr ES:[DI + 0x2]
202c:29bc  SUB AX,0x7
202c:29bf  PUSH AX
202c:29c0  MOV AX,word ptr ES:[DI + 0x6]
202c:29c4  SUB AX,0x7
202c:29c7  PUSH AX
202c:29c8  MOV DI,word ptr [BP + -0x12]
202c:29cb  MOV AL,byte ptr [DI + 0x1369]
202c:29cf  XOR AH,AH
202c:29d1  SHL AX,0x8
202c:29d4  LES DI,[0x6678]
202c:29d8  ADD DI,AX
202c:29da  PUSH ES
202c:29db  PUSH DI
202c:29dc  MOV DI,word ptr [BP + -0x12]
202c:29df  MOV AL,byte ptr [DI + 0x137d]
202c:29e3  XOR AH,AH
202c:29e5  PUSH AX
202c:29e6  CALLF 0x2000:9424
202c:29eb  MOV DX,AX
202c:29ed  MOV DI,word ptr [BP + -0x12]
202c:29f0  MOV AL,byte ptr [DI + 0x1373]
202c:29f4  XOR AH,AH
202c:29f6  ADD AX,DX
202c:29f8  SHL AX,0x8
202c:29fb  LES DI,[0x6678]
202c:29ff  ADD DI,AX
202c:2a01  PUSH ES
202c:2a02  PUSH DI
202c:2a03  MOV DI,word ptr [BP + -0x12]
202c:2a06  MOV AL,byte ptr [DI + 0x1387]
202c:2a0a  AND AL,0x1
202c:2a0c  CMP AL,0x1
202c:2a0e  MOV AL,0x0
202c:2a10  JNZ 0x2000:2cd3
202c:2a12  INC AX
202c:2a13  PUSH AX
202c:2a14  PUSH CS
202c:2a15  CALL 0x2000:031a
202c:2a18  CMP byte ptr [0x66af],0x0
202c:2a1d  JNZ 0x2000:2ce2
202c:2a1f  JMP 0x2000:2ecc
202c:2a22  LES DI,[BP + -0x2c]
202c:2a25  MOV AX,word ptr ES:[DI + 0x2]
202c:2a29  ADD AX,0xa
202c:2a2c  CWD
202c:2a2d  MOV word ptr [BP + -0x30],AX
202c:2a30  MOV word ptr [BP + -0x2e],DX
202c:2a33  MOV AX,word ptr ES:[DI + 0x2]
202c:2a37  SUB AX,0xa
202c:2a3a  CWD
202c:2a3b  CMP DX,word ptr [BP + -0x2e]
202c:2a3e  JLE 0x2000:2d03
202c:2a40  JMP 0x2000:2ecc
202c:2a43  JL 0x2000:2d0d
202c:2a45  CMP AX,word ptr [BP + -0x30]
202c:2a48  JBE 0x2000:2d0d
202c:2a4a  JMP 0x2000:2ecc
202c:2a4d  MOV word ptr [BP + -0x1a],AX
202c:2a50  MOV word ptr [BP + -0x18],DX
202c:2a53  JMP 0x2000:2d1d
202c:2a55  ADD word ptr [BP + -0x1a],0x1
202c:2a59  ADC word ptr [BP + -0x18],0x0
202c:2a5d  CMP word ptr [BP + -0x18],-0x1
202c:2a61  JG 0x2000:2d31
202c:2a63  JGE 0x2000:2d28
202c:2a65  JMP 0x2000:2eb6
202c:2a68  CMP word ptr [BP + -0x1a],-0x1
202c:2a6c  JA 0x2000:2d31
202c:2a6e  JMP 0x2000:2eb6
202c:2a71  CMP word ptr [BP + -0x18],0x0
202c:2a75  JL 0x2000:2d46
202c:2a77  JLE 0x2000:2d3c
202c:2a79  JMP 0x2000:2eb6
202c:2a7c  CMP word ptr [BP + -0x1a],0x1f8
202c:2a81  JC 0x2000:2d46
202c:2a83  JMP 0x2000:2eb6
202c:2a86  LES DI,[BP + -0x2c]
202c:2a89  MOV AX,word ptr ES:[DI + 0x6]
202c:2a8d  ADD AX,0xa
202c:2a90  CWD
202c:2a91  MOV word ptr [BP + -0x34],AX
202c:2a94  MOV word ptr [BP + -0x32],DX
202c:2a97  MOV AX,word ptr ES:[DI + 0x6]
202c:2a9b  SUB AX,0xa
202c:2a9e  CWD
202c:2a9f  CMP DX,word ptr [BP + -0x32]
202c:2aa2  JLE 0x2000:2d67
202c:2aa4  JMP 0x2000:2eb6
202c:2aa7  JL 0x2000:2d71
202c:2aa9  CMP AX,word ptr [BP + -0x34]
202c:2aac  JBE 0x2000:2d71
202c:2aae  JMP 0x2000:2eb6
202c:2ab1  MOV word ptr [BP + -0x1e],AX
202c:2ab4  MOV word ptr [BP + -0x1c],DX
202c:2ab7  JMP 0x2000:2d81
202c:2ab9  ADD word ptr [BP + -0x1e],0x1
202c:2abd  ADC word ptr [BP + -0x1c],0x0
202c:2ac1  CMP word ptr [BP + -0x1c],-0x1
202c:2ac5  JG 0x2000:2d95
202c:2ac7  JGE 0x2000:2d8c
202c:2ac9  JMP 0x2000:2ea0
202c:2acc  CMP word ptr [BP + -0x1e],-0x1
202c:2ad0  JA 0x2000:2d95
202c:2ad2  JMP 0x2000:2ea0
202c:2ad5  CMP word ptr [BP + -0x1c],0x0
202c:2ad9  JL 0x2000:2daa
202c:2adb  JLE 0x2000:2da0
202c:2add  JMP 0x2000:2ea0
202c:2ae0  CMP word ptr [BP + -0x1e],0x15e
202c:2ae5  JC 0x2000:2daa
202c:2ae7  JMP 0x2000:2ea0
202c:2aea  MOV DX,word ptr [BP + -0x1a]
202c:2aed  MOV AX,word ptr [BP + -0x1e]
202c:2af0  SHL AX,0x2
202c:2af3  LES DI,[0x6674]
202c:2af7  ADD DI,AX
202c:2af9  LES DI,ES:[DI]
202c:2afc  ADD DI,DX
202c:2afe  MOV AL,byte ptr ES:[DI]
202c:2b01  MOV AH,0x1
202c:2b03  MOV DX,0x20
202c:2b06  CALLF 0x2000:8f31
202c:2b0b  MOV DI,DX
202c:2b0d  TEST byte ptr [DI + 0x14e0],AL
202c:2b11  JZ 0x2000:2e2a
202c:2b13  MOV AX,word ptr [BP + -0x1a]
202c:2b16  MOV DX,word ptr [BP + -0x18]
202c:2b19  ADD AX,0x3
202c:2b1c  ADC DX,0x0
202c:2b1f  MOV CX,AX
202c:2b21  MOV AX,word ptr [BP + -0x1e]
202c:2b24  MOV DX,word ptr [BP + -0x1c]
202c:2b27  SUB AX,0x3
202c:2b2a  SBB DX,0x0
202c:2b2d  SHL AX,0x2
202c:2b30  LES DI,[0x6674]
202c:2b34  ADD DI,AX
202c:2b36  LES DI,ES:[DI]
202c:2b39  ADD DI,CX
202c:2b3b  MOV AL,byte ptr ES:[DI]
202c:2b3e  MOV AH,0x1
202c:2b40  MOV DX,0x20
202c:2b43  CALLF 0x2000:8f31
202c:2b48  MOV DI,DX
202c:2b4a  TEST byte ptr [DI + 0x6604],AL
202c:2b4e  JZ 0x2000:2e2a
202c:2b50  MOV DX,word ptr [BP + -0x1a]
202c:2b53  MOV AX,word ptr [BP + -0x1e]
202c:2b56  SHL AX,0x2
202c:2b59  LES DI,[0x6674]
202c:2b5d  ADD DI,AX
202c:2b5f  LES DI,ES:[DI]
202c:2b62  ADD DI,DX
202c:2b64  ADD byte ptr ES:[DI],0x4
202c:2b68  JMP 0x2000:2ea0
202c:2b6a  MOV DX,word ptr [BP + -0x1a]
202c:2b6d  MOV AX,word ptr [BP + -0x1e]
202c:2b70  SHL AX,0x2
202c:2b73  LES DI,[0x6674]
202c:2b77  ADD DI,AX
202c:2b79  LES DI,ES:[DI]
202c:2b7c  ADD DI,DX
202c:2b7e  MOV AL,byte ptr ES:[DI]
202c:2b81  CMP AL,0xa4
202c:2b83  JC 0x2000:2ea0
202c:2b85  CMP AL,0xa7
202c:2b87  JA 0x2000:2ea0
202c:2b89  MOV AX,word ptr [BP + -0x1a]
202c:2b8c  MOV DX,word ptr [BP + -0x18]
202c:2b8f  ADD AX,0x3
202c:2b92  ADC DX,0x0
202c:2b95  MOV CX,AX
202c:2b97  MOV AX,word ptr [BP + -0x1e]
202c:2b9a  MOV DX,word ptr [BP + -0x1c]
202c:2b9d  SUB AX,0x3
202c:2ba0  SBB DX,0x0
202c:2ba3  SHL AX,0x2
202c:2ba6  LES DI,[0x6674]
202c:2baa  ADD DI,AX
202c:2bac  LES DI,ES:[DI]
202c:2baf  ADD DI,CX
202c:2bb1  MOV AL,byte ptr ES:[DI]
202c:2bb4  NOT AL
202c:2bb6  MOV AH,0x1
202c:2bb8  MOV DX,0x20
202c:2bbb  CALLF 0x2000:8f31
202c:2bc0  MOV DI,DX
202c:2bc2  TEST byte ptr [DI + 0x6604],AL
202c:2bc6  JZ 0x2000:2ea0
202c:2bc8  MOV DX,word ptr [BP + -0x1a]
202c:2bcb  MOV AX,word ptr [BP + -0x1e]
202c:2bce  SHL AX,0x2
202c:2bd1  LES DI,[0x6674]
202c:2bd5  ADD DI,AX
202c:2bd7  LES DI,ES:[DI]
202c:2bda  ADD DI,DX
202c:2bdc  SUB byte ptr ES:[DI],0x4
202c:2be0  MOV AX,word ptr [BP + -0x1e]
202c:2be3  MOV DX,word ptr [BP + -0x1c]
202c:2be6  CMP DX,word ptr [BP + -0x32]
202c:2be9  JZ 0x2000:2eae
202c:2beb  JMP 0x2000:2d79
202c:2bee  CMP AX,word ptr [BP + -0x34]
202c:2bf1  JZ 0x2000:2eb6
202c:2bf3  JMP 0x2000:2d79
202c:2bf6  MOV AX,word ptr [BP + -0x1a]
202c:2bf9  MOV DX,word ptr [BP + -0x18]
202c:2bfc  CMP DX,word ptr [BP + -0x2e]
202c:2bff  JZ 0x2000:2ec4
202c:2c01  JMP 0x2000:2d15
202c:2c04  CMP AX,word ptr [BP + -0x30]
202c:2c07  JZ 0x2000:2ecc
202c:2c09  JMP 0x2000:2d15
202c:2c0c  CMP word ptr [BP + -0x14],0x0
202c:2c10  JZ 0x2000:2ed5
202c:2c12  JMP 0x2000:2849
202c:2c15  CMP word ptr [BP + -0x16],0x258
202c:2c1a  JZ 0x2000:2edf
202c:2c1c  JMP 0x2000:2849
202c:2c1f  XOR AX,AX
202c:2c21  MOV word ptr [BP + -0x16],AX
202c:2c24  MOV word ptr [BP + -0x14],AX
202c:2c27  JMP 0x2000:2ef1
202c:2c29  ADD word ptr [BP + -0x16],0x1
202c:2c2d  ADC word ptr [BP + -0x14],0x0
202c:2c31  IMUL AX,word ptr [BP + -0x16],0x14
202c:2c35  LES DI,[0x6694]
202c:2c39  ADD DI,AX
202c:2c3b  CMP byte ptr ES:[DI + 0x12],0x0
202c:2c40  JA 0x2000:2f05
202c:2c42  JMP 0x2000:314f
202c:2c45  IMUL AX,word ptr [BP + -0x16],0x14
202c:2c49  LES DI,[0x6694]
202c:2c4d  ADD DI,AX
202c:2c4f  MOV AL,byte ptr ES:[DI + 0x12]
202c:2c53  AND AL,0x7f
202c:2c55  XOR AH,AH
202c:2c57  MOV DI,AX
202c:2c59  CMP byte ptr [DI + 0x6bd],0x1
202c:2c5e  JZ 0x2000:2f23
202c:2c60  JMP 0x2000:314f
202c:2c63  MOV AX,word ptr [BP + -0x1a]
202c:2c66  MOV DX,word ptr [BP + -0x18]
202c:2c69  ADD AX,word ptr [BP + -0xa]
202c:2c6c  ADC DX,word ptr [BP + -0x8]
202c:2c6f  MOV CX,AX
202c:2c71  MOV BX,DX
202c:2c73  IMUL AX,word ptr [BP + -0x16],0x14
202c:2c77  LES DI,[0x6694]
202c:2c7b  ADD DI,AX
202c:2c7d  MOV AX,word ptr ES:[DI + 0x2]
202c:2c81  CWD
202c:2c82  CMP DX,BX
202c:2c84  JL 0x2000:2f52
202c:2c86  JLE 0x2000:2f4b
202c:2c88  JMP 0x2000:314f
202c:2c8b  CMP AX,CX
202c:2c8d  JC 0x2000:2f52
202c:2c8f  JMP 0x2000:314f
202c:2c92  MOV AX,word ptr [BP + -0x1a]
202c:2c95  MOV DX,word ptr [BP + -0x18]
202c:2c98  SUB AX,word ptr [BP + -0xa]
202c:2c9b  SBB DX,word ptr [BP + -0x8]
202c:2c9e  MOV CX,AX
202c:2ca0  MOV BX,DX
202c:2ca2  IMUL AX,word ptr [BP + -0x16],0x14
202c:2ca6  LES DI,[0x6694]
202c:2caa  ADD DI,AX
202c:2cac  MOV AX,word ptr ES:[DI + 0x2]
202c:2cb0  CWD
202c:2cb1  CMP DX,BX
202c:2cb3  JG 0x2000:2f81
202c:2cb5  JGE 0x2000:2f7a
202c:2cb7  JMP 0x2000:314f
202c:2cba  CMP AX,CX
202c:2cbc  JA 0x2000:2f81
202c:2cbe  JMP 0x2000:314f
202c:2cc1  MOV AX,word ptr [BP + -0x1e]
202c:2cc4  MOV DX,word ptr [BP + -0x1c]
202c:2cc7  ADD AX,word ptr [BP + -0xa]
202c:2cca  ADC DX,word ptr [BP + -0x8]
202c:2ccd  MOV CX,AX
202c:2ccf  MOV BX,DX
202c:2cd1  IMUL AX,word ptr [BP + -0x16],0x14
202c:2cd5  LES DI,[0x6694]
202c:2cd9  ADD DI,AX
202c:2cdb  MOV AX,word ptr ES:[DI + 0x6]
202c:2cdf  CWD
202c:2ce0  CMP DX,BX
202c:2ce2  JL 0x2000:2fb0
202c:2ce4  JLE 0x2000:2fa9
202c:2ce6  JMP 0x2000:314f
202c:2ce9  CMP AX,CX
202c:2ceb  JC 0x2000:2fb0
202c:2ced  JMP 0x2000:314f
202c:2cf0  MOV AX,word ptr [BP + -0x1e]
202c:2cf3  MOV DX,word ptr [BP + -0x1c]
202c:2cf6  SUB AX,word ptr [BP + -0xa]
202c:2cf9  SBB DX,word ptr [BP + -0x8]
202c:2cfc  MOV CX,AX
202c:2cfe  MOV BX,DX
202c:2d00  IMUL AX,word ptr [BP + -0x16],0x14
202c:2d04  LES DI,[0x6694]
202c:2d08  ADD DI,AX
202c:2d0a  MOV AX,word ptr ES:[DI + 0x6]
202c:2d0e  CWD
202c:2d0f  CMP DX,BX
202c:2d11  JG 0x2000:2fdf
202c:2d13  JGE 0x2000:2fd8
202c:2d15  JMP 0x2000:314f
202c:2d18  CMP AX,CX
202c:2d1a  JA 0x2000:2fdf
202c:2d1c  JMP 0x2000:314f
202c:2d1f  IMUL AX,word ptr [BP + -0x16],0x14
202c:2d23  LES DI,[0x6694]
202c:2d27  ADD DI,AX
202c:2d29  MOV AX,word ptr ES:[DI + 0x2]
202c:2d2d  CWD
202c:2d2e  SUB AX,word ptr [BP + -0x1a]
202c:2d31  SBB DX,word ptr [BP + -0x18]
202c:2d34  MOV word ptr [BP + -0x12],AX
202c:2d37  MOV word ptr [BP + -0x10],DX
202c:2d3a  MOV AX,word ptr [BP + -0x12]
202c:2d3d  MOV DX,word ptr [BP + -0x10]
202c:2d40  OR DX,DX
202c:2d42  JNS 0x2000:300b
202c:2d44  NOT DX
202c:2d46  NEG AX
202c:2d48  SBB DX,-0x1
202c:2d4b  MOV CX,AX
202c:2d4d  MOV BX,DX
202c:2d4f  MOV AX,word ptr [BP + -0xa]
202c:2d52  MOV DX,word ptr [BP + -0x8]
202c:2d55  SUB AX,CX
202c:2d57  SBB DX,BX
202c:2d59  MOV word ptr [BP + -0xe],AX
202c:2d5c  MOV word ptr [BP + -0xc],DX
202c:2d5f  CMP word ptr [BP + -0xc],0x0
202c:2d63  JG 0x2000:302d
202c:2d65  JL 0x2000:3097
202c:2d67  CMP word ptr [BP + -0xe],0x0
202c:2d6b  JBE 0x2000:3097
202c:2d6d  CMP word ptr [BP + -0x10],0x0
202c:2d71  JG 0x2000:303b
202c:2d73  JL 0x2000:3062
202c:2d75  CMP word ptr [BP + -0x12],0x0
202c:2d79  JBE 0x2000:3062
202c:2d7b  MOV AX,word ptr [BP + -0xe]
202c:2d7e  MOV DX,word ptr [BP + -0xc]
202c:2d81  MOV CX,word ptr [BP + -0x22]
202c:2d84  MOV BX,word ptr [BP + -0x20]
202c:2d87  CALLF 0x2000:8b50
202c:2d8c  MOV CX,AX
202c:2d8e  MOV BX,DX
202c:2d90  IMUL AX,word ptr [BP + -0x16],0x14
202c:2d94  LES DI,[0x6694]
202c:2d98  ADD DI,AX
202c:2d9a  ADD word ptr ES:[DI + 0x8],CX
202c:2d9e  ADC word ptr ES:[DI + 0xa],BX
202c:2da2  CMP word ptr [BP + -0x10],0x0
202c:2da6  JL 0x2000:3070
202c:2da8  JG 0x2000:3097
202c:2daa  CMP word ptr [BP + -0x12],0x0
202c:2dae  JNC 0x2000:3097
202c:2db0  MOV AX,word ptr [BP + -0xe]
202c:2db3  MOV DX,word ptr [BP + -0xc]
202c:2db6  MOV CX,word ptr [BP + -0x22]
202c:2db9  MOV BX,word ptr [BP + -0x20]
202c:2dbc  CALLF 0x2000:8b50
202c:2dc1  MOV CX,AX
202c:2dc3  MOV BX,DX
202c:2dc5  IMUL AX,word ptr [BP + -0x16],0x14
202c:2dc9  LES DI,[0x6694]
202c:2dcd  ADD DI,AX
202c:2dcf  SUB word ptr ES:[DI + 0x8],CX
202c:2dd3  SBB word ptr ES:[DI + 0xa],BX
202c:2dd7  IMUL AX,word ptr [BP + -0x16],0x14
202c:2ddb  LES DI,[0x6694]
202c:2ddf  ADD DI,AX
202c:2de1  MOV AX,word ptr ES:[DI + 0x6]
202c:2de5  CWD
202c:2de6  SUB AX,word ptr [BP + -0x1e]
202c:2de9  SBB DX,word ptr [BP + -0x1c]
202c:2dec  MOV word ptr [BP + -0x12],AX
202c:2def  MOV word ptr [BP + -0x10],DX
202c:2df2  MOV AX,word ptr [BP + -0x12]
202c:2df5  MOV DX,word ptr [BP + -0x10]
202c:2df8  OR DX,DX
202c:2dfa  JNS 0x2000:30c3
202c:2dfc  NOT DX
202c:2dfe  NEG AX
202c:2e00  SBB DX,-0x1
202c:2e03  MOV CX,AX
202c:2e05  MOV BX,DX
202c:2e07  MOV AX,word ptr [BP + -0xa]
202c:2e0a  MOV DX,word ptr [BP + -0x8]
202c:2e0d  SUB AX,CX
202c:2e0f  SBB DX,BX
202c:2e11  MOV word ptr [BP + -0xe],AX
202c:2e14  MOV word ptr [BP + -0xc],DX
202c:2e17  CMP word ptr [BP + -0xc],0x0
202c:2e1b  JG 0x2000:30e5
202c:2e1d  JL 0x2000:314f
202c:2e1f  CMP word ptr [BP + -0xe],0x0
202c:2e23  JBE 0x2000:314f
202c:2e25  CMP word ptr [BP + -0x10],0x0
202c:2e29  JG 0x2000:30f3
202c:2e2b  JL 0x2000:311a
202c:2e2d  CMP word ptr [BP + -0x12],0x0
202c:2e31  JBE 0x2000:311a
202c:2e33  MOV AX,word ptr [BP + -0xe]
202c:2e36  MOV DX,word ptr [BP + -0xc]
202c:2e39  MOV CX,word ptr [BP + -0x22]
202c:2e3c  MOV BX,word ptr [BP + -0x20]
202c:2e3f  CALLF 0x2000:8b50
202c:2e44  MOV CX,AX
202c:2e46  MOV BX,DX
202c:2e48  IMUL AX,word ptr [BP + -0x16],0x14
202c:2e4c  LES DI,[0x6694]
202c:2e50  ADD DI,AX
202c:2e52  ADD word ptr ES:[DI + 0xc],CX
202c:2e56  ADC word ptr ES:[DI + 0xe],BX
202c:2e5a  CMP word ptr [BP + -0x10],0x0
202c:2e5e  JL 0x2000:3128
202c:2e60  JG 0x2000:314f
202c:2e62  CMP word ptr [BP + -0x12],0x0
202c:2e66  JNC 0x2000:314f
202c:2e68  MOV AX,word ptr [BP + -0xe]
202c:2e6b  MOV DX,word ptr [BP + -0xc]
202c:2e6e  MOV CX,word ptr [BP + -0x22]
202c:2e71  MOV BX,word ptr [BP + -0x20]
202c:2e74  CALLF 0x2000:8b50
202c:2e79  MOV CX,AX
202c:2e7b  MOV BX,DX
202c:2e7d  IMUL AX,word ptr [BP + -0x16],0x14
202c:2e81  LES DI,[0x6694]
202c:2e85  ADD DI,AX
202c:2e87  SUB word ptr ES:[DI + 0xc],CX
202c:2e8b  SBB word ptr ES:[DI + 0xe],BX
202c:2e8f  CMP word ptr [BP + -0x14],0x0
202c:2e93  JZ 0x2000:3158
202c:2e95  JMP 0x2000:2ee9
202c:2e98  CMP word ptr [BP + -0x16],0x258
202c:2e9d  JZ 0x2000:3162
202c:2e9f  JMP 0x2000:2ee9
202c:2ea2  MOV AL,byte ptr [BP + -0x23]
202c:2ea5  XOR AH,AH
202c:2ea7  MOV DI,AX
202c:2ea9  MOV AL,byte ptr [DI + 0x13d7]
202c:2ead  XOR AH,AH
202c:2eaf  SHR AX,0x1
202c:2eb1  MOV word ptr [BP + -0x2],AX
202c:2eb4  MOV AX,word ptr [BP + -0x2]
202c:2eb7  MOV word ptr [BP + -0x26],AX
202c:2eba  MOV AX,word ptr [BP + -0x2]
202c:2ebd  NEG AX
202c:2ebf  CMP AX,word ptr [BP + -0x26]
202c:2ec2  JLE 0x2000:3187
202c:2ec4  JMP 0x2000:3245
202c:2ec7  MOV word ptr [BP + -0x4],AX
202c:2eca  JMP 0x2000:318f
202c:2ecc  INC word ptr [BP + -0x4]
202c:2ecf  MOV AX,word ptr [BP + -0x4]
202c:2ed2  ADD AX,word ptr [BP + 0x8]
202c:2ed5  CWD
202c:2ed6  MOV word ptr [BP + -0x1a],AX
202c:2ed9  MOV word ptr [BP + -0x18],DX
202c:2edc  MOV AX,word ptr [BP + -0x2]
202c:2edf  MOV word ptr [BP + -0x28],AX
202c:2ee2  MOV AX,word ptr [BP + -0x2]
202c:2ee5  NEG AX
202c:2ee7  CMP AX,word ptr [BP + -0x28]
202c:2eea  JLE 0x2000:31af
202c:2eec  JMP 0x2000:323a
202c:2eef  MOV word ptr [BP + -0x6],AX
202c:2ef2  JMP 0x2000:31b7
202c:2ef4  INC word ptr [BP + -0x6]
202c:2ef7  MOV AX,word ptr [BP + -0x6]
202c:2efa  ADD AX,word ptr [BP + 0x6]
202c:2efd  CWD
202c:2efe  MOV word ptr [BP + -0x1e],AX
202c:2f01  MOV word ptr [BP + -0x1c],DX
202c:2f04  MOV DX,word ptr [BP + -0x1a]
202c:2f07  MOV AX,word ptr [BP + -0x1e]
202c:2f0a  SHL AX,0x2
202c:2f0d  LES DI,[0x6674]
202c:2f11  ADD DI,AX
202c:2f13  LES DI,ES:[DI]
202c:2f16  ADD DI,DX
202c:2f18  MOV AL,byte ptr ES:[DI]
202c:2f1b  MOV AH,0x1
202c:2f1d  MOV DX,0x20
202c:2f20  CALLF 0x2000:8f31
202c:2f25  MOV DI,DX
202c:2f27  TEST byte ptr [DI + 0x6624],AL
202c:2f2b  JZ 0x2000:322f
202c:2f2d  PUSH 0x8
202c:2f2f  CALLF 0x2000:9424
202c:2f34  OR AX,AX
202c:2f36  JNZ 0x2000:322f
202c:2f38  PUSH 0x3
202c:2f3a  MOV DX,word ptr [BP + -0x1a]
202c:2f3d  MOV AX,word ptr [BP + -0x1e]
202c:2f40  SHL AX,0x2
202c:2f43  LES DI,[0x6674]
202c:2f47  ADD DI,AX
202c:2f49  LES DI,ES:[DI]
202c:2f4c  ADD DI,DX
202c:2f4e  MOV AL,byte ptr ES:[DI]
202c:2f51  XOR AH,AH
202c:2f53  PUSH AX
202c:2f54  PUSH word ptr [BP + -0x1a]
202c:2f57  PUSH word ptr [BP + -0x1e]
202c:2f5a  PUSH 0x0
202c:2f5c  PUSH 0x0
202c:2f5e  PUSH 0x0
202c:2f60  PUSH 0x0
202c:2f62  PUSH 0x80
202c:2f65  CALLF 0x2000:9424
202c:2f6a  PUSH AX
202c:2f6b  PUSH CS
202c:2f6c  CALL 0x2000:191d
202c:2f6f  MOV AX,word ptr [BP + -0x6]
202c:2f72  CMP AX,word ptr [BP + -0x28]
202c:2f75  JZ 0x2000:323a
202c:2f77  JMP 0x2000:31b4
202c:2f7a  MOV AX,word ptr [BP + -0x4]
202c:2f7d  CMP AX,word ptr [BP + -0x26]
202c:2f80  JZ 0x2000:3245
202c:2f82  JMP 0x2000:318c
202c:2f85  MOV AL,byte ptr [BP + -0x23]
202c:2f88  XOR AH,AH
202c:2f8a  MOV DI,AX
202c:2f8c  MOV AL,byte ptr [DI + 0x1451]
202c:2f90  XOR AH,AH
202c:2f92  MOV word ptr [BP + -0x2],AX
202c:2f95  CMP word ptr [BP + -0x2],0x0
202c:2f99  JG 0x2000:325e
202c:2f9b  JMP 0x2000:34a6
202c:2f9e  MOV AX,word ptr [BP + 0x8]
202c:2fa1  SUB AX,0x7
202c:2fa4  PUSH AX
202c:2fa5  MOV AX,word ptr [BP + 0x6]
202c:2fa8  SUB AX,0x7
202c:2fab  PUSH AX
202c:2fac  MOV DI,word ptr [BP + -0x2]
202c:2faf  MOV AL,byte ptr [DI + 0x1369]
202c:2fb3  XOR AH,AH
202c:2fb5  SHL AX,0x8
202c:2fb8  LES DI,[0x6678]
202c:2fbc  ADD DI,AX
202c:2fbe  PUSH ES
202c:2fbf  PUSH DI
202c:2fc0  MOV DI,word ptr [BP + -0x2]
202c:2fc3  MOV AL,byte ptr [DI + 0x137d]
202c:2fc7  XOR AH,AH
202c:2fc9  PUSH AX
202c:2fca  CALLF 0x2000:9424
202c:2fcf  MOV DX,AX
202c:2fd1  MOV DI,word ptr [BP + -0x2]
202c:2fd4  MOV AL,byte ptr [DI + 0x1373]
202c:2fd8  XOR AH,AH
202c:2fda  ADD AX,DX
202c:2fdc  SHL AX,0x8
202c:2fdf  LES DI,[0x6678]
202c:2fe3  ADD DI,AX
202c:2fe5  PUSH ES
202c:2fe6  PUSH DI
202c:2fe7  MOV DI,word ptr [BP + -0x2]
202c:2fea  MOV AL,byte ptr [DI + 0x1387]
202c:2fee  AND AL,0x1
202c:2ff0  CMP AL,0x1
202c:2ff2  MOV AL,0x0
202c:2ff4  JNZ 0x2000:32b7
202c:2ff6  INC AX
202c:2ff7  PUSH AX
202c:2ff8  PUSH CS
202c:2ff9  CALL 0x2000:031a
202c:2ffc  CMP byte ptr [0x66af],0x0
202c:3001  JNZ 0x2000:32c6
202c:3003  JMP 0x2000:34a6
202c:3006  MOV AX,word ptr [BP + 0x8]
202c:3009  ADD AX,0xa
202c:300c  CWD
202c:300d  MOV word ptr [BP + -0x28],AX
202c:3010  MOV word ptr [BP + -0x26],DX
202c:3013  MOV AX,word ptr [BP + 0x8]
202c:3016  SUB AX,0xa
202c:3019  CWD
202c:301a  CMP DX,word ptr [BP + -0x26]
202c:301d  JLE 0x2000:32e2
202c:301f  JMP 0x2000:34a6
202c:3022  JL 0x2000:32ec
202c:3024  CMP AX,word ptr [BP + -0x28]
202c:3027  JBE 0x2000:32ec
202c:3029  JMP 0x2000:34a6
202c:302c  MOV word ptr [BP + -0x1a],AX
202c:302f  MOV word ptr [BP + -0x18],DX
202c:3032  JMP 0x2000:32fc
202c:3034  ADD word ptr [BP + -0x1a],0x1
202c:3038  ADC word ptr [BP + -0x18],0x0
202c:303c  CMP word ptr [BP + -0x18],-0x1
202c:3040  JG 0x2000:3310
202c:3042  JGE 0x2000:3307
202c:3044  JMP 0x2000:3490
202c:3047  CMP word ptr [BP + -0x1a],-0x1
202c:304b  JA 0x2000:3310
202c:304d  JMP 0x2000:3490
202c:3050  CMP word ptr [BP + -0x18],0x0
202c:3054  JL 0x2000:3325
202c:3056  JLE 0x2000:331b
202c:3058  JMP 0x2000:3490
202c:305b  CMP word ptr [BP + -0x1a],0x1f8
202c:3060  JC 0x2000:3325
202c:3062  JMP 0x2000:3490
202c:3065  MOV AX,word ptr [BP + 0x6]
202c:3068  ADD AX,0xa
202c:306b  CWD
202c:306c  MOV word ptr [BP + -0x2c],AX
202c:306f  MOV word ptr [BP + -0x2a],DX
202c:3072  MOV AX,word ptr [BP + 0x6]
202c:3075  SUB AX,0xa
202c:3078  CWD
202c:3079  CMP DX,word ptr [BP + -0x2a]
202c:307c  JLE 0x2000:3341
202c:307e  JMP 0x2000:3490
202c:3081  JL 0x2000:334b
202c:3083  CMP AX,word ptr [BP + -0x2c]
202c:3086  JBE 0x2000:334b
202c:3088  JMP 0x2000:3490
202c:308b  MOV word ptr [BP + -0x1e],AX
202c:308e  MOV word ptr [BP + -0x1c],DX
202c:3091  JMP 0x2000:335b
202c:3093  ADD word ptr [BP + -0x1e],0x1
202c:3097  ADC word ptr [BP + -0x1c],0x0
202c:309b  CMP word ptr [BP + -0x1c],-0x1
202c:309f  JG 0x2000:336f
202c:30a1  JGE 0x2000:3366
202c:30a3  JMP 0x2000:347a
202c:30a6  CMP word ptr [BP + -0x1e],-0x1
202c:30aa  JA 0x2000:336f
202c:30ac  JMP 0x2000:347a
202c:30af  CMP word ptr [BP + -0x1c],0x0
202c:30b3  JL 0x2000:3384
202c:30b5  JLE 0x2000:337a
202c:30b7  JMP 0x2000:347a
202c:30ba  CMP word ptr [BP + -0x1e],0x15e
202c:30bf  JC 0x2000:3384
202c:30c1  JMP 0x2000:347a
202c:30c4  MOV DX,word ptr [BP + -0x1a]
202c:30c7  MOV AX,word ptr [BP + -0x1e]
202c:30ca  SHL AX,0x2
202c:30cd  LES DI,[0x6674]
202c:30d1  ADD DI,AX
202c:30d3  LES DI,ES:[DI]
202c:30d6  ADD DI,DX
202c:30d8  MOV AL,byte ptr ES:[DI]
202c:30db  MOV AH,0x1
202c:30dd  MOV DX,0x20
202c:30e0  CALLF 0x2000:8f31
202c:30e5  MOV DI,DX
202c:30e7  TEST byte ptr [DI + 0x14e0],AL
202c:30eb  JZ 0x2000:3404
202c:30ed  MOV AX,word ptr [BP + -0x1a]
202c:30f0  MOV DX,word ptr [BP + -0x18]
202c:30f3  ADD AX,0x3
202c:30f6  ADC DX,0x0
202c:30f9  MOV CX,AX
202c:30fb  MOV AX,word ptr [BP + -0x1e]
202c:30fe  MOV DX,word ptr [BP + -0x1c]
202c:3101  SUB AX,0x3
202c:3104  SBB DX,0x0
202c:3107  SHL AX,0x2
202c:310a  LES DI,[0x6674]
202c:310e  ADD DI,AX
202c:3110  LES DI,ES:[DI]
202c:3113  ADD DI,CX
202c:3115  MOV AL,byte ptr ES:[DI]
202c:3118  MOV AH,0x1
202c:311a  MOV DX,0x20
202c:311d  CALLF 0x2000:8f31
202c:3122  MOV DI,DX
202c:3124  TEST byte ptr [DI + 0x6604],AL
202c:3128  JZ 0x2000:3404
202c:312a  MOV DX,word ptr [BP + -0x1a]
202c:312d  MOV AX,word ptr [BP + -0x1e]
202c:3130  SHL AX,0x2
202c:3133  LES DI,[0x6674]
202c:3137  ADD DI,AX
202c:3139  LES DI,ES:[DI]
202c:313c  ADD DI,DX
202c:313e  ADD byte ptr ES:[DI],0x4
202c:3142  JMP 0x2000:347a
202c:3144  MOV DX,word ptr [BP + -0x1a]
202c:3147  MOV AX,word ptr [BP + -0x1e]
202c:314a  SHL AX,0x2
202c:314d  LES DI,[0x6674]
202c:3151  ADD DI,AX
202c:3153  LES DI,ES:[DI]
202c:3156  ADD DI,DX
202c:3158  MOV AL,byte ptr ES:[DI]
202c:315b  CMP AL,0xa4
202c:315d  JC 0x2000:347a
202c:315f  CMP AL,0xa7
202c:3161  JA 0x2000:347a
202c:3163  MOV AX,word ptr [BP + -0x1a]
202c:3166  MOV DX,word ptr [BP + -0x18]
202c:3169  ADD AX,0x3
202c:316c  ADC DX,0x0
202c:316f  MOV CX,AX
202c:3171  MOV AX,word ptr [BP + -0x1e]
202c:3174  MOV DX,word ptr [BP + -0x1c]
202c:3177  SUB AX,0x3
202c:317a  SBB DX,0x0
202c:317d  SHL AX,0x2
202c:3180  LES DI,[0x6674]
202c:3184  ADD DI,AX
202c:3186  LES DI,ES:[DI]
202c:3189  ADD DI,CX
202c:318b  MOV AL,byte ptr ES:[DI]
202c:318e  NOT AL
202c:3190  MOV AH,0x1
202c:3192  MOV DX,0x20
202c:3195  CALLF 0x2000:8f31
202c:319a  MOV DI,DX
202c:319c  TEST byte ptr [DI + 0x6604],AL
202c:31a0  JZ 0x2000:347a
202c:31a2  MOV DX,word ptr [BP + -0x1a]
202c:31a5  MOV AX,word ptr [BP + -0x1e]
202c:31a8  SHL AX,0x2
202c:31ab  LES DI,[0x6674]
202c:31af  ADD DI,AX
202c:31b1  LES DI,ES:[DI]
202c:31b4  ADD DI,DX
202c:31b6  SUB byte ptr ES:[DI],0x4
202c:31ba  MOV AX,word ptr [BP + -0x1e]
202c:31bd  MOV DX,word ptr [BP + -0x1c]
202c:31c0  CMP DX,word ptr [BP + -0x2a]
202c:31c3  JZ 0x2000:3488
202c:31c5  JMP 0x2000:3353
202c:31c8  CMP AX,word ptr [BP + -0x2c]
202c:31cb  JZ 0x2000:3490
202c:31cd  JMP 0x2000:3353
202c:31d0  MOV AX,word ptr [BP + -0x1a]
202c:31d3  MOV DX,word ptr [BP + -0x18]
202c:31d6  CMP DX,word ptr [BP + -0x26]
202c:31d9  JZ 0x2000:349e
202c:31db  JMP 0x2000:32f4
202c:31de  CMP AX,word ptr [BP + -0x28]
202c:31e1  JZ 0x2000:34a6
202c:31e3  JMP 0x2000:32f4
202c:31e6  MOV AL,[0x669c]
202c:31e9  XOR AH,AH
202c:31eb  MOV word ptr [BP + -0x26],AX
202c:31ee  MOV AX,0x1
202c:31f1  CMP AX,word ptr [BP + -0x26]
202c:31f4  JLE 0x2000:34b9
202c:31f6  JMP 0x2000:35af
202c:31f9  MOV word ptr [BP + -0x2],AX
202c:31fc  JMP 0x2000:34c1
202c:31fe  INC word ptr [BP + -0x2]
202c:3201  IMUL AX,word ptr [BP + -0x2],0xe
202c:3205  LES DI,[0x6698]
202c:3209  ADD DI,AX
202c:320b  CMP byte ptr ES:[DI + -0x2],0x0
202c:3210  JA 0x2000:34d5
202c:3212  JMP 0x2000:35a4
202c:3215  MOV AL,byte ptr [BP + -0x23]
202c:3218  XOR AH,AH
202c:321a  MOV DI,AX
202c:321c  MOV AL,byte ptr [DI + 0x13d7]
202c:3220  XOR AH,AH
202c:3222  MOV DX,AX
202c:3224  MOV AX,word ptr [BP + 0x8]
202c:3227  SUB AX,DX
202c:3229  MOV DX,AX
202c:322b  IMUL AX,word ptr [BP + -0x2],0xe
202c:322f  LES DI,[0x6698]
202c:3233  ADD DI,AX
202c:3235  MOV AX,word ptr ES:[DI + -0xe]
202c:3239  CMP AX,DX
202c:323b  JG 0x2000:3500
202c:323d  JMP 0x2000:35a4
202c:3240  MOV AL,byte ptr [BP + -0x23]
202c:3243  XOR AH,AH
202c:3245  MOV DI,AX
202c:3247  MOV AL,byte ptr [DI + 0x13d7]
202c:324b  XOR AH,AH
202c:324d  ADD AX,word ptr [BP + 0x8]
202c:3250  MOV DX,AX
202c:3252  IMUL AX,word ptr [BP + -0x2],0xe
202c:3256  LES DI,[0x6698]
202c:325a  ADD DI,AX
202c:325c  MOV AX,word ptr ES:[DI + -0xe]
202c:3260  CMP AX,DX
202c:3262  JL 0x2000:3527
202c:3264  JMP 0x2000:35a4
202c:3267  MOV AL,byte ptr [BP + -0x23]
202c:326a  XOR AH,AH
202c:326c  MOV DI,AX
202c:326e  MOV AL,byte ptr [DI + 0x13d7]
202c:3272  XOR AH,AH
202c:3274  MOV DX,AX
202c:3276  MOV AX,word ptr [BP + 0x6]
202c:3279  SUB AX,DX
202c:327b  MOV DX,AX
202c:327d  IMUL AX,word ptr [BP + -0x2],0xe
202c:3281  LES DI,[0x6698]
202c:3285  ADD DI,AX
202c:3287  MOV AX,word ptr ES:[DI + -0xa]
202c:328b  CMP AX,DX
202c:328d  JLE 0x2000:35a4
202c:328f  MOV AL,byte ptr [BP + -0x23]
202c:3292  XOR AH,AH
202c:3294  MOV DI,AX
202c:3296  MOV AL,byte ptr [DI + 0x13d7]
202c:329a  XOR AH,AH
202c:329c  ADD AX,word ptr [BP + 0x6]
202c:329f  MOV DX,AX
202c:32a1  IMUL AX,word ptr [BP + -0x2],0xe
202c:32a5  LES DI,[0x6698]
202c:32a9  ADD DI,AX
202c:32ab  MOV AX,word ptr ES:[DI + -0xa]
202c:32af  CMP AX,DX
202c:32b1  JGE 0x2000:35a4
202c:32b3  IMUL AX,word ptr [BP + -0x2],0xe
202c:32b7  LES DI,[0x6698]
202c:32bb  ADD DI,AX
202c:32bd  MOV byte ptr ES:[DI + -0x2],0x0
202c:32c2  PUSH 0x1
202c:32c4  IMUL AX,word ptr [BP + -0x2],0xe
202c:32c8  LES DI,[0x6698]
202c:32cc  ADD DI,AX
202c:32ce  PUSH word ptr ES:[DI + -0xe]
202c:32d2  IMUL AX,word ptr [BP + -0x2],0xe
202c:32d6  LES DI,[0x6698]
202c:32da  ADD DI,AX
202c:32dc  PUSH word ptr ES:[DI + -0xa]
202c:32e0  PUSH CS
202c:32e1  CALL 0x2000:1e44
202c:32e4  MOV AX,word ptr [BP + -0x2]
202c:32e7  CMP AX,word ptr [BP + -0x26]
202c:32ea  JZ 0x2000:35af
202c:32ec  JMP 0x2000:34be
202c:32ef  LEAVE
202c:32f0  RETF 0x6
