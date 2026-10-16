; FUN_1000_db9c  entry=1000:db9c size=954
1000:db9c  PUSH BP
1000:db9d  MOV BP,SP
1000:db9f  MOV AX,0x292
1000:dba2  CALLF 0x2000:5300
1000:dba7  SUB SP,0x292
1000:dbab  CALLF 0x2000:94b9
1000:dbb0  MOV DI,0x1500
1000:dbb3  PUSH DS
1000:dbb4  PUSH DI
1000:dbb5  MOV DI,0x669c
1000:dbb8  PUSH DS
1000:dbb9  PUSH DI
1000:dbba  PUSH 0x9b
1000:dbbd  CALLF 0x2000:8b38
1000:dbc2  MOV DI,0xdb82
1000:dbc5  PUSH CS
1000:dbc6  PUSH DI
1000:dbc7  CALLF 0x2000:0b03
1000:dbcc  OR AL,AL
1000:dbce  JZ 0x1000:dc37
1000:dbd0  LEA DI,[BP + 0xfd77]
1000:dbd4  PUSH SS
1000:dbd5  PUSH DI
1000:dbd6  MOV DI,0xdb82
1000:dbd9  PUSH CS
1000:dbda  PUSH DI
1000:dbdb  CALLF 0x2000:8409
1000:dbe0  LEA DI,[BP + 0xfd77]
1000:dbe4  PUSH SS
1000:dbe5  PUSH DI
1000:dbe6  CALLF 0x2000:8487
1000:dbeb  CALLF 0x2000:52c4
1000:dbf0  LEA DI,[BP + 0xfd77]
1000:dbf4  PUSH SS
1000:dbf5  PUSH DI
1000:dbf6  LEA DI,[BP + 0xfd6e]
1000:dbfa  PUSH SS
1000:dbfb  PUSH DI
1000:dbfc  PUSH 0x8
1000:dbfe  CALLF 0x2000:8758
1000:dc03  CALLF 0x2000:86c0
1000:dc08  CALLF 0x2000:52c4
1000:dc0d  LEA DI,[BP + 0xfd77]
1000:dc11  PUSH SS
1000:dc12  PUSH DI
1000:dc13  CALLF 0x2000:84e1
1000:dc18  CALLF 0x2000:52c4
1000:dc1d  CMP byte ptr [0x6664],0x0
1000:dc22  JNZ 0x1000:dc35
1000:dc24  MOV DI,0xdb8c
1000:dc27  PUSH CS
1000:dc28  PUSH DI
1000:dc29  MOV DI,0x6664
1000:dc2c  PUSH DS
1000:dc2d  PUSH DI
1000:dc2e  PUSH 0x8
1000:dc30  CALLF 0x2000:8c7f
1000:dc35  JMP 0x1000:dc48
1000:dc37  MOV DI,0xdb8c
1000:dc3a  PUSH CS
1000:dc3b  PUSH DI
1000:dc3c  MOV DI,0x6664
1000:dc3f  PUSH DS
1000:dc40  PUSH DI
1000:dc41  PUSH 0x8
1000:dc43  CALLF 0x2000:8c7f
1000:dc48  MOV DI,0x6664
1000:dc4b  PUSH DS
1000:dc4c  PUSH DI
1000:dc4d  CALLF 0x2000:0b72
1000:dc52  MOV DI,0x672e
1000:dc55  PUSH DS
1000:dc56  PUSH DI
1000:dc57  MOV DI,0x65f2
1000:dc5a  PUSH DS
1000:dc5b  PUSH DI
1000:dc5c  PUSH 0xc
1000:dc5e  CALLF 0x2000:8c7f
1000:dc63  CMP byte ptr [0x66ec],0x0
1000:dc68  JNZ 0x1000:dc6f
1000:dc6a  PUSH 0x0
1000:dc6c  CALL 0x1000:a816
1000:dc6f  CMP byte ptr [0x6701],0x0
1000:dc74  JNZ 0x1000:dc7b
1000:dc76  PUSH 0x1
1000:dc78  CALL 0x1000:a816
1000:dc7b  MOV DI,0xdb92
1000:dc7e  PUSH CS
1000:dc7f  PUSH DI
1000:dc80  LES DI,[0x6678]
1000:dc84  PUSH ES
1000:dc85  PUSH DI
1000:dc86  PUSH 0xa
1000:dc88  PUSH 0x6c00
1000:dc8b  CALLF 0x2000:0a5e
1000:dc90  MOV DI,0xdb92
1000:dc93  PUSH CS
1000:dc94  PUSH DI
1000:dc95  LES DI,[0x667c]
1000:dc99  PUSH ES
1000:dc9a  PUSH DI
1000:dc9b  PUSH 0x6e0e
1000:dc9e  PUSH 0x18e2
1000:dca1  CALLF 0x2000:0a5e
1000:dca6  MOV DI,0xdb92
1000:dca9  PUSH CS
1000:dcaa  PUSH DI
1000:dcab  LES DI,[0x6680]
1000:dcaf  PUSH ES
1000:dcb0  PUSH DI
1000:dcb1  PUSH -0x790c
1000:dcb4  PUSH 0x1c0
1000:dcb7  CALLF 0x2000:0a5e
1000:dcbc  XOR AX,AX
1000:dcbe  MOV word ptr [BP + 0xfe7b],AX
1000:dcc2  JMP 0x1000:dcc8
1000:dcc4  INC word ptr [BP + 0xfe7b]
1000:dcc8  XOR AX,AX
1000:dcca  MOV word ptr [BP + 0xfe79],AX
1000:dcce  JMP 0x1000:dcd4
1000:dcd0  INC word ptr [BP + 0xfe79]
1000:dcd4  XOR AX,AX
1000:dcd6  MOV word ptr [BP + 0xfe77],AX
1000:dcda  JMP 0x1000:dce0
1000:dcdc  INC word ptr [BP + 0xfe77]
1000:dce0  MOV CX,word ptr [BP + 0xfe77]
1000:dce4  MOV AX,word ptr [BP + 0xfe79]
1000:dce8  SHL AX,0x4
1000:dceb  MOV DX,AX
1000:dced  MOV AX,word ptr [BP + 0xfe7b]
1000:dcf1  SHL AX,0x8
1000:dcf4  LES DI,[0x6678]
1000:dcf8  ADD DI,AX
1000:dcfa  ADD DI,DX
1000:dcfc  ADD DI,CX
1000:dcfe  MOV DL,byte ptr ES:[DI]
1000:dd01  MOV AX,word ptr [BP + 0xfe79]
1000:dd05  MOV DI,word ptr [BP + 0xfe77]
1000:dd09  SHL DI,0x4
1000:dd0c  ADD DI,AX
1000:dd0e  MOV byte ptr [BP + DI + 0xff00],DL
1000:dd12  CMP word ptr [BP + 0xfe77],0xf
1000:dd17  JNZ 0x1000:dcdc
1000:dd19  CMP word ptr [BP + 0xfe79],0xf
1000:dd1e  JNZ 0x1000:dcd0
1000:dd20  LEA DI,[BP + 0xff00]
1000:dd24  PUSH SS
1000:dd25  PUSH DI
1000:dd26  MOV AX,word ptr [BP + 0xfe7b]
1000:dd2a  SHL AX,0x8
1000:dd2d  LES DI,[0x6678]
1000:dd31  ADD DI,AX
1000:dd33  PUSH ES
1000:dd34  PUSH DI
1000:dd35  PUSH 0x100
1000:dd38  CALLF 0x2000:8b38
1000:dd3d  CMP word ptr [BP + 0xfe7b],0x6b
1000:dd42  JNZ 0x1000:dcc4
1000:dd44  XOR AX,AX
1000:dd46  MOV word ptr [BP + 0xfe7b],AX
1000:dd4a  JMP 0x1000:dd50
1000:dd4c  INC word ptr [BP + 0xfe7b]
1000:dd50  XOR AX,AX
1000:dd52  MOV word ptr [BP + 0xfe79],AX
1000:dd56  JMP 0x1000:dd5c
1000:dd58  INC word ptr [BP + 0xfe79]
1000:dd5c  XOR AX,AX
1000:dd5e  MOV word ptr [BP + 0xfe77],AX
1000:dd62  JMP 0x1000:dd68
1000:dd64  INC word ptr [BP + 0xfe77]
1000:dd68  MOV CX,word ptr [BP + 0xfe77]
1000:dd6c  IMUL AX,word ptr [BP + 0xfe79],0x7
1000:dd71  MOV DX,AX
1000:dd73  IMUL AX,word ptr [BP + 0xfe7b],0x31
1000:dd78  LES DI,[0x667c]
1000:dd7c  ADD DI,AX
1000:dd7e  ADD DI,DX
1000:dd80  ADD DI,CX
1000:dd82  MOV DL,byte ptr ES:[DI]
1000:dd85  MOV AX,word ptr [BP + 0xfe79]
1000:dd89  IMUL DI,word ptr [BP + 0xfe77],0x7
1000:dd8e  ADD DI,AX
1000:dd90  MOV byte ptr [BP + DI + 0xfecf],DL
1000:dd94  CMP word ptr [BP + 0xfe77],0x6
1000:dd99  JNZ 0x1000:dd64
1000:dd9b  CMP word ptr [BP + 0xfe79],0x6
1000:dda0  JNZ 0x1000:dd58
1000:dda2  LEA DI,[BP + 0xfecf]
1000:dda6  PUSH SS
1000:dda7  PUSH DI
1000:dda8  IMUL AX,word ptr [BP + 0xfe7b],0x31
1000:ddad  LES DI,[0x667c]
1000:ddb1  ADD DI,AX
1000:ddb3  PUSH ES
1000:ddb4  PUSH DI
1000:ddb5  PUSH 0x31
1000:ddb7  CALLF 0x2000:8b38
1000:ddbc  CMP word ptr [BP + 0xfe7b],0x81
1000:ddc2  JNZ 0x1000:dd4c
1000:ddc4  XOR AX,AX
1000:ddc6  MOV word ptr [BP + 0xfe7b],AX
1000:ddca  JMP 0x1000:ddd0
1000:ddcc  INC word ptr [BP + 0xfe7b]
1000:ddd0  XOR AX,AX
1000:ddd2  MOV word ptr [BP + 0xfe79],AX
1000:ddd6  JMP 0x1000:dddc
1000:ddd8  INC word ptr [BP + 0xfe79]
1000:dddc  XOR AX,AX
1000:ddde  MOV word ptr [BP + 0xfe77],AX
1000:dde2  JMP 0x1000:dde8
1000:dde4  INC word ptr [BP + 0xfe77]
1000:dde8  MOV CX,word ptr [BP + 0xfe77]
1000:ddec  MOV AX,word ptr [BP + 0xfe79]
1000:ddf0  SHL AX,0x2
1000:ddf3  MOV DX,AX
1000:ddf5  MOV AX,word ptr [BP + 0xfe7b]
1000:ddf9  SHL AX,0x4
1000:ddfc  LES DI,[0x6680]
1000:de00  ADD DI,AX
1000:de02  ADD DI,DX
1000:de04  ADD DI,CX
1000:de06  MOV DL,byte ptr ES:[DI]
1000:de09  MOV AX,word ptr [BP + 0xfe79]
1000:de0d  MOV DI,word ptr [BP + 0xfe77]
1000:de11  SHL DI,0x2
1000:de14  ADD DI,AX
1000:de16  MOV byte ptr [BP + DI + 0xfe7f],DL
1000:de1a  CMP word ptr [BP + 0xfe77],0x3
1000:de1f  JNZ 0x1000:dde4
1000:de21  CMP word ptr [BP + 0xfe79],0x3
1000:de26  JNZ 0x1000:ddd8
1000:de28  LEA DI,[BP + 0xfe7f]
1000:de2c  PUSH SS
1000:de2d  PUSH DI
1000:de2e  MOV AX,word ptr [BP + 0xfe7b]
1000:de32  SHL AX,0x4
1000:de35  LES DI,[0x6680]
1000:de39  ADD DI,AX
1000:de3b  PUSH ES
1000:de3c  PUSH DI
1000:de3d  PUSH 0x10
1000:de3f  CALLF 0x2000:8b38
1000:de44  CMP word ptr [BP + 0xfe7b],0x1b
1000:de49  JNZ 0x1000:ddcc
1000:de4b  XOR AX,AX
1000:de4d  MOV word ptr [BP + 0xfe79],AX
1000:de51  JMP 0x1000:de57
1000:de53  INC word ptr [BP + 0xfe79]
1000:de57  XOR AX,AX
1000:de59  MOV word ptr [BP + 0xfe77],AX
1000:de5d  JMP 0x1000:de63
1000:de5f  INC word ptr [BP + 0xfe77]
1000:de63  PUSH 0x4
1000:de65  CALLF 0x2000:9424
1000:de6a  ADD AX,0xa0
1000:de6d  MOV CL,AL
1000:de6f  MOV DX,word ptr [BP + 0xfe77]
1000:de73  MOV AX,word ptr [BP + 0xfe79]
1000:de77  SHL AX,0x4
1000:de7a  LES DI,[0x6678]
1000:de7e  ADD DI,AX
1000:de80  ADD DI,DX
1000:de82  MOV byte ptr ES:[DI + 0x4900],CL
1000:de87  PUSH 0x4
1000:de89  CALLF 0x2000:9424
1000:de8e  ADD AX,0xa0
1000:de91  MOV CL,AL
1000:de93  MOV DX,word ptr [BP + 0xfe77]
1000:de97  MOV AX,word ptr [BP + 0xfe79]
1000:de9b  SHL AX,0x4
1000:de9e  LES DI,[0x6678]
1000:dea2  ADD DI,AX
1000:dea4  ADD DI,DX
1000:dea6  MOV byte ptr ES:[DI + 0x4a00],CL
1000:deab  PUSH 0x4
1000:dead  CALLF 0x2000:9424
1000:deb2  ADD AX,0xc
1000:deb5  MOV CL,AL
1000:deb7  MOV DX,word ptr [BP + 0xfe77]
1000:debb  MOV AX,word ptr [BP + 0xfe79]
1000:debf  SHL AX,0x4
1000:dec2  LES DI,[0x6678]
1000:dec6  ADD DI,AX
1000:dec8  ADD DI,DX
1000:deca  MOV byte ptr ES:[DI + 0x5700],CL
1000:decf  PUSH 0x4
1000:ded1  CALLF 0x2000:9424
1000:ded6  ADD AX,0xc
1000:ded9  MOV CL,AL
1000:dedb  MOV DX,word ptr [BP + 0xfe77]
1000:dedf  MOV AX,word ptr [BP + 0xfe79]
1000:dee3  SHL AX,0x4
1000:dee6  LES DI,[0x6678]
1000:deea  ADD DI,AX
1000:deec  ADD DI,DX
1000:deee  MOV byte ptr ES:[DI + 0x5800],CL
1000:def3  PUSH 0x4
1000:def5  CALLF 0x2000:9424
1000:defa  ADD AX,0x5e
1000:defd  MOV CL,AL
1000:deff  MOV DX,word ptr [BP + 0xfe77]
1000:df03  MOV AX,word ptr [BP + 0xfe79]
1000:df07  SHL AX,0x4
1000:df0a  LES DI,[0x6678]
1000:df0e  ADD DI,AX
1000:df10  ADD DI,DX
1000:df12  MOV byte ptr ES:[DI + 0x5200],CL
1000:df17  PUSH 0x4
1000:df19  CALLF 0x2000:9424
1000:df1e  ADD AX,0x5e
1000:df21  MOV CL,AL
1000:df23  MOV DX,word ptr [BP + 0xfe77]
1000:df27  MOV AX,word ptr [BP + 0xfe79]
1000:df2b  SHL AX,0x4
1000:df2e  LES DI,[0x6678]
1000:df32  ADD DI,AX
1000:df34  ADD DI,DX
1000:df36  MOV byte ptr ES:[DI + 0x5300],CL
1000:df3b  CMP word ptr [BP + 0xfe77],0xf
1000:df40  JZ 0x1000:df45
1000:df42  JMP 0x1000:de5f
1000:df45  CMP word ptr [BP + 0xfe79],0xf
1000:df4a  JZ 0x1000:df4f
1000:df4c  JMP 0x1000:de53
1000:df4f  CALLF 0x2000:94b9
1000:df54  LEAVE
1000:df55  RET
