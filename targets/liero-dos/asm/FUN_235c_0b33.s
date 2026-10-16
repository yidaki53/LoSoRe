; FUN_235c_0b33  entry=235c:0b33 size=73
235c:0b33  ENTER 0x8,0x0
235c:0b37  PUSH word ptr [BP + 0x6]
235c:0b3a  PUSH word ptr [BP + 0x4]
235c:0b3d  CALL 0x2000:40bf
235c:0b40  MOV word ptr [BP + -0x8],AX
235c:0b43  MOV word ptr [BP + -0x6],DX
235c:0b46  MOV AX,word ptr [BP + -0x8]
235c:0b49  MOV DX,word ptr [BP + -0x6]
235c:0b4c  MOV CX,0x10
235c:0b4f  XOR BX,BX
235c:0b51  CALLF 0x2000:8b8d
235c:0b56  PUSH AX
235c:0b57  MOV AX,word ptr [BP + -0x8]
235c:0b5a  MOV DX,word ptr [BP + -0x6]
235c:0b5d  MOV CX,0x10
235c:0b60  XOR BX,BX
235c:0b62  CALLF 0x2000:8b8d
235c:0b67  MOV AX,CX
235c:0b69  MOV DX,BX
235c:0b6b  POP DX
235c:0b6c  MOV word ptr [BP + -0x4],AX
235c:0b6f  MOV word ptr [BP + -0x2],DX
235c:0b72  MOV AX,word ptr [BP + -0x4]
235c:0b75  MOV DX,word ptr [BP + -0x2]
235c:0b78  LEAVE
235c:0b79  RET 0x4
