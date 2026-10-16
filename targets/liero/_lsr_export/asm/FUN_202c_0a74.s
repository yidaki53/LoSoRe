; FUN_202c_0a74  entry=202c:0a74 size=154
202c:0a74  ENTER 0xa,0x0
202c:0a78  MOV byte ptr [BP + -0x1],0x0
202c:0a7c  MOV AX,word ptr [BP + 0x8]
202c:0a7f  ADD AX,word ptr [BP + 0x4]
202c:0a82  MOV word ptr [BP + -0x8],AX
202c:0a85  MOV AX,word ptr [BP + 0x8]
202c:0a88  CMP AX,word ptr [BP + -0x8]
202c:0a8b  JG 0x2000:0dc3
202c:0a8d  MOV word ptr [BP + -0x4],AX
202c:0a90  JMP 0x2000:0d55
202c:0a92  INC word ptr [BP + -0x4]
202c:0a95  MOV AX,word ptr [BP + 0x6]
202c:0a98  ADD AX,word ptr [BP + 0x4]
202c:0a9b  MOV word ptr [BP + -0xa],AX
202c:0a9e  MOV AX,word ptr [BP + 0x6]
202c:0aa1  CMP AX,word ptr [BP + -0xa]
202c:0aa4  JG 0x2000:0dbb
202c:0aa6  MOV word ptr [BP + -0x6],AX
202c:0aa9  JMP 0x2000:0d6e
202c:0aab  INC word ptr [BP + -0x6]
202c:0aae  MOV DX,word ptr [BP + -0x4]
202c:0ab1  MOV AX,word ptr [BP + -0x6]
202c:0ab4  SHL AX,0x2
202c:0ab7  LES DI,[0x6674]
202c:0abb  ADD DI,AX
202c:0abd  LES DI,ES:[DI]
202c:0ac0  ADD DI,DX
202c:0ac2  MOV AL,byte ptr ES:[DI]
202c:0ac5  MOV AH,0x1
202c:0ac7  MOV DX,0x20
202c:0aca  CALLF 0x2000:8f31
202c:0acf  MOV DI,DX
202c:0ad1  TEST byte ptr [DI + 0x14a0],AL
202c:0ad5  JZ 0x2000:0db3
202c:0ad7  CMP word ptr [BP + -0x6],-0x1
202c:0adb  JLE 0x2000:0db3
202c:0add  CMP word ptr [BP + -0x6],0x15e
202c:0ae2  JGE 0x2000:0db3
202c:0ae4  CMP word ptr [BP + -0x4],-0x1
202c:0ae8  JLE 0x2000:0db3
202c:0aea  CMP word ptr [BP + -0x4],0x1f8
202c:0aef  JGE 0x2000:0db3
202c:0af1  JMP 0x2000:0dc7
202c:0af3  MOV AX,word ptr [BP + -0x6]
202c:0af6  CMP AX,word ptr [BP + -0xa]
202c:0af9  JNZ 0x2000:0d6b
202c:0afb  MOV AX,word ptr [BP + -0x4]
202c:0afe  CMP AX,word ptr [BP + -0x8]
202c:0b01  JNZ 0x2000:0d52
202c:0b03  MOV byte ptr [BP + -0x1],0x1
202c:0b07  MOV AL,byte ptr [BP + -0x1]
202c:0b0a  LEAVE
202c:0b0b  RET 0x6
