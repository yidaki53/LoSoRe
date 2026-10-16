; FUN_1ec2_01df  entry=1ec2:01df size=423
1ec2:01df  ENTER 0x106,0x0
1ec2:01e3  MOV BX,SS
1ec2:01e5  MOV BX,ES
1ec2:01e7  MOV BX,DS
1ec2:01e9  CLD
1ec2:01ea  LEA DI,[BP + 0xff00]
1ec2:01ee  LDS SI,[BP + 0xe]
1ec2:01f1  MOV CX,0x100
1ec2:01f4  MOVSB.REP ES:DI,SI
1ec2:01f6  MOV BX,DS
1ec2:01f8  MOV AL,byte ptr [BP + 0x6]
1ec2:01fb  CMP AL,0x0
1ec2:01fd  JZ 0x1000:ee22
1ec2:01ff  JMP 0x1000:eee0
1ec2:0202  CMP byte ptr [BP + 0x8],0x0
1ec2:0206  JZ 0x1000:ee82
1ec2:0208  XOR AX,AX
1ec2:020a  MOV word ptr [BP + 0xfefa],AX
1ec2:020e  JMP 0x1000:ee34
1ec2:0210  INC word ptr [BP + 0xfefa]
1ec2:0214  MOV AX,word ptr [BP + 0x12]
1ec2:0217  ADD AX,word ptr [BP + 0xfefa]
1ec2:021b  MOV word ptr [BP + 0xfefc],AX
1ec2:021f  MOV word ptr [BP + 0xfefe],0x2
1ec2:0225  JMP 0x1000:ee4b
1ec2:0227  INC word ptr [BP + 0xfefe]
1ec2:022b  MOV AX,word ptr [BP + 0x14]
1ec2:022e  ADD AX,word ptr [BP + 0xfefe]
1ec2:0232  PUSH AX
1ec2:0233  PUSH word ptr [BP + 0xfefc]
1ec2:0237  MOV AX,word ptr [BP + 0xfefe]
1ec2:023b  MOV DI,word ptr [BP + 0xfefa]
1ec2:023f  SHL DI,0x4
1ec2:0242  ADD DI,AX
1ec2:0244  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:0248  PUSH AX
1ec2:0249  LES DI,[BP + 0xa]
1ec2:024c  PUSH ES
1ec2:024d  PUSH DI
1ec2:024e  PUSH CS
1ec2:024f  CALL 0x1000:f9e8
1ec2:0252  CMP word ptr [BP + 0xfefe],0xb
1ec2:0257  JNZ 0x1000:ee47
1ec2:0259  CMP word ptr [BP + 0xfefa],0x8
1ec2:025e  JNZ 0x1000:ee30
1ec2:0260  JMP 0x1000:eedd
1ec2:0262  XOR AX,AX
1ec2:0264  MOV word ptr [BP + 0xfefa],AX
1ec2:0268  JMP 0x1000:ee8e
1ec2:026a  INC word ptr [BP + 0xfefa]
1ec2:026e  MOV AX,word ptr [BP + 0x12]
1ec2:0271  ADD AX,word ptr [BP + 0xfefa]
1ec2:0275  MOV word ptr [BP + 0xfefc],AX
1ec2:0279  MOV word ptr [BP + 0xfefe],0x2
1ec2:027f  JMP 0x1000:eea5
1ec2:0281  INC word ptr [BP + 0xfefe]
1ec2:0285  MOV AX,0xe
1ec2:0288  SUB AX,word ptr [BP + 0xfefe]
1ec2:028c  ADD AX,word ptr [BP + 0x14]
1ec2:028f  PUSH AX
1ec2:0290  PUSH word ptr [BP + 0xfefc]
1ec2:0294  MOV AX,word ptr [BP + 0xfefe]
1ec2:0298  MOV DI,word ptr [BP + 0xfefa]
1ec2:029c  SHL DI,0x4
1ec2:029f  ADD DI,AX
1ec2:02a1  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:02a5  PUSH AX
1ec2:02a6  LES DI,[BP + 0xa]
1ec2:02a9  PUSH ES
1ec2:02aa  PUSH DI
1ec2:02ab  PUSH CS
1ec2:02ac  CALL 0x1000:f9e8
1ec2:02af  CMP word ptr [BP + 0xfefe],0xb
1ec2:02b4  JNZ 0x1000:eea1
1ec2:02b6  CMP word ptr [BP + 0xfefa],0x8
1ec2:02bb  JNZ 0x1000:ee8a
1ec2:02bd  JMP 0x1000:efa2
1ec2:02c0  CMP AL,0x1
1ec2:02c2  JZ 0x1000:eee7
1ec2:02c4  JMP 0x1000:efa2
1ec2:02c7  CMP byte ptr [BP + 0x8],0x0
1ec2:02cb  JZ 0x1000:ef47
1ec2:02cd  XOR AX,AX
1ec2:02cf  MOV word ptr [BP + 0xfefa],AX
1ec2:02d3  JMP 0x1000:eef9
1ec2:02d5  INC word ptr [BP + 0xfefa]
1ec2:02d9  MOV AX,word ptr [BP + 0x12]
1ec2:02dc  ADD AX,word ptr [BP + 0xfefa]
1ec2:02e0  MOV word ptr [BP + 0xfefc],AX
1ec2:02e4  MOV word ptr [BP + 0xfefe],0x2
1ec2:02ea  JMP 0x1000:ef10
1ec2:02ec  INC word ptr [BP + 0xfefe]
1ec2:02f0  MOV AX,word ptr [BP + 0x14]
1ec2:02f3  ADD AX,word ptr [BP + 0xfefe]
1ec2:02f7  PUSH AX
1ec2:02f8  PUSH word ptr [BP + 0xfefc]
1ec2:02fc  MOV AX,word ptr [BP + 0xfefe]
1ec2:0300  MOV DI,word ptr [BP + 0xfefa]
1ec2:0304  SHL DI,0x4
1ec2:0307  ADD DI,AX
1ec2:0309  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:030d  PUSH AX
1ec2:030e  LES DI,[BP + 0xa]
1ec2:0311  PUSH ES
1ec2:0312  PUSH DI
1ec2:0313  PUSH CS
1ec2:0314  CALL 0x1000:fa26
1ec2:0317  CMP word ptr [BP + 0xfefe],0xb
1ec2:031c  JNZ 0x1000:ef0c
1ec2:031e  CMP word ptr [BP + 0xfefa],0x8
1ec2:0323  JNZ 0x1000:eef5
1ec2:0325  JMP 0x1000:efa2
1ec2:0327  XOR AX,AX
1ec2:0329  MOV word ptr [BP + 0xfefa],AX
1ec2:032d  JMP 0x1000:ef53
1ec2:032f  INC word ptr [BP + 0xfefa]
1ec2:0333  MOV AX,word ptr [BP + 0x12]
1ec2:0336  ADD AX,word ptr [BP + 0xfefa]
1ec2:033a  MOV word ptr [BP + 0xfefc],AX
1ec2:033e  MOV word ptr [BP + 0xfefe],0x2
1ec2:0344  JMP 0x1000:ef6a
1ec2:0346  INC word ptr [BP + 0xfefe]
1ec2:034a  MOV AX,0xe
1ec2:034d  SUB AX,word ptr [BP + 0xfefe]
1ec2:0351  ADD AX,word ptr [BP + 0x14]
1ec2:0354  PUSH AX
1ec2:0355  PUSH word ptr [BP + 0xfefc]
1ec2:0359  MOV AX,word ptr [BP + 0xfefe]
1ec2:035d  MOV DI,word ptr [BP + 0xfefa]
1ec2:0361  SHL DI,0x4
1ec2:0364  ADD DI,AX
1ec2:0366  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:036a  PUSH AX
1ec2:036b  LES DI,[BP + 0xa]
1ec2:036e  PUSH ES
1ec2:036f  PUSH DI
1ec2:0370  PUSH CS
1ec2:0371  CALL 0x1000:fa26
1ec2:0374  CMP word ptr [BP + 0xfefe],0xb
1ec2:0379  JNZ 0x1000:ef66
1ec2:037b  CMP word ptr [BP + 0xfefa],0x8
1ec2:0380  JNZ 0x1000:ef4f
1ec2:0382  LEAVE
1ec2:0383  RETF 0x10
