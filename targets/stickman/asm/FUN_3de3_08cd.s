; FUN_3de3_08cd  entry=3de3:08cd size=325
3de3:08cd  PUSH BP
3de3:08ce  MOV BP,SP
3de3:08d0  MOV AX,0x12
3de3:08d3  CALLF 0x4000:302f
3de3:08d8  SUB SP,0x12
3de3:08db  LEA DI,[BP + -0xc]
3de3:08de  PUSH SS
3de3:08df  PUSH DI
3de3:08e0  LEA DI,[BP + -0xa]
3de3:08e3  PUSH SS
3de3:08e4  PUSH DI
3de3:08e5  LEA DI,[BP + -0x8]
3de3:08e8  PUSH SS
3de3:08e9  PUSH DI
3de3:08ea  LEA DI,[BP + -0x2]
3de3:08ed  PUSH SS
3de3:08ee  PUSH DI
3de3:08ef  CALLF 0x4000:2992
3de3:08f4  LEA DI,[BP + -0x12]
3de3:08f7  PUSH SS
3de3:08f8  PUSH DI
3de3:08f9  LEA DI,[BP + -0x10]
3de3:08fc  PUSH SS
3de3:08fd  PUSH DI
3de3:08fe  LEA DI,[BP + -0xe]
3de3:0901  PUSH SS
3de3:0902  PUSH DI
3de3:0903  LEA DI,[BP + -0x2]
3de3:0906  PUSH SS
3de3:0907  PUSH DI
3de3:0908  CALLF 0x4000:295c
3de3:090d  MOV AX,word ptr [BP + -0x12]
3de3:0910  SUB AX,0x76c
3de3:0913  MOV word ptr [BP + -0x12],AX
3de3:0916  MOV AX,word ptr [BP + -0x12]
3de3:0919  XOR DX,DX
3de3:091b  MOV word ptr [BP + -0x6],AX
3de3:091e  MOV word ptr [BP + -0x4],DX
3de3:0921  MOV AX,word ptr [BP + -0x6]
3de3:0924  MOV DX,word ptr [BP + -0x4]
3de3:0927  MOV CX,0xc
3de3:092a  XOR BX,BX
3de3:092c  CALLF 0x4000:3664
3de3:0931  MOV word ptr [BP + -0x6],AX
3de3:0934  MOV word ptr [BP + -0x4],DX
3de3:0937  MOV AX,word ptr [BP + -0x10]
3de3:093a  XOR DX,DX
3de3:093c  ADD AX,word ptr [BP + -0x6]
3de3:093f  ADC DX,word ptr [BP + -0x4]
3de3:0942  MOV word ptr [BP + -0x6],AX
3de3:0945  MOV word ptr [BP + -0x4],DX
3de3:0948  MOV AX,word ptr [BP + -0x6]
3de3:094b  MOV DX,word ptr [BP + -0x4]
3de3:094e  MOV CX,0x1f
3de3:0951  XOR BX,BX
3de3:0953  CALLF 0x4000:3664
3de3:0958  MOV word ptr [BP + -0x6],AX
3de3:095b  MOV word ptr [BP + -0x4],DX
3de3:095e  MOV AX,word ptr [BP + -0xe]
3de3:0961  XOR DX,DX
3de3:0963  ADD AX,word ptr [BP + -0x6]
3de3:0966  ADC DX,word ptr [BP + -0x4]
3de3:0969  MOV word ptr [BP + -0x6],AX
3de3:096c  MOV word ptr [BP + -0x4],DX
3de3:096f  MOV AX,word ptr [BP + -0x6]
3de3:0972  MOV DX,word ptr [BP + -0x4]
3de3:0975  MOV CX,0x18
3de3:0978  XOR BX,BX
3de3:097a  CALLF 0x4000:3664
3de3:097f  MOV word ptr [BP + -0x6],AX
3de3:0982  MOV word ptr [BP + -0x4],DX
3de3:0985  MOV AX,word ptr [BP + -0xc]
3de3:0988  XOR DX,DX
3de3:098a  ADD AX,word ptr [BP + -0x6]
3de3:098d  ADC DX,word ptr [BP + -0x4]
3de3:0990  MOV word ptr [BP + -0x6],AX
3de3:0993  MOV word ptr [BP + -0x4],DX
3de3:0996  MOV AX,word ptr [BP + -0x6]
3de3:0999  MOV DX,word ptr [BP + -0x4]
3de3:099c  MOV CX,0x3c
3de3:099f  XOR BX,BX
3de3:09a1  CALLF 0x4000:3664
3de3:09a6  MOV word ptr [BP + -0x6],AX
3de3:09a9  MOV word ptr [BP + -0x4],DX
3de3:09ac  MOV AX,word ptr [BP + -0xa]
3de3:09af  XOR DX,DX
3de3:09b1  ADD AX,word ptr [BP + -0x6]
3de3:09b4  ADC DX,word ptr [BP + -0x4]
3de3:09b7  MOV word ptr [BP + -0x6],AX
3de3:09ba  MOV word ptr [BP + -0x4],DX
3de3:09bd  MOV AX,word ptr [BP + -0x6]
3de3:09c0  MOV DX,word ptr [BP + -0x4]
3de3:09c3  MOV CX,0x3c
3de3:09c6  XOR BX,BX
3de3:09c8  CALLF 0x4000:3664
3de3:09cd  MOV word ptr [BP + -0x6],AX
3de3:09d0  MOV word ptr [BP + -0x4],DX
3de3:09d3  MOV AX,word ptr [BP + -0x8]
3de3:09d6  XOR DX,DX
3de3:09d8  ADD AX,word ptr [BP + -0x6]
3de3:09db  ADC DX,word ptr [BP + -0x4]
3de3:09de  MOV word ptr [BP + -0x6],AX
3de3:09e1  MOV word ptr [BP + -0x4],DX
3de3:09e4  MOV AX,word ptr [BP + -0x6]
3de3:09e7  MOV DX,word ptr [BP + -0x4]
3de3:09ea  CMP DX,word ptr [0xa7c8]
3de3:09ee  JG 0x3000:e828
3de3:09f0  JL 0x3000:e831
3de3:09f2  CMP AX,word ptr [0xa7c6]
3de3:09f6  JBE 0x3000:e831
3de3:09f8  MOV DI,0x8bb
3de3:09fb  PUSH CS
3de3:09fc  PUSH DI
3de3:09fd  PUSH CS
3de3:09fe  CALL 0x3000:e0a8
3de3:0a01  PUSH CS
3de3:0a02  CALL 0x3000:e225
3de3:0a05  LEA DI,[BP + -0x12]
3de3:0a08  PUSH SS
3de3:0a09  PUSH DI
3de3:0a0a  PUSH CS
3de3:0a0b  CALL 0x3000:e3e6
3de3:0a0e  MOV SP,BP
3de3:0a10  POP BP
3de3:0a11  RETF
