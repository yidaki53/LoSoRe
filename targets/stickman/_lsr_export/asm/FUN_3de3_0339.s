; FUN_3de3_0339  entry=3de3:0339 size=174
3de3:0339  PUSH BP
3de3:033a  MOV BP,SP
3de3:033c  MOV AX,0x2
3de3:033f  CALLF 0x4000:302f
3de3:0344  SUB SP,0x2
3de3:0347  CALLF 0x4000:0a10
3de3:034c  MOV byte ptr [BP + -0x2],AL
3de3:034f  CMP byte ptr [BP + -0x2],0x0
3de3:0353  JNZ 0x3000:e1fe
3de3:0355  CALLF 0x4000:0a10
3de3:035a  CMP AL,0x23
3de3:035c  JNZ 0x3000:e1a8
3de3:035e  CALLF 0x4000:09e0
3de3:0363  CALLF 0x4000:09b9
3de3:0368  XOR AX,AX
3de3:036a  MOV [0xaaec],AX
3de3:036d  MOV DI,0x325
3de3:0370  PUSH CS
3de3:0371  PUSH DI
3de3:0372  PUSH CS
3de3:0373  CALL 0x3000:e0a8
3de3:0376  JMP 0x3000:e1fc
3de3:0378  CMP AL,0x50
3de3:037a  JNZ 0x3000:e1b2
3de3:037c  MOV byte ptr [BP + -0x1],0x32
3de3:0380  JMP 0x3000:e1fc
3de3:0382  CMP AL,0x4b
3de3:0384  JNZ 0x3000:e1bc
3de3:0386  MOV byte ptr [BP + -0x1],0x34
3de3:038a  JMP 0x3000:e1fc
3de3:038c  CMP AL,0x4d
3de3:038e  JNZ 0x3000:e1c6
3de3:0390  MOV byte ptr [BP + -0x1],0x36
3de3:0394  JMP 0x3000:e1fc
3de3:0396  CMP AL,0x48
3de3:0398  JNZ 0x3000:e1d0
3de3:039a  MOV byte ptr [BP + -0x1],0x38
3de3:039e  JMP 0x3000:e1fc
3de3:03a0  CMP AL,0x4f
3de3:03a2  JNZ 0x3000:e1da
3de3:03a4  MOV byte ptr [BP + -0x1],0x31
3de3:03a8  JMP 0x3000:e1fc
3de3:03aa  CMP AL,0x51
3de3:03ac  JNZ 0x3000:e1e4
3de3:03ae  MOV byte ptr [BP + -0x1],0x33
3de3:03b2  JMP 0x3000:e1fc
3de3:03b4  CMP AL,0x47
3de3:03b6  JNZ 0x3000:e1ee
3de3:03b8  MOV byte ptr [BP + -0x1],0x37
3de3:03bc  JMP 0x3000:e1fc
3de3:03be  CMP AL,0x49
3de3:03c0  JNZ 0x3000:e1f8
3de3:03c2  MOV byte ptr [BP + -0x1],0x39
3de3:03c6  JMP 0x3000:e1fc
3de3:03c8  MOV byte ptr [BP + -0x1],0x7e
3de3:03cc  JMP 0x3000:e204
3de3:03ce  MOV AL,byte ptr [BP + -0x2]
3de3:03d1  MOV byte ptr [BP + -0x1],AL
3de3:03d4  CALLF 0x4000:1796
3de3:03d9  MOV [0xa7d2],AX
3de3:03dc  MOV word ptr [0xa7d4],DX
3de3:03e0  MOV AL,byte ptr [BP + -0x1]
3de3:03e3  MOV SP,BP
3de3:03e5  POP BP
3de3:03e6  RETF
