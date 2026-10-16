; FUN_1ec2_0734  entry=1ec2:0734 size=220
1ec2:0734  ENTER 0x106,0x0
1ec2:0738  MOV BX,SS
1ec2:073a  MOV BX,ES
1ec2:073c  MOV BX,DS
1ec2:073e  CLD
1ec2:073f  LEA DI,[BP + 0xff00]
1ec2:0743  LDS SI,[BP + 0xc]
1ec2:0746  MOV CX,0x100
1ec2:0749  MOVSB.REP ES:DI,SI
1ec2:074b  MOV BX,DS
1ec2:074d  CMP byte ptr [BP + 0x6],0x0
1ec2:0751  JZ 0x1000:f3cf
1ec2:0753  XOR AX,AX
1ec2:0755  MOV word ptr [BP + 0xfefa],AX
1ec2:0759  JMP 0x1000:f37f
1ec2:075b  INC word ptr [BP + 0xfefa]
1ec2:075f  MOV AX,word ptr [BP + 0x10]
1ec2:0762  ADD AX,word ptr [BP + 0xfefa]
1ec2:0766  MOV word ptr [BP + 0xfefc],AX
1ec2:076a  MOV word ptr [BP + 0xfefe],0x2
1ec2:0770  JMP 0x1000:f396
1ec2:0772  INC word ptr [BP + 0xfefe]
1ec2:0776  MOV AX,word ptr [BP + 0xfefe]
1ec2:077a  MOV DI,word ptr [BP + 0xfefa]
1ec2:077e  SHL DI,0x4
1ec2:0781  ADD DI,AX
1ec2:0783  CMP byte ptr [BP + DI + 0xff00],0x0
1ec2:0788  JBE 0x1000:f3bf
1ec2:078a  MOV AX,word ptr [BP + 0x12]
1ec2:078d  ADD AX,word ptr [BP + 0xfefe]
1ec2:0791  PUSH AX
1ec2:0792  PUSH word ptr [BP + 0xfefc]
1ec2:0796  LES DI,[BP + 0x8]
1ec2:0799  PUSH ES
1ec2:079a  PUSH DI
1ec2:079b  PUSH CS
1ec2:079c  CALL 0x1000:fa6a
1ec2:079f  CMP word ptr [BP + 0xfefe],0xb
1ec2:07a4  JNZ 0x1000:f392
1ec2:07a6  CMP word ptr [BP + 0xfefa],0x8
1ec2:07ab  JNZ 0x1000:f37b
1ec2:07ad  JMP 0x1000:f42c
1ec2:07af  XOR AX,AX
1ec2:07b1  MOV word ptr [BP + 0xfefa],AX
1ec2:07b5  JMP 0x1000:f3db
1ec2:07b7  INC word ptr [BP + 0xfefa]
1ec2:07bb  MOV AX,word ptr [BP + 0x10]
1ec2:07be  ADD AX,word ptr [BP + 0xfefa]
1ec2:07c2  MOV word ptr [BP + 0xfefc],AX
1ec2:07c6  MOV word ptr [BP + 0xfefe],0x2
1ec2:07cc  JMP 0x1000:f3f2
1ec2:07ce  INC word ptr [BP + 0xfefe]
1ec2:07d2  MOV AX,word ptr [BP + 0xfefe]
1ec2:07d6  MOV DI,word ptr [BP + 0xfefa]
1ec2:07da  SHL DI,0x4
1ec2:07dd  ADD DI,AX
1ec2:07df  CMP byte ptr [BP + DI + 0xff00],0x0
1ec2:07e4  JBE 0x1000:f41e
1ec2:07e6  MOV AX,0xe
1ec2:07e9  SUB AX,word ptr [BP + 0xfefe]
1ec2:07ed  ADD AX,word ptr [BP + 0x12]
1ec2:07f0  PUSH AX
1ec2:07f1  PUSH word ptr [BP + 0xfefc]
1ec2:07f5  LES DI,[BP + 0x8]
1ec2:07f8  PUSH ES
1ec2:07f9  PUSH DI
1ec2:07fa  PUSH CS
1ec2:07fb  CALL 0x1000:fa6a
1ec2:07fe  CMP word ptr [BP + 0xfefe],0xb
1ec2:0803  JNZ 0x1000:f3ee
1ec2:0805  CMP word ptr [BP + 0xfefa],0x8
1ec2:080a  JNZ 0x1000:f3d7
1ec2:080c  LEAVE
1ec2:080d  RETF 0xe
