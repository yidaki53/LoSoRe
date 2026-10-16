; FUN_235c_095c  entry=235c:095c size=143
235c:095c  ENTER 0x2,0x0
235c:0960  MOV byte ptr [BP + -0x2],0xff
235c:0964  MOV byte ptr [BP + -0x1],0x0
235c:0968  MOV AL,byte ptr [BP + -0x1]
235c:096b  XOR AH,AH
235c:096d  MOV DI,AX
235c:096f  CMP byte ptr [DI + 0x67fc],0x0
235c:0974  JNZ 0x2000:3f3c
235c:0976  MOV AL,byte ptr [BP + -0x1]
235c:0979  MOV byte ptr [BP + -0x2],AL
235c:097c  INC byte ptr [BP + -0x1]
235c:097f  CMP byte ptr [BP + -0x2],0xff
235c:0983  JNZ 0x2000:3f4b
235c:0985  CMP byte ptr [BP + -0x1],0x8
235c:0989  JNZ 0x2000:3f28
235c:098b  CMP byte ptr [BP + -0x2],0xff
235c:098f  JZ 0x2000:3fa7
235c:0991  INC byte ptr [0x67ce]
235c:0995  MOV CX,word ptr [BP + 0xa]
235c:0998  MOV BX,word ptr [BP + 0xc]
235c:099b  MOV AL,byte ptr [BP + -0x2]
235c:099e  XOR AH,AH
235c:09a0  IMUL DI,AX,0xa
235c:09a3  MOV word ptr [DI + 0x6804],CX
235c:09a7  MOV word ptr [DI + 0x6806],BX
235c:09ab  MOV DL,byte ptr [BP + 0x8]
235c:09ae  MOV AL,byte ptr [BP + -0x2]
235c:09b1  XOR AH,AH
235c:09b3  IMUL DI,AX,0xa
235c:09b6  MOV byte ptr [DI + 0x6808],DL
235c:09ba  MOV AL,byte ptr [BP + -0x2]
235c:09bd  XOR AH,AH
235c:09bf  IMUL DI,AX,0xa
235c:09c2  XOR AX,AX
235c:09c4  MOV word ptr [DI + 0x6809],AX
235c:09c8  MOV word ptr [DI + 0x680b],AX
235c:09cc  MOV DL,byte ptr [BP + 0x6]
235c:09cf  MOV AL,byte ptr [BP + -0x2]
235c:09d2  XOR AH,AH
235c:09d4  IMUL DI,AX,0xa
235c:09d7  MOV byte ptr [DI + 0x680d],DL
235c:09db  MOV AL,byte ptr [BP + -0x2]
235c:09de  XOR AH,AH
235c:09e0  MOV DI,AX
235c:09e2  MOV byte ptr [DI + 0x67fc],0x1
235c:09e7  LEAVE
235c:09e8  RETF 0x8
