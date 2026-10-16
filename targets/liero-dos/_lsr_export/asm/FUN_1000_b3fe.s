; FUN_1000_b3fe  entry=1000:b3fe size=96
1000:b3fe  PUSH BP
1000:b3ff  MOV BP,SP
1000:b401  MOV AX,0x4
1000:b404  CALLF 0x2000:5300
1000:b409  SUB SP,0x4
1000:b40c  MOV word ptr [BP + -0x3],0x1
1000:b411  JMP 0x1000:b416
1000:b413  INC word ptr [BP + -0x3]
1000:b416  MOV DI,word ptr [BP + -0x3]
1000:b419  MOV byte ptr [DI + 0x783b],0x0
1000:b41e  CMP word ptr [BP + -0x3],0xab
1000:b423  JNZ 0x1000:b413
1000:b425  CALLF 0x2000:4c78
1000:b42a  OR AL,AL
1000:b42c  JZ 0x1000:b425
1000:b42e  MOV word ptr [BP + -0x3],0x1
1000:b433  JMP 0x1000:b438
1000:b435  INC word ptr [BP + -0x3]
1000:b438  MOV DI,word ptr [BP + -0x3]
1000:b43b  CMP byte ptr [DI + 0x783b],0x0
1000:b440  JZ 0x1000:b450
1000:b442  MOV AL,byte ptr [BP + -0x3]
1000:b445  MOV byte ptr [BP + -0x1],AL
1000:b448  MOV DI,word ptr [BP + -0x3]
1000:b44b  MOV byte ptr [DI + 0x783b],0x0
1000:b450  CMP word ptr [BP + -0x3],0xab
1000:b455  JNZ 0x1000:b435
1000:b457  MOV AL,byte ptr [BP + -0x1]
1000:b45a  LEAVE
1000:b45b  RET 0x2
