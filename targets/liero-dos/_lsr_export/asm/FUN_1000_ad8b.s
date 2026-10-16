; FUN_1000_ad8b  entry=1000:ad8b size=701
1000:ad8b  PUSH BP
1000:ad8c  MOV BP,SP
1000:ad8e  MOV AX,0x312
1000:ad91  CALLF 0x2000:5300
1000:ad96  SUB SP,0x312
1000:ad9a  MOV DI,word ptr [BP + 0x4]
1000:ad9d  MOV byte ptr SS:[DI + 0xfdf2],0x1
1000:ada3  CALLF 0x2000:4c64
1000:ada8  LEA DI,[BP + 0xfdef]
1000:adac  PUSH SS
1000:adad  PUSH DI
1000:adae  MOV AX,word ptr [BP + 0x6]
1000:adb1  CWD
1000:adb2  PUSH DX
1000:adb3  PUSH AX
1000:adb4  CALLF 0x2000:0a2d
1000:adb9  LEA DI,[BP + 0xfef1]
1000:adbd  PUSH SS
1000:adbe  PUSH DI
1000:adbf  PUSH 0xff
1000:adc2  CALLF 0x2000:8c7f
1000:adc7  LEA DI,[BP + 0xfdef]
1000:adcb  PUSH SS
1000:adcc  PUSH DI
1000:adcd  MOV AX,word ptr [BP + 0x8]
1000:add0  CWD
1000:add1  PUSH DX
1000:add2  PUSH AX
1000:add3  CALLF 0x2000:0a2d
1000:add8  POP DI
1000:add9  POP ES
1000:adda  MOV AL,byte ptr ES:[DI]
1000:addd  XOR AH,AH
1000:addf  XOR DX,DX
1000:ade1  MOV word ptr [BP + -0xe],AX
1000:ade4  MOV word ptr [BP + -0xc],DX
1000:ade7  LEA DI,[BP + 0xfdef]
1000:adeb  PUSH SS
1000:adec  PUSH DI
1000:aded  LEA DI,[BP + 0xfef1]
1000:adf1  PUSH SS
1000:adf2  PUSH DI
1000:adf3  CALLF 0x2000:8c65
1000:adf8  MOV DI,0xad89
1000:adfb  PUSH CS
1000:adfc  PUSH DI
1000:adfd  CALLF 0x2000:8ce4
1000:ae02  CALLF 0x2000:0933
1000:ae07  MOV word ptr [BP + 0xfeef],AX
1000:ae0b  MOV AX,word ptr [BP + 0xfeef]
1000:ae0f  SHR AX,0x1
1000:ae11  MOV DX,AX
1000:ae13  MOV AX,word ptr [BP + 0xc]
1000:ae16  SUB AX,0xa
1000:ae19  SUB AX,DX
1000:ae1b  MOV DX,AX
1000:ae1d  IMUL AX,word ptr [BP + 0xe],0x140
1000:ae22  LES DI,[0x6684]
1000:ae26  ADD DI,AX
1000:ae28  ADD DI,DX
1000:ae2a  PUSH ES
1000:ae2b  PUSH DI
1000:ae2c  MOV AX,word ptr [BP + 0xfeef]
1000:ae30  SHR AX,0x1
1000:ae32  MOV DX,AX
1000:ae34  MOV AX,word ptr [BP + 0xc]
1000:ae37  SUB AX,0xa
1000:ae3a  SUB AX,DX
1000:ae3c  MOV DX,AX
1000:ae3e  IMUL AX,word ptr [BP + 0xe],0x140
1000:ae43  LES DI,[0x65d7]
1000:ae47  ADD DI,AX
1000:ae49  ADD DI,DX
1000:ae4b  PUSH ES
1000:ae4c  PUSH DI
1000:ae4d  MOV AX,word ptr [BP + 0xfeef]
1000:ae51  SHR AX,0x1
1000:ae53  MOV DX,AX
1000:ae55  MOV AX,0x140
1000:ae58  SUB AX,word ptr [BP + 0xc]
1000:ae5b  ADD AX,0xa
1000:ae5e  ADD AX,DX
1000:ae60  PUSH AX
1000:ae61  PUSH 0x8
1000:ae63  CALLF 0x1000:ecc5
1000:ae68  MOV AX,word ptr [BP + 0xfeef]
1000:ae6c  SHR AX,0x1
1000:ae6e  MOV DX,AX
1000:ae70  MOV AX,word ptr [BP + 0xc]
1000:ae73  DEC AX
1000:ae74  DEC AX
1000:ae75  SUB AX,DX
1000:ae77  MOV DX,AX
1000:ae79  IMUL AX,word ptr [BP + 0xe],0x140
1000:ae7e  LES DI,[0x65d7]
1000:ae82  ADD DI,AX
1000:ae84  ADD DI,DX
1000:ae86  PUSH ES
1000:ae87  PUSH DI
1000:ae88  PUSH word ptr [BP + 0xfeef]
1000:ae8c  PUSH 0x7
1000:ae8e  PUSH 0x0
1000:ae90  CALLF 0x1000:f9a8
1000:ae95  MOV AX,word ptr [BP + 0xfeef]
1000:ae99  SHR AX,0x1
1000:ae9b  MOV DX,AX
1000:ae9d  MOV AX,word ptr [BP + 0xc]
1000:aea0  SUB AX,DX
1000:aea2  PUSH AX
1000:aea3  MOV AX,word ptr [BP + 0xe]
1000:aea6  INC AX
1000:aea7  PUSH AX
1000:aea8  LEA DI,[BP + 0xfdef]
1000:aeac  PUSH SS
1000:aead  PUSH DI
1000:aeae  LEA DI,[BP + 0xfef1]
1000:aeb2  PUSH SS
1000:aeb3  PUSH DI
1000:aeb4  CALLF 0x2000:8c65
1000:aeb9  MOV DI,0xad89
1000:aebc  PUSH CS
1000:aebd  PUSH DI
1000:aebe  CALLF 0x2000:8ce4
1000:aec3  PUSH 0x32
1000:aec5  LES DI,[0x65d7]
1000:aec9  PUSH ES
1000:aeca  PUSH DI
1000:aecb  MOV DI,0x19a6
1000:aece  PUSH DS
1000:aecf  PUSH DI
1000:aed0  CALLF 0x2000:0009
1000:aed5  MOV AX,word ptr [BP + 0xfeef]
1000:aed9  SHR AX,0x1
1000:aedb  MOV DX,AX
1000:aedd  MOV AX,word ptr [BP + 0xc]
1000:aee0  SUB AX,0xa
1000:aee3  SUB AX,DX
1000:aee5  MOV DX,AX
1000:aee7  IMUL AX,word ptr [BP + 0xe],0x140
1000:aeec  LES DI,[0x65d7]
1000:aef0  ADD DI,AX
1000:aef2  ADD DI,DX
1000:aef4  PUSH ES
1000:aef5  PUSH DI
1000:aef6  MOV AX,word ptr [BP + 0xfeef]
1000:aefa  SHR AX,0x1
1000:aefc  MOV DX,AX
1000:aefe  MOV AX,word ptr [BP + 0xc]
1000:af01  SUB AX,0xa
1000:af04  SUB AX,DX
1000:af06  IMUL DI,word ptr [BP + 0xe],0x140
1000:af0b  ADD DI,AX
1000:af0d  MOV AX,0xa000
1000:af10  PUSH AX
1000:af11  PUSH DI
1000:af12  MOV AX,word ptr [BP + 0xfeef]
1000:af16  SHR AX,0x1
1000:af18  MOV DX,AX
1000:af1a  MOV AX,0x140
1000:af1d  SUB AX,word ptr [BP + 0xc]
1000:af20  ADD AX,0xa
1000:af23  ADD AX,DX
1000:af25  PUSH AX
1000:af26  PUSH 0x8
1000:af28  CALLF 0x1000:ecc5
1000:af2d  CALLF 0x2000:4b5d
1000:af32  MOV byte ptr [BP + -0xf],AL
1000:af35  MOV AL,byte ptr [BP + -0xf]
1000:af38  CMP AL,0x30
1000:af3a  JC 0x1000:af89
1000:af3c  CMP AL,0x39
1000:af3e  JA 0x1000:af89
1000:af40  MOV AL,byte ptr [BP + 0xfef1]
1000:af44  XOR AH,AH
1000:af46  XOR DX,DX
1000:af48  CMP DX,word ptr [BP + -0xc]
1000:af4b  JL 0x1000:af54
1000:af4d  JG 0x1000:af87
1000:af4f  CMP AX,word ptr [BP + -0xe]
1000:af52  JNC 0x1000:af87
1000:af54  LEA DI,[BP + 0xfcef]
1000:af58  PUSH SS
1000:af59  PUSH DI
1000:af5a  LEA DI,[BP + 0xfef1]
1000:af5e  PUSH SS
1000:af5f  PUSH DI
1000:af60  CALLF 0x2000:8c65
1000:af65  LEA DI,[BP + 0xfdef]
1000:af69  PUSH SS
1000:af6a  PUSH DI
1000:af6b  MOV AL,byte ptr [BP + -0xf]
1000:af6e  PUSH AX
1000:af6f  CALLF 0x2000:8d81
1000:af74  CALLF 0x2000:8ce4
1000:af79  LEA DI,[BP + 0xfef1]
1000:af7d  PUSH SS
1000:af7e  PUSH DI
1000:af7f  PUSH 0xff
1000:af82  CALLF 0x2000:8c7f
1000:af87  JMP 0x1000:afa1
1000:af89  CMP AL,0x8
1000:af8b  JNZ 0x1000:afa1
1000:af8d  LEA DI,[BP + 0xfef1]
1000:af91  PUSH SS
1000:af92  PUSH DI
1000:af93  MOV AL,byte ptr [BP + 0xfef1]
1000:af97  XOR AH,AH
1000:af99  PUSH AX
1000:af9a  PUSH 0x1
1000:af9c  CALLF 0x2000:8e0d
1000:afa1  CMP byte ptr [BP + 0xfef1],0x0
1000:afa6  JZ 0x1000:afbc
1000:afa8  LEA DI,[BP + 0xfef1]
1000:afac  PUSH SS
1000:afad  PUSH DI
1000:afae  LEA DI,[BP + -0x6]
1000:afb1  PUSH SS
1000:afb2  PUSH DI
1000:afb3  MOV DI,word ptr [BP + 0x4]
1000:afb6  PUSH DI
1000:afb7  CALL 0x1000:a8f7
1000:afba  JMP 0x1000:afc6
1000:afbc  MOV AX,word ptr [BP + 0xa]
1000:afbf  CWD
1000:afc0  MOV word ptr [BP + -0x6],AX
1000:afc3  MOV word ptr [BP + -0x4],DX
1000:afc6  CMP byte ptr [BP + -0xf],0xd
1000:afca  JZ 0x1000:afcf
1000:afcc  JMP 0x1000:ade7
1000:afcf  CALLF 0x2000:4c30
1000:afd4  MOV AX,word ptr [BP + 0xa]
1000:afd7  CWD
1000:afd8  CMP DX,word ptr [BP + -0x4]
1000:afdb  JG 0x1000:afe4
1000:afdd  JL 0x1000:afee
1000:afdf  CMP AX,word ptr [BP + -0x6]
1000:afe2  JBE 0x1000:afee
1000:afe4  MOV AX,word ptr [BP + 0xa]
1000:afe7  CWD
1000:afe8  MOV word ptr [BP + -0x6],AX
1000:afeb  MOV word ptr [BP + -0x4],DX
1000:afee  MOV AX,word ptr [BP + 0x8]
1000:aff1  CWD
1000:aff2  CMP DX,word ptr [BP + -0x4]
1000:aff5  JL 0x1000:affe
1000:aff7  JG 0x1000:b008
1000:aff9  CMP AX,word ptr [BP + -0x6]
1000:affc  JNC 0x1000:b008
1000:affe  MOV AX,word ptr [BP + 0x8]
1000:b001  CWD
1000:b002  MOV word ptr [BP + -0x6],AX
1000:b005  MOV word ptr [BP + -0x4],DX
1000:b008  MOV AX,word ptr [BP + -0x6]
1000:b00b  MOV word ptr [BP + -0x2],AX
1000:b00e  CMP byte ptr [BP + 0xfef1],0x0
1000:b013  JNZ 0x1000:b020
1000:b015  MOV DI,word ptr [BP + 0x4]
1000:b018  MOV byte ptr SS:[DI + 0xfef4],0x0
1000:b01e  JMP 0x1000:b029
1000:b020  MOV DI,word ptr [BP + 0x4]
1000:b023  MOV byte ptr SS:[DI + 0xfef4],0x1
1000:b029  CMP byte ptr [0x4b8],0x0
1000:b02e  JZ 0x1000:b041
1000:b030  PUSH word ptr [0x67a6]
1000:b034  PUSH word ptr [0x67a4]
1000:b038  PUSH 0x0
1000:b03a  PUSH 0x0
1000:b03c  CALLF 0x2000:3f1c
1000:b041  MOV AX,word ptr [BP + -0x2]
1000:b044  LEAVE
1000:b045  RET 0xc
