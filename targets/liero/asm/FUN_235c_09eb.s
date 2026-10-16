; FUN_235c_09eb  entry=235c:09eb size=51
235c:09eb  ENTER 0x2,0x0
235c:09ef  MOV byte ptr [BP + -0x1],0x0
235c:09f3  JMP 0x2000:3fb8
235c:09f5  INC byte ptr [BP + -0x1]
235c:09f8  MOV AL,byte ptr [BP + -0x1]
235c:09fb  XOR AH,AH
235c:09fd  IMUL DI,AX,0xa
235c:0a00  MOV AL,byte ptr [DI + 0x6808]
235c:0a04  CMP AL,byte ptr [BP + 0x6]
235c:0a07  JNZ 0x2000:3fd4
235c:0a09  MOV AL,byte ptr [BP + -0x1]
235c:0a0c  PUSH AX
235c:0a0d  CALL 0x2000:3edd
235c:0a10  DEC byte ptr [0x67ce]
235c:0a14  CMP byte ptr [BP + -0x1],0x7
235c:0a18  JNZ 0x2000:3fb5
235c:0a1a  LEAVE
235c:0a1b  RETF 0x2
