; FUN_235c_0a1e  entry=235c:0a1e size=51
235c:0a1e  ENTER 0x2,0x0
235c:0a22  MOV byte ptr [BP + -0x1],0x0
235c:0a26  MOV byte ptr [BP + -0x2],0x0
235c:0a2a  JMP 0x2000:3fef
235c:0a2c  INC byte ptr [BP + -0x2]
235c:0a2f  MOV AL,byte ptr [BP + -0x2]
235c:0a32  XOR AH,AH
235c:0a34  IMUL DI,AX,0xa
235c:0a37  MOV AL,byte ptr [DI + 0x6808]
235c:0a3b  CMP AL,byte ptr [BP + 0x6]
235c:0a3e  JNZ 0x2000:4004
235c:0a40  MOV byte ptr [BP + -0x1],0x1
235c:0a44  CMP byte ptr [BP + -0x2],0x7
235c:0a48  JNZ 0x2000:3fec
235c:0a4a  MOV AL,byte ptr [BP + -0x1]
235c:0a4d  LEAVE
235c:0a4e  RETF 0x2
