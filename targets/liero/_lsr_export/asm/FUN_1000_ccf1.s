; FUN_1000_ccf1  entry=1000:ccf1 size=562
1000:ccf1  PUSH BP
1000:ccf2  MOV BP,SP
1000:ccf4  XOR AX,AX
1000:ccf6  CALLF 0x2000:5300
1000:ccfb  MOV AL,byte ptr [BP + 0x8]
1000:ccfe  CMP AL,0x4
1000:cd00  JZ 0x1000:cd16
1000:cd02  CMP AL,0x5
1000:cd04  JZ 0x1000:cd16
1000:cd06  CMP AL,0x8
1000:cd08  JZ 0x1000:cd16
1000:cd0a  CMP AL,0x9
1000:cd0c  JZ 0x1000:cd16
1000:cd0e  CMP AL,0xa
1000:cd10  JZ 0x1000:cd16
1000:cd12  CMP AL,0xb
1000:cd14  JNZ 0x1000:cd5f
1000:cd16  CMP byte ptr [0x4b8],0x0
1000:cd1b  JZ 0x1000:cd47
1000:cd1d  CMP byte ptr [BP + 0x6],0x0
1000:cd21  JLE 0x1000:cd36
1000:cd23  PUSH word ptr [0x67a2]
1000:cd27  PUSH word ptr [0x67a0]
1000:cd2b  PUSH 0x0
1000:cd2d  PUSH 0x0
1000:cd2f  CALLF 0x2000:3f1c
1000:cd34  JMP 0x1000:cd47
1000:cd36  PUSH word ptr [0x679e]
1000:cd3a  PUSH word ptr [0x679c]
1000:cd3e  PUSH 0x0
1000:cd40  PUSH 0x0
1000:cd42  CALLF 0x2000:3f1c
1000:cd47  MOV byte ptr [0x78e0],0x0
1000:cd4c  MOV byte ptr [0x78de],0x0
1000:cd51  MOV AL,byte ptr [BP + 0x8]
1000:cd54  PUSH AX
1000:cd55  MOV DI,word ptr [BP + 0x4]
1000:cd58  PUSH DI
1000:cd59  CALL 0x1000:bfd7
1000:cd5c  JMP 0x1000:cf1f
1000:cd5f  CMP AL,0x0
1000:cd61  JNZ 0x1000:cdc0
1000:cd63  CMP byte ptr [0x4b8],0x0
1000:cd68  JZ 0x1000:cd94
1000:cd6a  CMP byte ptr [BP + 0x6],0x0
1000:cd6e  JLE 0x1000:cd83
1000:cd70  PUSH word ptr [0x67a2]
1000:cd74  PUSH word ptr [0x67a0]
1000:cd78  PUSH 0x0
1000:cd7a  PUSH 0x0
1000:cd7c  CALLF 0x2000:3f1c
1000:cd81  JMP 0x1000:cd94
1000:cd83  PUSH word ptr [0x679e]
1000:cd87  PUSH word ptr [0x679c]
1000:cd8b  PUSH 0x0
1000:cd8d  PUSH 0x0
1000:cd8f  CALLF 0x2000:3f1c
1000:cd94  MOV byte ptr [0x78de],0x0
1000:cd99  MOV byte ptr [0x78e0],0x0
1000:cd9e  MOV AL,byte ptr [BP + 0x6]
1000:cda1  ADD byte ptr [0x66ac],AL
1000:cda5  CMP byte ptr [0x66ac],0x0
1000:cdaa  JGE 0x1000:cdb1
1000:cdac  MOV byte ptr [0x66ac],0x3
1000:cdb1  CMP byte ptr [0x66ac],0x3
1000:cdb6  JLE 0x1000:cdbd
1000:cdb8  MOV byte ptr [0x66ac],0x0
1000:cdbd  JMP 0x1000:cf1f
1000:cdc0  CMP AL,0x1
1000:cdc2  JZ 0x1000:cdc7
1000:cdc4  JMP 0x1000:ce76
1000:cdc7  MOV DI,word ptr [BP + 0x4]
1000:cdca  CMP byte ptr SS:[DI + 0xfef3],0x0
1000:cdd0  JZ 0x1000:cdd5
1000:cdd2  JMP 0x1000:ce73
1000:cdd5  MOV AL,[0x66ac]
1000:cdd8  CMP AL,0x0
1000:cdda  JNZ 0x1000:ce09
1000:cddc  CMP byte ptr [BP + 0x6],0x0
1000:cde0  JGE 0x1000:cdf1
1000:cde2  CMP word ptr [0x669f],0x1
1000:cde7  JLE 0x1000:cdf1
1000:cde9  MOV AL,byte ptr [BP + 0x6]
1000:cdec  CBW
1000:cded  ADD word ptr [0x669f],AX
1000:cdf1  CMP byte ptr [BP + 0x6],0x0
1000:cdf5  JLE 0x1000:ce07
1000:cdf7  CMP word ptr [0x669f],0x3e7
1000:cdfd  JGE 0x1000:ce07
1000:cdff  MOV AL,byte ptr [BP + 0x6]
1000:ce02  CBW
1000:ce03  ADD word ptr [0x669f],AX
1000:ce07  JMP 0x1000:ce73
1000:ce09  CMP AL,0x1
1000:ce0b  JNZ 0x1000:ce40
1000:ce0d  CMP byte ptr [BP + 0x6],0x0
1000:ce11  JGE 0x1000:ce25
1000:ce13  CMP word ptr [0x66a1],0x3c
1000:ce18  JLE 0x1000:ce25
1000:ce1a  MOV AL,byte ptr [BP + 0x6]
1000:ce1d  CBW
1000:ce1e  IMUL AX,AX,0xa
1000:ce21  ADD word ptr [0x66a1],AX
1000:ce25  CMP byte ptr [BP + 0x6],0x0
1000:ce29  JLE 0x1000:ce3e
1000:ce2b  CMP word ptr [0x66a1],0xe10
1000:ce31  JGE 0x1000:ce3e
1000:ce33  MOV AL,byte ptr [BP + 0x6]
1000:ce36  CBW
1000:ce37  IMUL AX,AX,0xa
1000:ce3a  ADD word ptr [0x66a1],AX
1000:ce3e  JMP 0x1000:ce73
1000:ce40  CMP AL,0x2
1000:ce42  JZ 0x1000:ce48
1000:ce44  CMP AL,0x3
1000:ce46  JNZ 0x1000:ce73
1000:ce48  CMP byte ptr [BP + 0x6],0x0
1000:ce4c  JGE 0x1000:ce5d
1000:ce4e  CMP word ptr [0x66a3],0x1
1000:ce53  JLE 0x1000:ce5d
1000:ce55  MOV AL,byte ptr [BP + 0x6]
1000:ce58  CBW
1000:ce59  ADD word ptr [0x66a3],AX
1000:ce5d  CMP byte ptr [BP + 0x6],0x0
1000:ce61  JLE 0x1000:ce73
1000:ce63  CMP word ptr [0x66a3],0x3e7
1000:ce69  JGE 0x1000:ce73
1000:ce6b  MOV AL,byte ptr [BP + 0x6]
1000:ce6e  CBW
1000:ce6f  ADD word ptr [0x66a3],AX
1000:ce73  JMP 0x1000:cf1f
1000:ce76  CMP AL,0x2
1000:ce78  JNZ 0x1000:ceb2
1000:ce7a  MOV DI,word ptr [BP + 0x4]
1000:ce7d  CMP byte ptr SS:[DI + 0xfef3],0x0
1000:ce83  JNZ 0x1000:ceb0
1000:ce85  CMP byte ptr [BP + 0x6],0x0
1000:ce89  JGE 0x1000:ce9a
1000:ce8b  CMP word ptr [0x669d],0x0
1000:ce90  JBE 0x1000:ce9a
1000:ce92  MOV AL,byte ptr [BP + 0x6]
1000:ce95  CBW
1000:ce96  ADD word ptr [0x669d],AX
1000:ce9a  CMP byte ptr [BP + 0x6],0x0
1000:ce9e  JLE 0x1000:ceb0
1000:cea0  CMP word ptr [0x669d],0x270f
1000:cea6  JNC 0x1000:ceb0
1000:cea8  MOV AL,byte ptr [BP + 0x6]
1000:ceab  CBW
1000:ceac  ADD word ptr [0x669d],AX
1000:ceb0  JMP 0x1000:cf1f
1000:ceb2  CMP AL,0x3
1000:ceb4  JNZ 0x1000:ceeb
1000:ceb6  MOV DI,word ptr [BP + 0x4]
1000:ceb9  CMP byte ptr SS:[DI + 0xfef3],0x0
1000:cebf  JNZ 0x1000:cee9
1000:cec1  CMP byte ptr [BP + 0x6],0x0
1000:cec5  JGE 0x1000:ced5
1000:cec7  CMP byte ptr [0x669c],0x0
1000:cecc  JBE 0x1000:ced5
1000:cece  MOV AL,byte ptr [BP + 0x6]
1000:ced1  ADD byte ptr [0x669c],AL
1000:ced5  CMP byte ptr [BP + 0x6],0x0
1000:ced9  JLE 0x1000:cee9
1000:cedb  CMP byte ptr [0x669c],0x63
1000:cee0  JNC 0x1000:cee9
1000:cee2  MOV AL,byte ptr [BP + 0x6]
1000:cee5  ADD byte ptr [0x669c],AL
1000:cee9  JMP 0x1000:cf1f
1000:ceeb  CMP AL,0x6
1000:ceed  JNZ 0x1000:cf1f
1000:ceef  MOV DI,word ptr [BP + 0x4]
1000:cef2  CMP byte ptr SS:[DI + 0xfef3],0x0
1000:cef8  JNZ 0x1000:cf1f
1000:cefa  CMP byte ptr [BP + 0x6],0x0
1000:cefe  JGE 0x1000:cf0c
1000:cf00  CMP word ptr [0x66aa],0x0
1000:cf05  JLE 0x1000:cf0c
1000:cf07  SUB word ptr [0x66aa],0x19
1000:cf0c  CMP byte ptr [BP + 0x6],0x0
1000:cf10  JLE 0x1000:cf1f
1000:cf12  CMP word ptr [0x66aa],0x1f4
1000:cf18  JGE 0x1000:cf1f
1000:cf1a  ADD word ptr [0x66aa],0x19
1000:cf1f  LEAVE
1000:cf20  RET 0x6
