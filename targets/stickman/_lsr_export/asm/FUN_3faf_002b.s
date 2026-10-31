; FUN_3faf_002b  entry=3faf:002b size=722
3faf:002b  PUSH BP
3faf:002c  MOV BP,SP
3faf:002e  MOV AX,0x402
3faf:0031  CALLF 0x4000:302f
3faf:0036  SUB SP,0x402
3faf:003a  LES DI,[BP + 0x6]
3faf:003d  PUSH ES
3faf:003e  PUSH DI
3faf:003f  LEA DI,[BP + 0xfefe]
3faf:0043  PUSH SS
3faf:0044  PUSH DI
3faf:0045  MOV AX,0xff
3faf:0048  PUSH AX
3faf:0049  CALLF 0x4000:372e
3faf:004e  LEA DI,[BP + 0xfefe]
3faf:0052  PUSH SS
3faf:0053  PUSH DI
3faf:0054  CALLF 0x4000:1702
3faf:0059  OR AL,AL
3faf:005b  JNZ 0x3000:fbc1
3faf:005d  CMP byte ptr [BP + 0xfefe],0x0
3faf:0062  JZ 0x3000:fb97
3faf:0064  MOV AL,byte ptr [BP + 0xfefe]
3faf:0068  XOR AH,AH
3faf:006a  MOV DI,AX
3faf:006c  MOV AL,byte ptr [BP + DI + 0xfefe]
3faf:0070  PUSH AX
3faf:0071  MOV DI,0x0
3faf:0074  PUSH CS
3faf:0075  PUSH DI
3faf:0076  CALLF 0x4000:39c9
3faf:007b  JNZ 0x3000:fb97
3faf:007d  LEA DI,[BP + 0xfbfe]
3faf:0081  PUSH SS
3faf:0082  PUSH DI
3faf:0083  LEA DI,[BP + 0xfefe]
3faf:0087  PUSH SS
3faf:0088  PUSH DI
3faf:0089  CALLF 0x4000:3714
3faf:008e  MOV DI,0x20
3faf:0091  PUSH CS
3faf:0092  PUSH DI
3faf:0093  CALLF 0x4000:37a1
3faf:0098  LEA DI,[BP + 0xfefe]
3faf:009c  PUSH SS
3faf:009d  PUSH DI
3faf:009e  MOV AX,0xff
3faf:00a1  PUSH AX
3faf:00a2  CALLF 0x4000:372e
3faf:00a7  LEA DI,[BP + 0xfbfe]
3faf:00ab  PUSH SS
3faf:00ac  PUSH DI
3faf:00ad  LEA DI,[BP + 0xfefe]
3faf:00b1  PUSH SS
3faf:00b2  PUSH DI
3faf:00b3  CALLF 0x4000:3714
3faf:00b8  MOV DI,0x22
3faf:00bb  PUSH CS
3faf:00bc  PUSH DI
3faf:00bd  CALLF 0x4000:37a1
3faf:00c2  LEA DI,[BP + 0xfefe]
3faf:00c6  PUSH SS
3faf:00c7  PUSH DI
3faf:00c8  MOV AX,0xff
3faf:00cb  PUSH AX
3faf:00cc  CALLF 0x4000:372e
3faf:00d1  MOV byte ptr [BP + -0x1],0x0
3faf:00d5  LEA DI,[BP + 0xfcfe]
3faf:00d9  PUSH SS
3faf:00da  PUSH DI
3faf:00db  LEA DI,[BP + 0xfefe]
3faf:00df  PUSH SS
3faf:00e0  PUSH DI
3faf:00e1  CALLF 0x4000:3045
3faf:00e6  LEA DI,[BP + 0xfcfe]
3faf:00ea  PUSH SS
3faf:00eb  PUSH DI
3faf:00ec  CALLF 0x4000:30b5
3faf:00f1  LEA DI,[BP + 0xfcfe]
3faf:00f5  PUSH SS
3faf:00f6  PUSH DI
3faf:00f7  LEA DI,[BP + 0xfdfe]
3faf:00fb  PUSH SS
3faf:00fc  PUSH DI
3faf:00fd  MOV AX,0xff
3faf:0100  PUSH AX
3faf:0101  CALLF 0x4000:342f
3faf:0106  CALLF 0x4000:336a
3faf:010b  MOV AL,byte ptr [BP + 0xfe02]
3faf:010f  XOR AH,AH
3faf:0111  SUB AX,0x30
3faf:0114  MOV [0xa8e2],AL
3faf:0117  LEA DI,[BP + 0xfcfe]
3faf:011b  PUSH SS
3faf:011c  PUSH DI
3faf:011d  CALLF 0x4000:34a5
3faf:0122  MOV [0xa8e3],AX
3faf:0125  MOV word ptr [0xa8e5],DX
3faf:0129  CALLF 0x4000:336a
3faf:012e  LEA DI,[BP + 0xfcfe]
3faf:0132  PUSH SS
3faf:0133  PUSH DI
3faf:0134  LEA DI,[BP + 0xfdfe]
3faf:0138  PUSH SS
3faf:0139  PUSH DI
3faf:013a  MOV AX,0xff
3faf:013d  PUSH AX
3faf:013e  CALLF 0x4000:342f
3faf:0143  CALLF 0x4000:336a
3faf:0148  LEA DI,[BP + 0xfcfe]
3faf:014c  PUSH SS
3faf:014d  PUSH DI
3faf:014e  CALLF 0x4000:34a5
3faf:0153  MOV [0xa8e7],AL
3faf:0156  CALLF 0x4000:336a
3faf:015b  LEA DI,[BP + 0xfcfe]
3faf:015f  PUSH SS
3faf:0160  PUSH DI
3faf:0161  MOV DI,0xa8e8
3faf:0164  PUSH DS
3faf:0165  PUSH DI
3faf:0166  MOV AX,0xff
3faf:0169  PUSH AX
3faf:016a  CALLF 0x4000:342f
3faf:016f  CALLF 0x4000:336a
3faf:0174  LEA DI,[BP + 0xfcfe]
3faf:0178  PUSH SS
3faf:0179  PUSH DI
3faf:017a  LEA DI,[BP + 0xfdfe]
3faf:017e  PUSH SS
3faf:017f  PUSH DI
3faf:0180  MOV AX,0xff
3faf:0183  PUSH AX
3faf:0184  CALLF 0x4000:342f
3faf:0189  CALLF 0x4000:336a
3faf:018e  LEA DI,[BP + 0xfcfe]
3faf:0192  PUSH SS
3faf:0193  PUSH DI
3faf:0194  LEA DI,[BP + 0xfdfe]
3faf:0198  PUSH SS
3faf:0199  PUSH DI
3faf:019a  MOV AX,0xff
3faf:019d  PUSH AX
3faf:019e  CALLF 0x4000:342f
3faf:01a3  CALLF 0x4000:336a
3faf:01a8  LEA DI,[BP + 0xfcfe]
3faf:01ac  PUSH SS
3faf:01ad  PUSH DI
3faf:01ae  LEA DI,[BP + 0xfdfe]
3faf:01b2  PUSH SS
3faf:01b3  PUSH DI
3faf:01b4  MOV AX,0xff
3faf:01b7  PUSH AX
3faf:01b8  CALLF 0x4000:342f
3faf:01bd  CALLF 0x4000:336a
3faf:01c2  LEA DI,[BP + 0xfcfe]
3faf:01c6  PUSH SS
3faf:01c7  PUSH DI
3faf:01c8  LEA DI,[BP + 0xfdfe]
3faf:01cc  PUSH SS
3faf:01cd  PUSH DI
3faf:01ce  MOV AX,0xff
3faf:01d1  PUSH AX
3faf:01d2  CALLF 0x4000:342f
3faf:01d7  CALLF 0x4000:336a
3faf:01dc  LEA DI,[BP + 0xfcfe]
3faf:01e0  PUSH SS
3faf:01e1  PUSH DI
3faf:01e2  MOV DI,0xa9e8
3faf:01e5  PUSH DS
3faf:01e6  PUSH DI
3faf:01e7  MOV AX,0xff
3faf:01ea  PUSH AX
3faf:01eb  CALLF 0x4000:342f
3faf:01f0  CALLF 0x4000:336a
3faf:01f5  LEA DI,[BP + 0xfcfe]
3faf:01f9  PUSH SS
3faf:01fa  PUSH DI
3faf:01fb  LEA DI,[BP + 0xfdfe]
3faf:01ff  PUSH SS
3faf:0200  PUSH DI
3faf:0201  MOV AX,0xff
3faf:0204  PUSH AX
3faf:0205  CALLF 0x4000:342f
3faf:020a  CALLF 0x4000:336a
3faf:020f  LEA DI,[BP + 0xfcfe]
3faf:0213  PUSH SS
3faf:0214  PUSH DI
3faf:0215  LEA DI,[BP + 0xfdfe]
3faf:0219  PUSH SS
3faf:021a  PUSH DI
3faf:021b  MOV AX,0xff
3faf:021e  PUSH AX
3faf:021f  CALLF 0x4000:342f
3faf:0224  CALLF 0x4000:336a
3faf:0229  LEA DI,[BP + 0xfcfe]
3faf:022d  PUSH SS
3faf:022e  PUSH DI
3faf:022f  LEA DI,[BP + 0xfdfe]
3faf:0233  PUSH SS
3faf:0234  PUSH DI
3faf:0235  MOV AX,0xff
3faf:0238  PUSH AX
3faf:0239  CALLF 0x4000:342f
3faf:023e  CALLF 0x4000:336a
3faf:0243  LEA DI,[BP + 0xfcfe]
3faf:0247  PUSH SS
3faf:0248  PUSH DI
3faf:0249  LEA DI,[BP + 0xfdfe]
3faf:024d  PUSH SS
3faf:024e  PUSH DI
3faf:024f  MOV AX,0xff
3faf:0252  PUSH AX
3faf:0253  CALLF 0x4000:342f
3faf:0258  CALLF 0x4000:336a
3faf:025d  LEA DI,[BP + 0xfcfe]
3faf:0261  PUSH SS
3faf:0262  PUSH DI
3faf:0263  LEA DI,[BP + 0xfdfe]
3faf:0267  PUSH SS
3faf:0268  PUSH DI
3faf:0269  MOV AX,0xff
3faf:026c  PUSH AX
3faf:026d  CALLF 0x4000:342f
3faf:0272  CALLF 0x4000:336a
3faf:0277  LEA DI,[BP + 0xfcfe]
3faf:027b  PUSH SS
3faf:027c  PUSH DI
3faf:027d  LEA DI,[BP + 0xfdfe]
3faf:0281  PUSH SS
3faf:0282  PUSH DI
3faf:0283  MOV AX,0xff
3faf:0286  PUSH AX
3faf:0287  CALLF 0x4000:342f
3faf:028c  CALLF 0x4000:336a
3faf:0291  LEA DI,[BP + 0xfcfe]
3faf:0295  PUSH SS
3faf:0296  PUSH DI
3faf:0297  LEA DI,[BP + 0xfdfe]
3faf:029b  PUSH SS
3faf:029c  PUSH DI
3faf:029d  MOV AX,0xff
3faf:02a0  PUSH AX
3faf:02a1  CALLF 0x4000:342f
3faf:02a6  CALLF 0x4000:336a
3faf:02ab  LEA DI,[BP + 0xfcfe]
3faf:02af  PUSH SS
3faf:02b0  PUSH DI
3faf:02b1  LEA DI,[BP + 0xfdfe]
3faf:02b5  PUSH SS
3faf:02b6  PUSH DI
3faf:02b7  MOV AX,0xff
3faf:02ba  PUSH AX
3faf:02bb  CALLF 0x4000:342f
3faf:02c0  CALLF 0x4000:336a
3faf:02c5  LEA DI,[BP + 0xfcfe]
3faf:02c9  PUSH SS
3faf:02ca  PUSH DI
3faf:02cb  CALLF 0x4000:34a5
3faf:02d0  MOV [0xaae8],AX
3faf:02d3  MOV word ptr [0xaaea],DX
3faf:02d7  CALLF 0x4000:336a
3faf:02dc  LEA DI,[BP + 0xfcfe]
3faf:02e0  PUSH SS
3faf:02e1  PUSH DI
3faf:02e2  CALLF 0x4000:310f
3faf:02e7  CALLF 0x4000:2ff2
3faf:02ec  OR AX,AX
3faf:02ee  JNZ 0x3000:fde4
3faf:02f0  MOV byte ptr [BP + -0x1],0x1
3faf:02f4  MOV AL,byte ptr [BP + -0x1]
3faf:02f7  MOV SP,BP
3faf:02f9  POP BP
3faf:02fa  RETF 0x4
