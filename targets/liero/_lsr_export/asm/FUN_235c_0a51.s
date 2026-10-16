; FUN_235c_0a51  entry=235c:0a51 size=92
235c:0a51  ENTER 0x2,0x0
235c:0a55  MOV byte ptr [BP + -0x1],0x0
235c:0a59  JMP 0x2000:401e
235c:0a5b  INC byte ptr [BP + -0x1]
235c:0a5e  MOV AL,byte ptr [BP + -0x1]
235c:0a61  XOR AH,AH
235c:0a63  MOV DI,AX
235c:0a65  CMP byte ptr [DI + 0x67fc],0x0
235c:0a6a  JZ 0x2000:4065
235c:0a6c  MOV AL,byte ptr [BP + -0x1]
235c:0a6f  XOR AH,AH
235c:0a71  IMUL DI,AX,0xa
235c:0a74  LES DI,[DI + 0x6804]
235c:0a78  MOV CX,word ptr ES:[DI + 0x6]
235c:0a7c  MOV BX,word ptr ES:[DI + 0x8]
235c:0a80  MOV AL,byte ptr [BP + -0x1]
235c:0a83  XOR AH,AH
235c:0a85  IMUL DI,AX,0xa
235c:0a88  MOV AX,word ptr [DI + 0x6809]
235c:0a8c  MOV DX,word ptr [DI + 0x680b]
235c:0a90  CMP DX,BX
235c:0a92  JG 0x2000:405a
235c:0a94  JL 0x2000:4065
235c:0a96  CMP AX,CX
235c:0a98  JC 0x2000:4065
235c:0a9a  MOV AL,byte ptr [BP + -0x1]
235c:0a9d  PUSH AX
235c:0a9e  CALL 0x2000:3edd
235c:0aa1  DEC byte ptr [0x67ce]
235c:0aa5  CMP byte ptr [BP + -0x1],0x7
235c:0aa9  JNZ 0x2000:401b
235c:0aab  LEAVE
235c:0aac  RET
