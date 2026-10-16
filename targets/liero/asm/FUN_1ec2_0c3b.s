; FUN_1ec2_0c3b  entry=1ec2:0c3b size=290
1ec2:0c3b  ENTER 0x10,0x0
1ec2:0c3f  MOV byte ptr [BP + -0xf],0x3e
1ec2:0c43  MOV AX,word ptr [BP + 0x10]
1ec2:0c46  MOV word ptr [BP + -0x2],AX
1ec2:0c49  MOV AX,word ptr [BP + 0xe]
1ec2:0c4c  MOV word ptr [BP + -0x4],AX
1ec2:0c4f  MOV AX,word ptr [BP + 0xc]
1ec2:0c52  SUB AX,word ptr [BP + 0x10]
1ec2:0c55  MOV word ptr [BP + -0x8],AX
1ec2:0c58  MOV AX,word ptr [BP + 0xa]
1ec2:0c5b  SUB AX,word ptr [BP + 0xe]
1ec2:0c5e  MOV word ptr [BP + -0xa],AX
1ec2:0c61  PUSH word ptr [BP + -0x8]
1ec2:0c64  PUSH BP
1ec2:0c65  CALL 0x1000:f831
1ec2:0c68  MOV word ptr [BP + -0xc],AX
1ec2:0c6b  PUSH word ptr [BP + -0xa]
1ec2:0c6e  PUSH BP
1ec2:0c6f  CALL 0x1000:f831
1ec2:0c72  MOV word ptr [BP + -0xe],AX
1ec2:0c75  MOV AX,word ptr [BP + -0x8]
1ec2:0c78  CWD
1ec2:0c79  XOR AX,DX
1ec2:0c7b  SUB AX,DX
1ec2:0c7d  MOV word ptr [BP + -0x8],AX
1ec2:0c80  MOV AX,word ptr [BP + -0xa]
1ec2:0c83  CWD
1ec2:0c84  XOR AX,DX
1ec2:0c86  SUB AX,DX
1ec2:0c88  MOV word ptr [BP + -0xa],AX
1ec2:0c8b  MOV AX,word ptr [BP + -0x8]
1ec2:0c8e  CMP AX,word ptr [BP + -0xa]
1ec2:0c91  JLE 0x1000:f917
1ec2:0c93  MOV AX,word ptr [BP + -0x8]
1ec2:0c96  CWD
1ec2:0c97  MOV CX,0x2
1ec2:0c9a  IDIV CX
1ec2:0c9c  NEG AX
1ec2:0c9e  MOV word ptr [BP + -0x6],AX
1ec2:0ca1  MOV AX,word ptr [BP + -0x2]
1ec2:0ca4  CMP AX,word ptr [BP + 0xc]
1ec2:0ca7  JZ 0x1000:f915
1ec2:0ca9  MOV AX,word ptr [BP + -0x6]
1ec2:0cac  ADD AX,word ptr [BP + -0xa]
1ec2:0caf  MOV word ptr [BP + -0x6],AX
1ec2:0cb2  MOV AX,word ptr [BP + -0x2]
1ec2:0cb5  ADD AX,word ptr [BP + -0xc]
1ec2:0cb8  MOV word ptr [BP + -0x2],AX
1ec2:0cbb  CMP word ptr [BP + -0x6],0x0
1ec2:0cbf  JLE 0x1000:f8f3
1ec2:0cc1  MOV AX,word ptr [BP + -0x4]
1ec2:0cc4  ADD AX,word ptr [BP + -0xe]
1ec2:0cc7  MOV word ptr [BP + -0x4],AX
1ec2:0cca  MOV AX,word ptr [BP + -0x6]
1ec2:0ccd  SUB AX,word ptr [BP + -0x8]
1ec2:0cd0  MOV word ptr [BP + -0x6],AX
1ec2:0cd3  INC byte ptr [BP + -0xf]
1ec2:0cd6  CMP byte ptr [BP + -0xf],0x40
1ec2:0cda  JNZ 0x1000:f900
1ec2:0cdc  MOV byte ptr [BP + -0xf],0x3e
1ec2:0ce0  PUSH word ptr [BP + -0x2]
1ec2:0ce3  PUSH word ptr [BP + -0x4]
1ec2:0ce6  MOV AL,byte ptr [BP + -0xf]
1ec2:0ce9  PUSH AX
1ec2:0cea  LES DI,[BP + 0x6]
1ec2:0ced  PUSH ES
1ec2:0cee  PUSH DI
1ec2:0cef  PUSH CS
1ec2:0cf0  CALL 0x1000:f9e8
1ec2:0cf3  JMP 0x1000:f8c1
1ec2:0cf5  JMP 0x1000:f979
1ec2:0cf7  MOV AX,word ptr [BP + -0xa]
1ec2:0cfa  CWD
1ec2:0cfb  MOV CX,0x2
1ec2:0cfe  IDIV CX
1ec2:0d00  NEG AX
1ec2:0d02  MOV word ptr [BP + -0x6],AX
1ec2:0d05  MOV AX,word ptr [BP + -0x4]
1ec2:0d08  CMP AX,word ptr [BP + 0xa]
1ec2:0d0b  JZ 0x1000:f979
1ec2:0d0d  MOV AX,word ptr [BP + -0x6]
1ec2:0d10  ADD AX,word ptr [BP + -0x8]
1ec2:0d13  MOV word ptr [BP + -0x6],AX
1ec2:0d16  MOV AX,word ptr [BP + -0x4]
1ec2:0d19  ADD AX,word ptr [BP + -0xe]
1ec2:0d1c  MOV word ptr [BP + -0x4],AX
1ec2:0d1f  CMP word ptr [BP + -0x6],0x0
1ec2:0d23  JLE 0x1000:f957
1ec2:0d25  MOV AX,word ptr [BP + -0x2]
1ec2:0d28  ADD AX,word ptr [BP + -0xc]
1ec2:0d2b  MOV word ptr [BP + -0x2],AX
1ec2:0d2e  MOV AX,word ptr [BP + -0x6]
1ec2:0d31  SUB AX,word ptr [BP + -0xa]
1ec2:0d34  MOV word ptr [BP + -0x6],AX
1ec2:0d37  INC byte ptr [BP + -0xf]
1ec2:0d3a  CMP byte ptr [BP + -0xf],0x40
1ec2:0d3e  JNZ 0x1000:f964
1ec2:0d40  MOV byte ptr [BP + -0xf],0x3e
1ec2:0d44  PUSH word ptr [BP + -0x2]
1ec2:0d47  PUSH word ptr [BP + -0x4]
1ec2:0d4a  MOV AL,byte ptr [BP + -0xf]
1ec2:0d4d  PUSH AX
1ec2:0d4e  LES DI,[BP + 0x6]
1ec2:0d51  PUSH ES
1ec2:0d52  PUSH DI
1ec2:0d53  PUSH CS
1ec2:0d54  CALL 0x1000:f9e8
1ec2:0d57  JMP 0x1000:f925
1ec2:0d59  LEAVE
1ec2:0d5a  RETF 0xc
