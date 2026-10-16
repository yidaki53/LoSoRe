; FUN_249c_019d  entry=249c:019d size=38
249c:019d  ENTER 0x2,0x0
249c:01a1  MOV AH,0x7
249c:01a3  INT 0x21
249c:01a5  MOV byte ptr [BP + 0xfffe],AL
249c:01a9  CMP byte ptr [0x159c],0x0
249c:01ae  JZ 0x2000:4b78
249c:01b0  CMP byte ptr [BP + -0x2],0x3
249c:01b4  JNZ 0x2000:4b78
249c:01b6  INT 0x23
249c:01b8  MOV AL,byte ptr [BP + -0x2]
249c:01bb  MOV byte ptr [BP + -0x1],AL
249c:01be  MOV AL,byte ptr [BP + -0x1]
249c:01c1  LEAVE
249c:01c2  RETF
