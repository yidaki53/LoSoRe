; FUN_235c_0aad  entry=235c:0aad size=38
235c:0aad  PUSH BP
235c:0aae  MOV BP,SP
235c:0ab0  MOV AL,byte ptr [BP + 0x4]
235c:0ab3  MOV [0x6854],AL
235c:0ab6  MOV AL,byte ptr [BP + 0x4]
235c:0ab9  XOR AH,AH
235c:0abb  MOV DI,AX
235c:0abd  SHL DI,0x2
235c:0ac0  MOV AX,word ptr [DI + 0x6e60]
235c:0ac4  MOV DX,word ptr [DI + 0x6e62]
235c:0ac8  MOV [0x6e6c],AX
235c:0acb  MOV word ptr [0x6e6e],DX
235c:0acf  LEAVE
235c:0ad0  RET 0x2
