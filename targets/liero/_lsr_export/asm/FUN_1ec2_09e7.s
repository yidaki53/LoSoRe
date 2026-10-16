; FUN_1ec2_09e7  entry=1ec2:09e7 size=252
1ec2:09e7  ENTER 0xe,0x0
1ec2:09eb  MOV AX,word ptr [BP + 0x10]
1ec2:09ee  MOV word ptr [BP + -0x2],AX
1ec2:09f1  MOV AX,word ptr [BP + 0xe]
1ec2:09f4  MOV word ptr [BP + -0x4],AX
1ec2:09f7  MOV AX,word ptr [BP + 0xc]
1ec2:09fa  SUB AX,word ptr [BP + 0x10]
1ec2:09fd  MOV word ptr [BP + -0x8],AX
1ec2:0a00  MOV AX,word ptr [BP + 0xa]
1ec2:0a03  SUB AX,word ptr [BP + 0xe]
1ec2:0a06  MOV word ptr [BP + -0xa],AX
1ec2:0a09  PUSH word ptr [BP + -0x8]
1ec2:0a0c  PUSH BP
1ec2:0a0d  CALL 0x1000:f5dd
1ec2:0a10  MOV word ptr [BP + -0xc],AX
1ec2:0a13  PUSH word ptr [BP + -0xa]
1ec2:0a16  PUSH BP
1ec2:0a17  CALL 0x1000:f5dd
1ec2:0a1a  MOV word ptr [BP + -0xe],AX
1ec2:0a1d  MOV AX,word ptr [BP + -0x8]
1ec2:0a20  CWD
1ec2:0a21  XOR AX,DX
1ec2:0a23  SUB AX,DX
1ec2:0a25  MOV word ptr [BP + -0x8],AX
1ec2:0a28  MOV AX,word ptr [BP + -0xa]
1ec2:0a2b  CWD
1ec2:0a2c  XOR AX,DX
1ec2:0a2e  SUB AX,DX
1ec2:0a30  MOV word ptr [BP + -0xa],AX
1ec2:0a33  MOV AX,word ptr [BP + -0x8]
1ec2:0a36  CMP AX,word ptr [BP + -0xa]
1ec2:0a39  JLE 0x1000:f6ae
1ec2:0a3b  MOV AX,word ptr [BP + -0x8]
1ec2:0a3e  CWD
1ec2:0a3f  MOV CX,0x2
1ec2:0a42  IDIV CX
1ec2:0a44  NEG AX
1ec2:0a46  MOV word ptr [BP + -0x6],AX
1ec2:0a49  MOV AX,word ptr [BP + -0x2]
1ec2:0a4c  CMP AX,word ptr [BP + 0xc]
1ec2:0a4f  JZ 0x1000:f6ac
1ec2:0a51  MOV AX,word ptr [BP + -0x6]
1ec2:0a54  ADD AX,word ptr [BP + -0xa]
1ec2:0a57  MOV word ptr [BP + -0x6],AX
1ec2:0a5a  MOV AX,word ptr [BP + -0x2]
1ec2:0a5d  ADD AX,word ptr [BP + -0xc]
1ec2:0a60  MOV word ptr [BP + -0x2],AX
1ec2:0a63  CMP word ptr [BP + -0x6],0x0
1ec2:0a67  JLE 0x1000:f69b
1ec2:0a69  MOV AX,word ptr [BP + -0x4]
1ec2:0a6c  ADD AX,word ptr [BP + -0xe]
1ec2:0a6f  MOV word ptr [BP + -0x4],AX
1ec2:0a72  MOV AX,word ptr [BP + -0x6]
1ec2:0a75  SUB AX,word ptr [BP + -0x8]
1ec2:0a78  MOV word ptr [BP + -0x6],AX
1ec2:0a7b  PUSH word ptr [BP + -0x2]
1ec2:0a7e  PUSH word ptr [BP + -0x4]
1ec2:0a81  LES DI,[BP + 0x6]
1ec2:0a84  PUSH ES
1ec2:0a85  PUSH DI
1ec2:0a86  PUSH CS
1ec2:0a87  CALL 0x1000:fa6a
1ec2:0a8a  JMP 0x1000:f669
1ec2:0a8c  JMP 0x1000:f6ff
1ec2:0a8e  MOV AX,word ptr [BP + -0xa]
1ec2:0a91  CWD
1ec2:0a92  MOV CX,0x2
1ec2:0a95  IDIV CX
1ec2:0a97  NEG AX
1ec2:0a99  MOV word ptr [BP + -0x6],AX
1ec2:0a9c  MOV AX,word ptr [BP + -0x4]
1ec2:0a9f  CMP AX,word ptr [BP + 0xa]
1ec2:0aa2  JZ 0x1000:f6ff
1ec2:0aa4  MOV AX,word ptr [BP + -0x6]
1ec2:0aa7  ADD AX,word ptr [BP + -0x8]
1ec2:0aaa  MOV word ptr [BP + -0x6],AX
1ec2:0aad  MOV AX,word ptr [BP + -0x4]
1ec2:0ab0  ADD AX,word ptr [BP + -0xe]
1ec2:0ab3  MOV word ptr [BP + -0x4],AX
1ec2:0ab6  CMP word ptr [BP + -0x6],0x0
1ec2:0aba  JLE 0x1000:f6ee
1ec2:0abc  MOV AX,word ptr [BP + -0x2]
1ec2:0abf  ADD AX,word ptr [BP + -0xc]
1ec2:0ac2  MOV word ptr [BP + -0x2],AX
1ec2:0ac5  MOV AX,word ptr [BP + -0x6]
1ec2:0ac8  SUB AX,word ptr [BP + -0xa]
1ec2:0acb  MOV word ptr [BP + -0x6],AX
1ec2:0ace  PUSH word ptr [BP + -0x2]
1ec2:0ad1  PUSH word ptr [BP + -0x4]
1ec2:0ad4  LES DI,[BP + 0x6]
1ec2:0ad7  PUSH ES
1ec2:0ad8  PUSH DI
1ec2:0ad9  PUSH CS
1ec2:0ada  CALL 0x1000:fa6a
1ec2:0add  JMP 0x1000:f6bc
1ec2:0adf  LEAVE
1ec2:0ae0  RETF 0xc
