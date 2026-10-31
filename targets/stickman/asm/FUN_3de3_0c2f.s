; FUN_3de3_0c2f  entry=3de3:0c2f size=68
3de3:0c2f  PUSH BP
3de3:0c30  MOV BP,SP
3de3:0c32  MOV AX,0x4
3de3:0c35  CALLF 0x4000:302f
3de3:0c3a  SUB SP,0x4
3de3:0c3d  MOV AX,word ptr [BP + 0x6]
3de3:0c40  MOV word ptr [BP + -0x4],AX
3de3:0c43  MOV AX,0x1
3de3:0c46  CMP AX,word ptr [BP + -0x4]
3de3:0c49  JG 0x3000:ea9d
3de3:0c4b  MOV word ptr [BP + -0x2],AX
3de3:0c4e  JMP 0x3000:ea83
3de3:0c50  INC word ptr [BP + -0x2]
3de3:0c53  MOV DI,0xc27
3de3:0c56  PUSH CS
3de3:0c57  PUSH DI
3de3:0c58  PUSH CS
3de3:0c59  CALL 0x3000:de5d
3de3:0c5c  MOV AX,0x32
3de3:0c5f  PUSH AX
3de3:0c60  CALLF 0x4000:137c
3de3:0c65  MOV AX,word ptr [BP + -0x2]
3de3:0c68  CMP AX,word ptr [BP + -0x4]
3de3:0c6b  JNZ 0x3000:ea80
3de3:0c6d  MOV SP,BP
3de3:0c6f  POP BP
3de3:0c70  RETF 0x2
