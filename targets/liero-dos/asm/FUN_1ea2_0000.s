; FUN_1ea2_0000  entry=1ea2:0000 size=260
1ea2:0000  ENTER 0xa,0x0
1ea2:0004  MOV byte ptr [BP + -0x1],0x0
1ea2:0008  CMP byte ptr [0x65ee],0x2
1ea2:000d  JLE 0x1000:ea32
1ea2:000f  JMP 0x1000:eb1d
1ea2:0012  MOV DX,word ptr [BP + 0x8]
1ea2:0015  MOV AL,[0x65ee]
1ea2:0018  CBW
1ea2:0019  MOV DI,AX
1ea2:001b  SHL DI,0x1
1ea2:001d  MOV word ptr [DI + 0x65e2],DX
1ea2:0021  MOV DX,word ptr [BP + 0x6]
1ea2:0024  MOV AL,[0x65ee]
1ea2:0027  CBW
1ea2:0028  MOV DI,AX
1ea2:002a  SHL DI,0x1
1ea2:002c  MOV word ptr [DI + 0x65e8],DX
1ea2:0030  CALLF 0x2000:50d3
1ea2:0035  MOV CX,AX
1ea2:0037  MOV BX,DX
1ea2:0039  MOV AL,[0x65ee]
1ea2:003c  CBW
1ea2:003d  MOV DI,AX
1ea2:003f  SHL DI,0x1
1ea2:0041  MOV DX,word ptr [DI + 0x65e8]
1ea2:0045  MOV AL,[0x65ee]
1ea2:0048  CBW
1ea2:0049  MOV DI,AX
1ea2:004b  SHL DI,0x1
1ea2:004d  MOV AX,word ptr [DI + 0x65e2]
1ea2:0051  MUL DX
1ea2:0053  XOR DX,DX
1ea2:0055  CMP DX,BX
1ea2:0057  JG 0x1000:ea7f
1ea2:0059  JL 0x1000:ea82
1ea2:005b  CMP AX,CX
1ea2:005d  JBE 0x1000:ea82
1ea2:005f  JMP 0x1000:eb1d
1ea2:0062  MOV AL,[0x65ee]
1ea2:0065  CBW
1ea2:0066  MOV DI,AX
1ea2:0068  SHL DI,0x1
1ea2:006a  MOV AX,word ptr [DI + 0x65e8]
1ea2:006e  SHL AX,0x2
1ea2:0071  PUSH AX
1ea2:0072  CALLF 0x2000:505a
1ea2:0077  LES DI,[BP + 0xa]
1ea2:007a  MOV word ptr ES:[DI],AX
1ea2:007d  MOV word ptr ES:[DI + 0x2],DX
1ea2:0081  MOV AL,[0x65ee]
1ea2:0084  CBW
1ea2:0085  MOV DI,AX
1ea2:0087  SHL DI,0x1
1ea2:0089  MOV AX,word ptr [DI + 0x65e8]
1ea2:008d  DEC AX
1ea2:008e  MOV word ptr [BP + -0xa],AX
1ea2:0091  XOR AX,AX
1ea2:0093  CMP AX,word ptr [BP + -0xa]
1ea2:0096  JA 0x1000:eb15
1ea2:0098  MOV word ptr [BP + -0x4],AX
1ea2:009b  JMP 0x1000:eac0
1ea2:009d  INC word ptr [BP + -0x4]
1ea2:00a0  CALLF 0x2000:50d3
1ea2:00a5  MOV CX,AX
1ea2:00a7  MOV BX,DX
1ea2:00a9  MOV AL,[0x65ee]
1ea2:00ac  CBW
1ea2:00ad  MOV DI,AX
1ea2:00af  SHL DI,0x1
1ea2:00b1  MOV AX,word ptr [DI + 0x65e2]
1ea2:00b5  XOR DX,DX
1ea2:00b7  CMP DX,BX
1ea2:00b9  JG 0x1000:eae1
1ea2:00bb  JL 0x1000:eae3
1ea2:00bd  CMP AX,CX
1ea2:00bf  JBE 0x1000:eae3
1ea2:00c1  JMP 0x1000:eb1d
1ea2:00c3  MOV AL,[0x65ee]
1ea2:00c6  CBW
1ea2:00c7  MOV DI,AX
1ea2:00c9  SHL DI,0x1
1ea2:00cb  PUSH word ptr [DI + 0x65e2]
1ea2:00cf  CALLF 0x2000:505a
1ea2:00d4  MOV CX,AX
1ea2:00d6  MOV BX,DX
1ea2:00d8  MOV AX,word ptr [BP + -0x4]
1ea2:00db  SHL AX,0x2
1ea2:00de  LES DI,[BP + 0xa]
1ea2:00e1  LES DI,ES:[DI]
1ea2:00e4  ADD DI,AX
1ea2:00e6  MOV word ptr ES:[DI],CX
1ea2:00e9  MOV word ptr ES:[DI + 0x2],BX
1ea2:00ed  MOV AX,word ptr [BP + -0x4]
1ea2:00f0  CMP AX,word ptr [BP + -0xa]
1ea2:00f3  JNZ 0x1000:eabd
1ea2:00f5  INC byte ptr [0x65ee]
1ea2:00f9  MOV byte ptr [BP + -0x1],0x1
1ea2:00fd  MOV AL,byte ptr [BP + -0x1]
1ea2:0100  LEAVE
1ea2:0101  RETF 0x8
