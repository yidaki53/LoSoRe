; FUN_1ea2_0104  entry=1ea2:0104 size=164
1ea2:0104  ENTER 0x6,0x0
1ea2:0108  MOV byte ptr [BP + -0x1],0x0
1ea2:010c  CMP byte ptr [0x65ee],0x0
1ea2:0111  JGE 0x1000:eb36
1ea2:0113  JMP 0x1000:ebc1
1ea2:0116  MOV AL,[0x65ee]
1ea2:0119  CBW
1ea2:011a  MOV DI,AX
1ea2:011c  SHL DI,0x1
1ea2:011e  MOV AX,word ptr [DI + 0x65e8]
1ea2:0122  DEC AX
1ea2:0123  MOV word ptr [BP + -0x6],AX
1ea2:0126  XOR AX,AX
1ea2:0128  CMP AX,word ptr [BP + -0x6]
1ea2:012b  JA 0x1000:eb9a
1ea2:012d  MOV word ptr [BP + -0x4],AX
1ea2:0130  JMP 0x1000:eb55
1ea2:0132  INC word ptr [BP + -0x4]
1ea2:0135  MOV AX,word ptr [BP + -0x4]
1ea2:0138  SHL AX,0x2
1ea2:013b  LES DI,[BP + 0x6]
1ea2:013e  LES DI,ES:[DI]
1ea2:0141  ADD DI,AX
1ea2:0143  MOV AX,word ptr ES:[DI]
1ea2:0146  OR AX,word ptr ES:[DI + 0x2]
1ea2:014a  JZ 0x1000:eb92
1ea2:014c  MOV AX,word ptr [BP + -0x4]
1ea2:014f  SHL AX,0x2
1ea2:0152  LES DI,[BP + 0x6]
1ea2:0155  LES DI,ES:[DI]
1ea2:0158  ADD DI,AX
1ea2:015a  PUSH word ptr ES:[DI + 0x2]
1ea2:015e  PUSH word ptr ES:[DI]
1ea2:0161  MOV AL,[0x65ee]
1ea2:0164  CBW
1ea2:0165  MOV DI,AX
1ea2:0167  SHL DI,0x1
1ea2:0169  PUSH word ptr [DI + 0x65e2]
1ea2:016d  CALLF 0x2000:506f
1ea2:0172  MOV AX,word ptr [BP + -0x4]
1ea2:0175  CMP AX,word ptr [BP + -0x6]
1ea2:0178  JNZ 0x1000:eb52
1ea2:017a  LES DI,[BP + 0x6]
1ea2:017d  PUSH word ptr ES:[DI + 0x2]
1ea2:0181  PUSH word ptr ES:[DI]
1ea2:0184  MOV AL,[0x65ee]
1ea2:0187  CBW
1ea2:0188  MOV DI,AX
1ea2:018a  SHL DI,0x1
1ea2:018c  MOV AX,word ptr [DI + 0x65e8]
1ea2:0190  SHL AX,0x2
1ea2:0193  PUSH AX
1ea2:0194  CALLF 0x2000:506f
1ea2:0199  DEC byte ptr [0x65ee]
1ea2:019d  MOV byte ptr [BP + -0x1],0x1
1ea2:01a1  MOV AL,byte ptr [BP + -0x1]
1ea2:01a4  LEAVE
1ea2:01a5  RETF 0x4
