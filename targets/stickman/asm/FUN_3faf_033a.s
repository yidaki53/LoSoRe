; FUN_3faf_033a  entry=3faf:033a size=747
3faf:033a  PUSH BP
3faf:033b  MOV BP,SP
3faf:033d  MOV AX,0x502
3faf:0340  CALLF 0x4000:302f
3faf:0345  SUB SP,0x502
3faf:0349  LES DI,[BP + 0x6]
3faf:034c  PUSH ES
3faf:034d  PUSH DI
3faf:034e  LEA DI,[BP + 0xfefe]
3faf:0352  PUSH SS
3faf:0353  PUSH DI
3faf:0354  MOV AX,0xff
3faf:0357  PUSH AX
3faf:0358  CALLF 0x4000:372e
3faf:035d  LEA DI,[BP + 0xfefe]
3faf:0361  PUSH SS
3faf:0362  PUSH DI
3faf:0363  CALLF 0x4000:1702
3faf:0368  OR AL,AL
3faf:036a  JZ 0x3000:fe5f
3faf:036c  JMP 0x3000:ff23
3faf:036f  CMP byte ptr [BP + 0xfefe],0x0
3faf:0374  JZ 0x3000:fea9
3faf:0376  MOV AL,byte ptr [BP + 0xfefe]
3faf:037a  XOR AH,AH
3faf:037c  MOV DI,AX
3faf:037e  MOV AL,byte ptr [BP + DI + 0xfefe]
3faf:0382  PUSH AX
3faf:0383  MOV DI,0x2fd
3faf:0386  PUSH CS
3faf:0387  PUSH DI
3faf:0388  CALLF 0x4000:39c9
3faf:038d  JNZ 0x3000:fea9
3faf:038f  LEA DI,[BP + 0xfbfe]
3faf:0393  PUSH SS
3faf:0394  PUSH DI
3faf:0395  LEA DI,[BP + 0xfefe]
3faf:0399  PUSH SS
3faf:039a  PUSH DI
3faf:039b  CALLF 0x4000:3714
3faf:03a0  MOV DI,0x31d
3faf:03a3  PUSH CS
3faf:03a4  PUSH DI
3faf:03a5  CALLF 0x4000:37a1
3faf:03aa  LEA DI,[BP + 0xfefe]
3faf:03ae  PUSH SS
3faf:03af  PUSH DI
3faf:03b0  MOV AX,0xff
3faf:03b3  PUSH AX
3faf:03b4  CALLF 0x4000:372e
3faf:03b9  LEA DI,[BP + 0xfbfe]
3faf:03bd  PUSH SS
3faf:03be  PUSH DI
3faf:03bf  LEA DI,[BP + 0xfefe]
3faf:03c3  PUSH SS
3faf:03c4  PUSH DI
3faf:03c5  CALLF 0x4000:3714
3faf:03ca  MOV DI,0x31f
3faf:03cd  PUSH CS
3faf:03ce  PUSH DI
3faf:03cf  CALLF 0x4000:37a1
3faf:03d4  CALLF 0x4000:1702
3faf:03d9  OR AL,AL
3faf:03db  JZ 0x3000:fef9
3faf:03dd  LEA DI,[BP + 0xfafe]
3faf:03e1  PUSH SS
3faf:03e2  PUSH DI
3faf:03e3  LEA DI,[BP + 0xfefe]
3faf:03e7  PUSH SS
3faf:03e8  PUSH DI
3faf:03e9  CALLF 0x4000:3714
3faf:03ee  MOV DI,0x31f
3faf:03f1  PUSH CS
3faf:03f2  PUSH DI
3faf:03f3  CALLF 0x4000:37a1
3faf:03f8  LEA DI,[BP + 0xfefe]
3faf:03fc  PUSH SS
3faf:03fd  PUSH DI
3faf:03fe  MOV AX,0xff
3faf:0401  PUSH AX
3faf:0402  CALLF 0x4000:372e
3faf:0407  JMP 0x3000:ff23
3faf:0409  LEA DI,[BP + 0xfafe]
3faf:040d  PUSH SS
3faf:040e  PUSH DI
3faf:040f  LEA DI,[BP + 0xfefe]
3faf:0413  PUSH SS
3faf:0414  PUSH DI
3faf:0415  CALLF 0x4000:3714
3faf:041a  MOV DI,0x32b
3faf:041d  PUSH CS
3faf:041e  PUSH DI
3faf:041f  CALLF 0x4000:37a1
3faf:0424  LEA DI,[BP + 0xfefe]
3faf:0428  PUSH SS
3faf:0429  PUSH DI
3faf:042a  MOV AX,0xff
3faf:042d  PUSH AX
3faf:042e  CALLF 0x4000:372e
3faf:0433  MOV byte ptr [BP + -0x1],0x0
3faf:0437  LEA DI,[BP + 0xfcfe]
3faf:043b  PUSH SS
3faf:043c  PUSH DI
3faf:043d  LEA DI,[BP + 0xfefe]
3faf:0441  PUSH SS
3faf:0442  PUSH DI
3faf:0443  CALLF 0x4000:3045
3faf:0448  LEA DI,[BP + 0xfcfe]
3faf:044c  PUSH SS
3faf:044d  PUSH DI
3faf:044e  CALLF 0x4000:30b5
3faf:0453  LEA DI,[BP + 0xfcfe]
3faf:0457  PUSH SS
3faf:0458  PUSH DI
3faf:0459  LEA DI,[BP + 0xfdfe]
3faf:045d  PUSH SS
3faf:045e  PUSH DI
3faf:045f  MOV AX,0xff
3faf:0462  PUSH AX
3faf:0463  CALLF 0x4000:342f
3faf:0468  CALLF 0x4000:336a
3faf:046d  LEA DI,[BP + 0xfcfe]
3faf:0471  PUSH SS
3faf:0472  PUSH DI
3faf:0473  LEA DI,[BP + 0xfdfe]
3faf:0477  PUSH SS
3faf:0478  PUSH DI
3faf:0479  MOV AX,0xff
3faf:047c  PUSH AX
3faf:047d  CALLF 0x4000:342f
3faf:0482  CALLF 0x4000:336a
3faf:0487  LEA DI,[BP + 0xfcfe]
3faf:048b  PUSH SS
3faf:048c  PUSH DI
3faf:048d  LEA DI,[BP + 0xfdfe]
3faf:0491  PUSH SS
3faf:0492  PUSH DI
3faf:0493  MOV AX,0xff
3faf:0496  PUSH AX
3faf:0497  CALLF 0x4000:342f
3faf:049c  CALLF 0x4000:336a
3faf:04a1  LEA DI,[BP + 0xfcfe]
3faf:04a5  PUSH SS
3faf:04a6  PUSH DI
3faf:04a7  LEA DI,[BP + 0xfdfe]
3faf:04ab  PUSH SS
3faf:04ac  PUSH DI
3faf:04ad  MOV AX,0xff
3faf:04b0  PUSH AX
3faf:04b1  CALLF 0x4000:342f
3faf:04b6  CALLF 0x4000:336a
3faf:04bb  MOV AL,byte ptr [BP + 0xfe02]
3faf:04bf  XOR AH,AH
3faf:04c1  SUB AX,0x30
3faf:04c4  MOV [0xa8e2],AL
3faf:04c7  LEA DI,[BP + 0xfcfe]
3faf:04cb  PUSH SS
3faf:04cc  PUSH DI
3faf:04cd  CALLF 0x4000:34a5
3faf:04d2  MOV [0xa8e3],AX
3faf:04d5  MOV word ptr [0xa8e5],DX
3faf:04d9  CALLF 0x4000:33bc
3faf:04de  LEA DI,[BP + 0xfcfe]
3faf:04e2  PUSH SS
3faf:04e3  PUSH DI
3faf:04e4  CALLF 0x4000:336a
3faf:04e9  LEA DI,[BP + 0xfcfe]
3faf:04ed  PUSH SS
3faf:04ee  PUSH DI
3faf:04ef  LEA DI,[BP + 0xfdfe]
3faf:04f3  PUSH SS
3faf:04f4  PUSH DI
3faf:04f5  MOV AX,0xff
3faf:04f8  PUSH AX
3faf:04f9  CALLF 0x4000:342f
3faf:04fe  CALLF 0x4000:336a
3faf:0503  LEA DI,[BP + 0xfcfe]
3faf:0507  PUSH SS
3faf:0508  PUSH DI
3faf:0509  MOV DI,0xa9e8
3faf:050c  PUSH DS
3faf:050d  PUSH DI
3faf:050e  MOV AX,0xff
3faf:0511  PUSH AX
3faf:0512  CALLF 0x4000:342f
3faf:0517  CALLF 0x4000:336a
3faf:051c  LEA DI,[BP + 0xfcfe]
3faf:0520  PUSH SS
3faf:0521  PUSH DI
3faf:0522  LEA DI,[BP + 0xfdfe]
3faf:0526  PUSH SS
3faf:0527  PUSH DI
3faf:0528  MOV AX,0xff
3faf:052b  PUSH AX
3faf:052c  CALLF 0x4000:342f
3faf:0531  CALLF 0x4000:336a
3faf:0536  LEA DI,[BP + 0xfbfe]
3faf:053a  PUSH SS
3faf:053b  PUSH DI
3faf:053c  MOV DI,0xa9e8
3faf:053f  PUSH DS
3faf:0540  PUSH DI
3faf:0541  CALLF 0x4000:3714
3faf:0546  MOV DI,0x338
3faf:0549  PUSH CS
3faf:054a  PUSH DI
3faf:054b  CALLF 0x4000:37a1
3faf:0550  LEA DI,[BP + 0xfdfe]
3faf:0554  PUSH SS
3faf:0555  PUSH DI
3faf:0556  CALLF 0x4000:37a1
3faf:055b  MOV DI,0xa9e8
3faf:055e  PUSH DS
3faf:055f  PUSH DI
3faf:0560  MOV AX,0xff
3faf:0563  PUSH AX
3faf:0564  CALLF 0x4000:372e
3faf:0569  LEA DI,[BP + 0xfcfe]
3faf:056d  PUSH SS
3faf:056e  PUSH DI
3faf:056f  LEA DI,[BP + 0xfdfe]
3faf:0573  PUSH SS
3faf:0574  PUSH DI
3faf:0575  MOV AX,0xff
3faf:0578  PUSH AX
3faf:0579  CALLF 0x4000:342f
3faf:057e  CALLF 0x4000:336a
3faf:0583  LEA DI,[BP + 0xfcfe]
3faf:0587  PUSH SS
3faf:0588  PUSH DI
3faf:0589  LEA DI,[BP + 0xfdfe]
3faf:058d  PUSH SS
3faf:058e  PUSH DI
3faf:058f  MOV AX,0xff
3faf:0592  PUSH AX
3faf:0593  CALLF 0x4000:342f
3faf:0598  CALLF 0x4000:336a
3faf:059d  LEA DI,[BP + 0xfcfe]
3faf:05a1  PUSH SS
3faf:05a2  PUSH DI
3faf:05a3  LEA DI,[BP + 0xfdfe]
3faf:05a7  PUSH SS
3faf:05a8  PUSH DI
3faf:05a9  MOV AX,0xff
3faf:05ac  PUSH AX
3faf:05ad  CALLF 0x4000:342f
3faf:05b2  CALLF 0x4000:336a
3faf:05b7  LEA DI,[BP + 0xfcfe]
3faf:05bb  PUSH SS
3faf:05bc  PUSH DI
3faf:05bd  CALLF 0x4000:34a5
3faf:05c2  MOV [0xaae8],AX
3faf:05c5  MOV word ptr [0xaaea],DX
3faf:05c9  CALLF 0x4000:336a
3faf:05ce  LEA DI,[BP + 0xfcfe]
3faf:05d2  PUSH SS
3faf:05d3  PUSH DI
3faf:05d4  CALLF 0x4000:34a5
3faf:05d9  MOV [0xa8e7],AL
3faf:05dc  CALLF 0x4000:336a
3faf:05e1  LEA DI,[BP + 0xfcfe]
3faf:05e5  PUSH SS
3faf:05e6  PUSH DI
3faf:05e7  MOV DI,0xa8e8
3faf:05ea  PUSH DS
3faf:05eb  PUSH DI
3faf:05ec  MOV AX,0xff
3faf:05ef  PUSH AX
3faf:05f0  CALLF 0x4000:342f
3faf:05f5  CALLF 0x4000:336a
3faf:05fa  LEA DI,[BP + 0xfcfe]
3faf:05fe  PUSH SS
3faf:05ff  PUSH DI
3faf:0600  CALLF 0x4000:310f
3faf:0605  CALLF 0x4000:2ff2
3faf:060a  OR AX,AX
3faf:060c  JNZ 0x4000:0102
3faf:060e  MOV byte ptr [BP + -0x1],0x1
3faf:0612  MOV byte ptr [0xa8e7],0xff
3faf:0617  MOV byte ptr [0xa8e8],0x0
3faf:061c  MOV AL,byte ptr [BP + -0x1]
3faf:061f  MOV SP,BP
3faf:0621  POP BP
3faf:0622  RETF 0x4
