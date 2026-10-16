; FUN_24dd_18d9  entry=24dd:18d9 size=243
24dd:18d9  PUSH BP
24dd:18da  MOV BP,SP
24dd:18dc  PUSH SI
24dd:18dd  PUSH DI
24dd:18de  PUSH DS
24dd:18df  PUSH ES
24dd:18e0  MOV AL,0xc
24dd:18e2  MUL byte ptr [BP + 0x6]
24dd:18e5  SUB AX,0xc
24dd:18e8  XCHG AX,SI
24dd:18e9  ADD SI,word ptr [BP + 0x4]
24dd:18ec  CALL 0x2000:5412
24dd:18ef  MOV DI,SI
24dd:18f1  DEC byte ptr [BP + 0x6]
24dd:18f4  JLE 0x2000:6744
24dd:18f6  PUSH DI
24dd:18f7  MOV DI,word ptr [0xd8]
24dd:18fb  MOV AL,byte ptr [DI + 0x16]
24dd:18fe  XOR byte ptr [DI + 0xa],AL
24dd:1901  CALL 0x2000:5f60
24dd:1904  MOV word ptr [DI],AX
24dd:1906  MOV word ptr [DI + 0x2],BX
24dd:1909  MOV word ptr [DI + 0x4],CX
24dd:190c  MOV word ptr [DI + 0x6],DX
24dd:190f  POP DI
24dd:1910  SUB DI,0xc
24dd:1913  PUSH BP
24dd:1914  MOV BP,word ptr [0xd8]
24dd:1918  MOV BX,word ptr CS:[DI]
24dd:191b  MOV CX,word ptr CS:[DI + 0x2]
24dd:191f  MOV DX,word ptr CS:[DI + 0x4]
24dd:1923  MOV SI,word ptr CS:[DI + 0x6]
24dd:1927  MOV AL,byte ptr CS:[DI + 0xa]
24dd:192b  CMP AL,byte ptr [BP + 0xa]
24dd:192e  JZ 0x2000:6734
24dd:1930  SUB BX,word ptr [BP + 0x0]
24dd:1933  SBB CX,word ptr [BP + 0x2]
24dd:1936  SBB DX,word ptr [BP + 0x4]
24dd:1939  SBB SI,word ptr [BP + 0x6]
24dd:193c  JNC 0x2000:6722
24dd:193e  NOT SI
24dd:1940  NOT DX
24dd:1942  NOT CX
24dd:1944  NEG BX
24dd:1946  CMC
24dd:1947  ADC CX,0x0
24dd:194a  ADC DX,0x0
24dd:194d  ADC SI,0x0
24dd:1950  XOR AL,0x1
24dd:1952  MOV word ptr [BP + 0x0],BX
24dd:1955  MOV word ptr [BP + 0x2],CX
24dd:1958  MOV word ptr [BP + 0x4],DX
24dd:195b  MOV word ptr [BP + 0x6],SI
24dd:195e  MOV byte ptr [BP + 0xa],AL
24dd:1961  POP BP
24dd:1962  JMP 0x2000:66c1
24dd:1964  ADD word ptr [BP + 0x0],BX
24dd:1967  ADC word ptr [BP + 0x2],CX
24dd:196a  ADC word ptr [BP + 0x4],DX
24dd:196d  ADC word ptr [BP + 0x6],SI
24dd:1970  POP BP
24dd:1971  JMP 0x2000:66c1
24dd:1974  MOV SI,word ptr [0xd8]
24dd:1978  CLD
24dd:1979  LODSW SI
24dd:197a  XCHG AX,BX
24dd:197b  LODSW SI
24dd:197c  XCHG AX,CX
24dd:197d  LODSW SI
24dd:197e  XCHG AX,DX
24dd:197f  LODSW SI
24dd:1980  XCHG AX,DI
24dd:1981  LODSW SI
24dd:1982  LODSW SI
24dd:1983  MOV word ptr [0xd8],SI
24dd:1987  XCHG DI,SI
24dd:1989  SUB DI,DI
24dd:198b  CMP AL,0x1
24dd:198d  JNZ 0x2000:6770
24dd:198f  NOT SI
24dd:1991  NOT DX
24dd:1993  NOT CX
24dd:1995  NEG BX
24dd:1997  CMC
24dd:1998  ADC CX,DI
24dd:199a  ADC DX,DI
24dd:199c  ADC SI,DI
24dd:199e  JMP 0x2000:6782
24dd:19a0  STC
24dd:19a1  RCR SI,0x1
24dd:19a3  RCR DX,0x1
24dd:19a5  RCR CX,0x1
24dd:19a7  RCR BX,0x1
24dd:19a9  ADC BX,DI
24dd:19ab  ADC CX,DI
24dd:19ad  ADC DX,DI
24dd:19af  ADC SI,DI
24dd:19b1  INC DI
24dd:19b2  MOV AX,[0xd8]
24dd:19b5  XCHG AX,DI
24dd:19b6  XCHG AX,BX
24dd:19b7  STOSW ES:DI
24dd:19b8  XCHG AX,CX
24dd:19b9  STOSW ES:DI
24dd:19ba  XCHG AX,DX
24dd:19bb  STOSW ES:DI
24dd:19bc  XCHG AX,SI
24dd:19bd  STOSW ES:DI
24dd:19be  XCHG AX,BX
24dd:19bf  STOSW ES:DI
24dd:19c0  MOV AX,0x0
24dd:19c3  STOSW ES:DI
24dd:19c4  POP ES
24dd:19c5  POP DS
24dd:19c6  POP DI
24dd:19c7  POP SI
24dd:19c8  POP BP
24dd:19c9  RET 0x4
