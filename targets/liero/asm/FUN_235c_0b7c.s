; FUN_235c_0b7c  entry=235c:0b7c size=64
235c:0b7c  ENTER 0x4,0x0
235c:0b80  MOV word ptr [BP + -0x2],0xfc00
235c:0b85  JMP 0x2000:414a
235c:0b87  INC word ptr [BP + -0x2]
235c:0b8a  MOV AX,word ptr [BP + -0x2]
235c:0b8d  MOV word ptr [BP + -0x4],AX
235c:0b90  CMP word ptr [BP + -0x4],-0x80
235c:0b94  JGE 0x2000:415b
235c:0b96  MOV word ptr [BP + -0x4],0xff80
235c:0b9b  CMP word ptr [BP + -0x4],0x7f
235c:0b9f  JLE 0x2000:4166
235c:0ba1  MOV word ptr [BP + -0x4],0x7f
235c:0ba6  MOV AX,word ptr [BP + -0x4]
235c:0ba9  ADD AX,0x80
235c:0bac  MOV DI,word ptr [BP + -0x2]
235c:0baf  MOV byte ptr [DI + 0x7286],AL
235c:0bb3  CMP word ptr [BP + -0x2],0x400
235c:0bb8  JNZ 0x2000:4147
235c:0bba  LEAVE
235c:0bbb  RET
