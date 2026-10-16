; FUN_1ec2_0d88  entry=1ec2:0d88 size=64
1ec2:0d88  ENTER 0x2,0x0
1ec2:0d8c  LES DI,[BP + 0xc]
1ec2:0d8f  MOV BX,word ptr [BP + 0x8]
1ec2:0d92  SUB BX,0x2
1ec2:0d95  MOV CX,word ptr [BP + 0xa]
1ec2:0d98  MOV DX,0x140
1ec2:0d9b  SUB DX,CX
1ec2:0d9d  MOV word ptr [BP + -0x2],CX
1ec2:0da0  XOR AX,AX
1ec2:0da2  MOV AL,byte ptr [BP + 0x6]
1ec2:0da5  INC DI
1ec2:0da6  OR CX,word ptr [BP + -0x2]
1ec2:0da9  SUB CX,0x2
1ec2:0dac  STOSB.REP ES:DI
1ec2:0dae  INC DI
1ec2:0daf  ADD DI,DX
1ec2:0db1  OR CX,word ptr [BP + -0x2]
1ec2:0db4  STOSB.REP ES:DI
1ec2:0db6  ADD DI,DX
1ec2:0db8  DEC BX
1ec2:0db9  JNZ 0x1000:f9d1
1ec2:0dbb  INC DI
1ec2:0dbc  OR CX,word ptr [BP + -0x2]
1ec2:0dbf  SUB CX,0x2
1ec2:0dc2  STOSB.REP ES:DI
1ec2:0dc4  LEAVE
1ec2:0dc5  RETF 0xa
