; FUN_1ec2_0b0d  entry=1ec2:0b0d size=260
1ec2:0b0d  ENTER 0xe,0x0
1ec2:0b11  MOV AX,word ptr [BP + 0x12]
1ec2:0b14  MOV word ptr [BP + -0x2],AX
1ec2:0b17  MOV AX,word ptr [BP + 0x10]
1ec2:0b1a  MOV word ptr [BP + -0x4],AX
1ec2:0b1d  MOV AX,word ptr [BP + 0xe]
1ec2:0b20  SUB AX,word ptr [BP + 0x12]
1ec2:0b23  MOV word ptr [BP + -0x8],AX
1ec2:0b26  MOV AX,word ptr [BP + 0xc]
1ec2:0b29  SUB AX,word ptr [BP + 0x10]
1ec2:0b2c  MOV word ptr [BP + -0xa],AX
1ec2:0b2f  PUSH word ptr [BP + -0x8]
1ec2:0b32  PUSH BP
1ec2:0b33  CALL 0x1000:f703
1ec2:0b36  MOV word ptr [BP + -0xc],AX
1ec2:0b39  PUSH word ptr [BP + -0xa]
1ec2:0b3c  PUSH BP
1ec2:0b3d  CALL 0x1000:f703
1ec2:0b40  MOV word ptr [BP + -0xe],AX
1ec2:0b43  MOV AX,word ptr [BP + -0x8]
1ec2:0b46  CWD
1ec2:0b47  XOR AX,DX
1ec2:0b49  SUB AX,DX
1ec2:0b4b  MOV word ptr [BP + -0x8],AX
1ec2:0b4e  MOV AX,word ptr [BP + -0xa]
1ec2:0b51  CWD
1ec2:0b52  XOR AX,DX
1ec2:0b54  SUB AX,DX
1ec2:0b56  MOV word ptr [BP + -0xa],AX
1ec2:0b59  MOV AX,word ptr [BP + -0x8]
1ec2:0b5c  CMP AX,word ptr [BP + -0xa]
1ec2:0b5f  JLE 0x1000:f7d8
1ec2:0b61  MOV AX,word ptr [BP + -0x8]
1ec2:0b64  CWD
1ec2:0b65  MOV CX,0x2
1ec2:0b68  IDIV CX
1ec2:0b6a  NEG AX
1ec2:0b6c  MOV word ptr [BP + -0x6],AX
1ec2:0b6f  MOV AX,word ptr [BP + -0x2]
1ec2:0b72  CMP AX,word ptr [BP + 0xe]
1ec2:0b75  JZ 0x1000:f7d6
1ec2:0b77  MOV AX,word ptr [BP + -0x6]
1ec2:0b7a  ADD AX,word ptr [BP + -0xa]
1ec2:0b7d  MOV word ptr [BP + -0x6],AX
1ec2:0b80  MOV AX,word ptr [BP + -0x2]
1ec2:0b83  ADD AX,word ptr [BP + -0xc]
1ec2:0b86  MOV word ptr [BP + -0x2],AX
1ec2:0b89  CMP word ptr [BP + -0x6],0x0
1ec2:0b8d  JLE 0x1000:f7c1
1ec2:0b8f  MOV AX,word ptr [BP + -0x4]
1ec2:0b92  ADD AX,word ptr [BP + -0xe]
1ec2:0b95  MOV word ptr [BP + -0x4],AX
1ec2:0b98  MOV AX,word ptr [BP + -0x6]
1ec2:0b9b  SUB AX,word ptr [BP + -0x8]
1ec2:0b9e  MOV word ptr [BP + -0x6],AX
1ec2:0ba1  PUSH word ptr [BP + -0x2]
1ec2:0ba4  PUSH word ptr [BP + -0x4]
1ec2:0ba7  MOV AL,byte ptr [BP + 0xa]
1ec2:0baa  PUSH AX
1ec2:0bab  LES DI,[BP + 0x6]
1ec2:0bae  PUSH ES
1ec2:0baf  PUSH DI
1ec2:0bb0  PUSH CS
1ec2:0bb1  CALL 0x1000:f9e8
1ec2:0bb4  JMP 0x1000:f78f
1ec2:0bb6  JMP 0x1000:f82d
1ec2:0bb8  MOV AX,word ptr [BP + -0xa]
1ec2:0bbb  CWD
1ec2:0bbc  MOV CX,0x2
1ec2:0bbf  IDIV CX
1ec2:0bc1  NEG AX
1ec2:0bc3  MOV word ptr [BP + -0x6],AX
1ec2:0bc6  MOV AX,word ptr [BP + -0x4]
1ec2:0bc9  CMP AX,word ptr [BP + 0xc]
1ec2:0bcc  JZ 0x1000:f82d
1ec2:0bce  MOV AX,word ptr [BP + -0x6]
1ec2:0bd1  ADD AX,word ptr [BP + -0x8]
1ec2:0bd4  MOV word ptr [BP + -0x6],AX
1ec2:0bd7  MOV AX,word ptr [BP + -0x4]
1ec2:0bda  ADD AX,word ptr [BP + -0xe]
1ec2:0bdd  MOV word ptr [BP + -0x4],AX
1ec2:0be0  CMP word ptr [BP + -0x6],0x0
1ec2:0be4  JLE 0x1000:f818
1ec2:0be6  MOV AX,word ptr [BP + -0x2]
1ec2:0be9  ADD AX,word ptr [BP + -0xc]
1ec2:0bec  MOV word ptr [BP + -0x2],AX
1ec2:0bef  MOV AX,word ptr [BP + -0x6]
1ec2:0bf2  SUB AX,word ptr [BP + -0xa]
1ec2:0bf5  MOV word ptr [BP + -0x6],AX
1ec2:0bf8  PUSH word ptr [BP + -0x2]
1ec2:0bfb  PUSH word ptr [BP + -0x4]
1ec2:0bfe  MOV AL,byte ptr [BP + 0xa]
1ec2:0c01  PUSH AX
1ec2:0c02  LES DI,[BP + 0x6]
1ec2:0c05  PUSH ES
1ec2:0c06  PUSH DI
1ec2:0c07  PUSH CS
1ec2:0c08  CALL 0x1000:f9e8
1ec2:0c0b  JMP 0x1000:f7e6
1ec2:0c0d  LEAVE
1ec2:0c0e  RETF 0xe
