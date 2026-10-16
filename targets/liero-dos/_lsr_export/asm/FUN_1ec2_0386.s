; FUN_1ec2_0386  entry=1ec2:0386 size=942
1ec2:0386  ENTER 0x108,0x0
1ec2:038a  MOV BX,SS
1ec2:038c  MOV BX,ES
1ec2:038e  MOV BX,DS
1ec2:0390  CLD
1ec2:0391  LEA DI,[BP + 0xff00]
1ec2:0395  LDS SI,[BP + 0xe]
1ec2:0398  MOV CX,0x100
1ec2:039b  MOVSB.REP ES:DI,SI
1ec2:039d  MOV BX,DS
1ec2:039f  MOV AL,byte ptr [BP + 0x6]
1ec2:03a2  CMP AL,0x0
1ec2:03a4  JZ 0x1000:efc9
1ec2:03a6  JMP 0x1000:f0af
1ec2:03a9  CMP byte ptr [BP + 0x8],0x0
1ec2:03ad  JZ 0x1000:f03d
1ec2:03af  XOR AX,AX
1ec2:03b1  MOV word ptr [BP + 0xfefa],AX
1ec2:03b5  JMP 0x1000:efdb
1ec2:03b7  INC word ptr [BP + 0xfefa]
1ec2:03bb  MOV AX,word ptr [BP + 0x12]
1ec2:03be  ADD AX,word ptr [BP + 0xfefa]
1ec2:03c2  MOV word ptr [BP + 0xfefc],AX
1ec2:03c6  MOV word ptr [BP + 0xfefe],0x2
1ec2:03cc  JMP 0x1000:eff2
1ec2:03ce  INC word ptr [BP + 0xfefe]
1ec2:03d2  MOV AX,word ptr [BP + 0xfefe]
1ec2:03d6  MOV DI,word ptr [BP + 0xfefa]
1ec2:03da  SHL DI,0x4
1ec2:03dd  ADD DI,AX
1ec2:03df  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:03e3  MOV byte ptr [BP + 0xfef9],AL
1ec2:03e7  CMP byte ptr [BP + 0xfef9],0x74
1ec2:03ec  JBE 0x1000:f02d
1ec2:03ee  MOV AX,word ptr [BP + 0x14]
1ec2:03f1  ADD AX,word ptr [BP + 0xfefe]
1ec2:03f5  PUSH AX
1ec2:03f6  PUSH word ptr [BP + 0xfefc]
1ec2:03fa  MOV AL,byte ptr [BP + 0xfef9]
1ec2:03fe  XOR AH,AH
1ec2:0400  SUB AX,0x5
1ec2:0403  PUSH AX
1ec2:0404  LES DI,[BP + 0xa]
1ec2:0407  PUSH ES
1ec2:0408  PUSH DI
1ec2:0409  PUSH CS
1ec2:040a  CALL 0x1000:f9e8
1ec2:040d  CMP word ptr [BP + 0xfefe],0xd
1ec2:0412  JNZ 0x1000:efee
1ec2:0414  CMP word ptr [BP + 0xfefa],0xf
1ec2:0419  JNZ 0x1000:efd7
1ec2:041b  JMP 0x1000:f0ac
1ec2:041d  XOR AX,AX
1ec2:041f  MOV word ptr [BP + 0xfefa],AX
1ec2:0423  JMP 0x1000:f049
1ec2:0425  INC word ptr [BP + 0xfefa]
1ec2:0429  MOV AX,word ptr [BP + 0x12]
1ec2:042c  ADD AX,word ptr [BP + 0xfefa]
1ec2:0430  MOV word ptr [BP + 0xfefc],AX
1ec2:0434  MOV word ptr [BP + 0xfefe],0x2
1ec2:043a  JMP 0x1000:f060
1ec2:043c  INC word ptr [BP + 0xfefe]
1ec2:0440  MOV AX,word ptr [BP + 0xfefe]
1ec2:0444  MOV DI,word ptr [BP + 0xfefa]
1ec2:0448  SHL DI,0x4
1ec2:044b  ADD DI,AX
1ec2:044d  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:0451  MOV byte ptr [BP + 0xfef9],AL
1ec2:0455  CMP byte ptr [BP + 0xfef9],0x74
1ec2:045a  JBE 0x1000:f09e
1ec2:045c  MOV AX,0xe
1ec2:045f  SUB AX,word ptr [BP + 0xfefe]
1ec2:0463  ADD AX,word ptr [BP + 0x14]
1ec2:0466  PUSH AX
1ec2:0467  PUSH word ptr [BP + 0xfefc]
1ec2:046b  MOV AL,byte ptr [BP + 0xfef9]
1ec2:046f  XOR AH,AH
1ec2:0471  SUB AX,0x5
1ec2:0474  PUSH AX
1ec2:0475  LES DI,[BP + 0xa]
1ec2:0478  PUSH ES
1ec2:0479  PUSH DI
1ec2:047a  PUSH CS
1ec2:047b  CALL 0x1000:f9e8
1ec2:047e  CMP word ptr [BP + 0xfefe],0xd
1ec2:0483  JNZ 0x1000:f05c
1ec2:0485  CMP word ptr [BP + 0xfefa],0xf
1ec2:048a  JNZ 0x1000:f045
1ec2:048c  JMP 0x1000:f350
1ec2:048f  CMP AL,0x1
1ec2:0491  JZ 0x1000:f0b6
1ec2:0493  JMP 0x1000:f19c
1ec2:0496  CMP byte ptr [BP + 0x8],0x0
1ec2:049a  JZ 0x1000:f12a
1ec2:049c  XOR AX,AX
1ec2:049e  MOV word ptr [BP + 0xfefa],AX
1ec2:04a2  JMP 0x1000:f0c8
1ec2:04a4  INC word ptr [BP + 0xfefa]
1ec2:04a8  MOV AX,word ptr [BP + 0x12]
1ec2:04ab  ADD AX,word ptr [BP + 0xfefa]
1ec2:04af  MOV word ptr [BP + 0xfefc],AX
1ec2:04b3  MOV word ptr [BP + 0xfefe],0x2
1ec2:04b9  JMP 0x1000:f0df
1ec2:04bb  INC word ptr [BP + 0xfefe]
1ec2:04bf  MOV AX,word ptr [BP + 0xfefe]
1ec2:04c3  MOV DI,word ptr [BP + 0xfefa]
1ec2:04c7  SHL DI,0x4
1ec2:04ca  ADD DI,AX
1ec2:04cc  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:04d0  MOV byte ptr [BP + 0xfef9],AL
1ec2:04d4  CMP byte ptr [BP + 0xfef9],0x72
1ec2:04d9  JBE 0x1000:f11a
1ec2:04db  MOV AX,word ptr [BP + 0x14]
1ec2:04de  ADD AX,word ptr [BP + 0xfefe]
1ec2:04e2  PUSH AX
1ec2:04e3  PUSH word ptr [BP + 0xfefc]
1ec2:04e7  MOV AL,byte ptr [BP + 0xfef9]
1ec2:04eb  XOR AH,AH
1ec2:04ed  SUB AX,0x3
1ec2:04f0  PUSH AX
1ec2:04f1  LES DI,[BP + 0xa]
1ec2:04f4  PUSH ES
1ec2:04f5  PUSH DI
1ec2:04f6  PUSH CS
1ec2:04f7  CALL 0x1000:f9e8
1ec2:04fa  CMP word ptr [BP + 0xfefe],0xd
1ec2:04ff  JNZ 0x1000:f0db
1ec2:0501  CMP word ptr [BP + 0xfefa],0xf
1ec2:0506  JNZ 0x1000:f0c4
1ec2:0508  JMP 0x1000:f199
1ec2:050a  XOR AX,AX
1ec2:050c  MOV word ptr [BP + 0xfefa],AX
1ec2:0510  JMP 0x1000:f136
1ec2:0512  INC word ptr [BP + 0xfefa]
1ec2:0516  MOV AX,word ptr [BP + 0x12]
1ec2:0519  ADD AX,word ptr [BP + 0xfefa]
1ec2:051d  MOV word ptr [BP + 0xfefc],AX
1ec2:0521  MOV word ptr [BP + 0xfefe],0x2
1ec2:0527  JMP 0x1000:f14d
1ec2:0529  INC word ptr [BP + 0xfefe]
1ec2:052d  MOV AX,word ptr [BP + 0xfefe]
1ec2:0531  MOV DI,word ptr [BP + 0xfefa]
1ec2:0535  SHL DI,0x4
1ec2:0538  ADD DI,AX
1ec2:053a  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:053e  MOV byte ptr [BP + 0xfef9],AL
1ec2:0542  CMP byte ptr [BP + 0xfef9],0x72
1ec2:0547  JBE 0x1000:f18b
1ec2:0549  MOV AX,0xe
1ec2:054c  SUB AX,word ptr [BP + 0xfefe]
1ec2:0550  ADD AX,word ptr [BP + 0x14]
1ec2:0553  PUSH AX
1ec2:0554  PUSH word ptr [BP + 0xfefc]
1ec2:0558  MOV AL,byte ptr [BP + 0xfef9]
1ec2:055c  XOR AH,AH
1ec2:055e  SUB AX,0x3
1ec2:0561  PUSH AX
1ec2:0562  LES DI,[BP + 0xa]
1ec2:0565  PUSH ES
1ec2:0566  PUSH DI
1ec2:0567  PUSH CS
1ec2:0568  CALL 0x1000:f9e8
1ec2:056b  CMP word ptr [BP + 0xfefe],0xd
1ec2:0570  JNZ 0x1000:f149
1ec2:0572  CMP word ptr [BP + 0xfefa],0xf
1ec2:0577  JNZ 0x1000:f132
1ec2:0579  JMP 0x1000:f350
1ec2:057c  CMP AL,0x2
1ec2:057e  JZ 0x1000:f1a3
1ec2:0580  JMP 0x1000:f285
1ec2:0583  CMP byte ptr [BP + 0x8],0x0
1ec2:0587  JZ 0x1000:f215
1ec2:0589  XOR AX,AX
1ec2:058b  MOV word ptr [BP + 0xfefa],AX
1ec2:058f  JMP 0x1000:f1b5
1ec2:0591  INC word ptr [BP + 0xfefa]
1ec2:0595  MOV AX,word ptr [BP + 0x12]
1ec2:0598  ADD AX,word ptr [BP + 0xfefa]
1ec2:059c  MOV word ptr [BP + 0xfefc],AX
1ec2:05a0  MOV word ptr [BP + 0xfefe],0x2
1ec2:05a6  JMP 0x1000:f1cc
1ec2:05a8  INC word ptr [BP + 0xfefe]
1ec2:05ac  MOV AX,word ptr [BP + 0xfefe]
1ec2:05b0  MOV DI,word ptr [BP + 0xfefa]
1ec2:05b4  SHL DI,0x4
1ec2:05b7  ADD DI,AX
1ec2:05b9  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:05bd  MOV byte ptr [BP + 0xfef9],AL
1ec2:05c1  CMP byte ptr [BP + 0xfef9],0x70
1ec2:05c6  JBE 0x1000:f205
1ec2:05c8  MOV AX,word ptr [BP + 0x14]
1ec2:05cb  ADD AX,word ptr [BP + 0xfefe]
1ec2:05cf  PUSH AX
1ec2:05d0  PUSH word ptr [BP + 0xfefc]
1ec2:05d4  MOV AL,byte ptr [BP + 0xfef9]
1ec2:05d8  XOR AH,AH
1ec2:05da  DEC AX
1ec2:05db  PUSH AX
1ec2:05dc  LES DI,[BP + 0xa]
1ec2:05df  PUSH ES
1ec2:05e0  PUSH DI
1ec2:05e1  PUSH CS
1ec2:05e2  CALL 0x1000:f9e8
1ec2:05e5  CMP word ptr [BP + 0xfefe],0xd
1ec2:05ea  JNZ 0x1000:f1c8
1ec2:05ec  CMP word ptr [BP + 0xfefa],0xf
1ec2:05f1  JNZ 0x1000:f1b1
1ec2:05f3  JMP 0x1000:f282
1ec2:05f5  XOR AX,AX
1ec2:05f7  MOV word ptr [BP + 0xfefa],AX
1ec2:05fb  JMP 0x1000:f221
1ec2:05fd  INC word ptr [BP + 0xfefa]
1ec2:0601  MOV AX,word ptr [BP + 0x12]
1ec2:0604  ADD AX,word ptr [BP + 0xfefa]
1ec2:0608  MOV word ptr [BP + 0xfefc],AX
1ec2:060c  MOV word ptr [BP + 0xfefe],0x2
1ec2:0612  JMP 0x1000:f238
1ec2:0614  INC word ptr [BP + 0xfefe]
1ec2:0618  MOV AX,word ptr [BP + 0xfefe]
1ec2:061c  MOV DI,word ptr [BP + 0xfefa]
1ec2:0620  SHL DI,0x4
1ec2:0623  ADD DI,AX
1ec2:0625  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:0629  MOV byte ptr [BP + 0xfef9],AL
1ec2:062d  CMP byte ptr [BP + 0xfef9],0x70
1ec2:0632  JBE 0x1000:f274
1ec2:0634  MOV AX,0xe
1ec2:0637  SUB AX,word ptr [BP + 0xfefe]
1ec2:063b  ADD AX,word ptr [BP + 0x14]
1ec2:063e  PUSH AX
1ec2:063f  PUSH word ptr [BP + 0xfefc]
1ec2:0643  MOV AL,byte ptr [BP + 0xfef9]
1ec2:0647  XOR AH,AH
1ec2:0649  DEC AX
1ec2:064a  PUSH AX
1ec2:064b  LES DI,[BP + 0xa]
1ec2:064e  PUSH ES
1ec2:064f  PUSH DI
1ec2:0650  PUSH CS
1ec2:0651  CALL 0x1000:f9e8
1ec2:0654  CMP word ptr [BP + 0xfefe],0xd
1ec2:0659  JNZ 0x1000:f234
1ec2:065b  CMP word ptr [BP + 0xfefa],0xf
1ec2:0660  JNZ 0x1000:f21d
1ec2:0662  JMP 0x1000:f350
1ec2:0665  CMP byte ptr [BP + 0x8],0x0
1ec2:0669  JZ 0x1000:f2ed
1ec2:066b  XOR AX,AX
1ec2:066d  MOV word ptr [BP + 0xfefa],AX
1ec2:0671  JMP 0x1000:f297
1ec2:0673  INC word ptr [BP + 0xfefa]
1ec2:0677  MOV AX,word ptr [BP + 0x12]
1ec2:067a  ADD AX,word ptr [BP + 0xfefa]
1ec2:067e  MOV word ptr [BP + 0xfefc],AX
1ec2:0682  MOV word ptr [BP + 0xfefe],0x2
1ec2:0688  JMP 0x1000:f2ae
1ec2:068a  INC word ptr [BP + 0xfefe]
1ec2:068e  MOV AX,word ptr [BP + 0xfefe]
1ec2:0692  MOV DI,word ptr [BP + 0xfefa]
1ec2:0696  SHL DI,0x4
1ec2:0699  ADD DI,AX
1ec2:069b  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:069f  MOV byte ptr [BP + 0xfef9],AL
1ec2:06a3  MOV AX,word ptr [BP + 0x14]
1ec2:06a6  ADD AX,word ptr [BP + 0xfefe]
1ec2:06aa  PUSH AX
1ec2:06ab  PUSH word ptr [BP + 0xfefc]
1ec2:06af  MOV AL,byte ptr [BP + 0xfef9]
1ec2:06b3  PUSH AX
1ec2:06b4  LES DI,[BP + 0xa]
1ec2:06b7  PUSH ES
1ec2:06b8  PUSH DI
1ec2:06b9  PUSH CS
1ec2:06ba  CALL 0x1000:f9e8
1ec2:06bd  CMP word ptr [BP + 0xfefe],0xd
1ec2:06c2  JNZ 0x1000:f2aa
1ec2:06c4  CMP word ptr [BP + 0xfefa],0xf
1ec2:06c9  JNZ 0x1000:f293
1ec2:06cb  JMP 0x1000:f350
1ec2:06cd  XOR AX,AX
1ec2:06cf  MOV word ptr [BP + 0xfefa],AX
1ec2:06d3  JMP 0x1000:f2f9
1ec2:06d5  INC word ptr [BP + 0xfefa]
1ec2:06d9  MOV AX,word ptr [BP + 0x12]
1ec2:06dc  ADD AX,word ptr [BP + 0xfefa]
1ec2:06e0  MOV word ptr [BP + 0xfefc],AX
1ec2:06e4  MOV word ptr [BP + 0xfefe],0x2
1ec2:06ea  JMP 0x1000:f310
1ec2:06ec  INC word ptr [BP + 0xfefe]
1ec2:06f0  MOV AX,word ptr [BP + 0xfefe]
1ec2:06f4  MOV DI,word ptr [BP + 0xfefa]
1ec2:06f8  SHL DI,0x4
1ec2:06fb  ADD DI,AX
1ec2:06fd  MOV AL,byte ptr [BP + DI + 0xff00]
1ec2:0701  MOV byte ptr [BP + 0xfef9],AL
1ec2:0705  MOV AX,0xe
1ec2:0708  SUB AX,word ptr [BP + 0xfefe]
1ec2:070c  ADD AX,word ptr [BP + 0x14]
1ec2:070f  PUSH AX
1ec2:0710  PUSH word ptr [BP + 0xfefc]
1ec2:0714  MOV AL,byte ptr [BP + 0xfef9]
1ec2:0718  PUSH AX
1ec2:0719  LES DI,[BP + 0xa]
1ec2:071c  PUSH ES
1ec2:071d  PUSH DI
1ec2:071e  PUSH CS
1ec2:071f  CALL 0x1000:f9e8
1ec2:0722  CMP word ptr [BP + 0xfefe],0xd
1ec2:0727  JNZ 0x1000:f30c
1ec2:0729  CMP word ptr [BP + 0xfefa],0xf
1ec2:072e  JNZ 0x1000:f2f5
1ec2:0730  LEAVE
1ec2:0731  RETF 0x10
