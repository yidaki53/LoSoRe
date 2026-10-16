; FUN_235c_06d7  entry=235c:06d7 size=58
235c:06d7  ENTER 0x4,0x0
235c:06db  MOV AX,word ptr [BP + 0x8]
235c:06de  MOV DX,word ptr [BP + 0xa]
235c:06e1  CMP DX,word ptr [BP + 0x6]
235c:06e4  JL 0x2000:3cad
235c:06e6  JG 0x2000:3cbb
235c:06e8  CMP AX,word ptr [BP + 0x4]
235c:06eb  JNC 0x2000:3cbb
235c:06ed  MOV AX,word ptr [BP + 0x8]
235c:06f0  MOV DX,word ptr [BP + 0xa]
235c:06f3  MOV word ptr [BP + -0x4],AX
235c:06f6  MOV word ptr [BP + -0x2],DX
235c:06f9  JMP 0x2000:3cc7
235c:06fb  MOV AX,word ptr [BP + 0x4]
235c:06fe  MOV DX,word ptr [BP + 0x6]
235c:0701  MOV word ptr [BP + -0x4],AX
235c:0704  MOV word ptr [BP + -0x2],DX
235c:0707  MOV AX,word ptr [BP + -0x4]
235c:070a  MOV DX,word ptr [BP + -0x2]
235c:070d  LEAVE
235c:070e  RET 0x8
