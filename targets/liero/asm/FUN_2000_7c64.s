; FUN_2000_7c64  entry=2000:7c64 size=92
24dd:2e94  PUSH BP
24dd:2e95  MOV BP,SP
24dd:2e97  PUSH AX
24dd:2e98  PUSH SI
24dd:2e99  PUSH DS
24dd:2e9a  TEST byte ptr [BP + 0x7],0x2
24dd:2e9e  JZ 0x2000:7c71
24dd:2ea0  STI
24dd:2ea1  LDS SI,[BP + 0x2]
24dd:2ea4  MOV AX,word ptr [SI + -0x1]
24dd:2ea7  SUB AL,0x34
24dd:2ea9  CMP AL,0x8
24dd:2eab  JNC 0x2000:7c89
24dd:2ead  SUB SI,0x2
24dd:2eb0  ADD word ptr [SI],0xa3ce
24dd:2eb4  MOV word ptr [BP + 0x2],SI
24dd:2eb7  JMP 0x2000:7cac
24dd:2eb9  JA 0x2000:7cb1
24dd:2ebb  TEST AH,0x20
24dd:2ebe  JNZ 0x2000:7cbe
24dd:2ec0  SUB SI,0x2
24dd:2ec3  MOV word ptr [BP + 0x2],SI
24dd:2ec6  MOV byte ptr [SI],0x9b
24dd:2ec9  INC SI
24dd:2eca  MOV AL,AH
24dd:2ecc  AND AX,0x7c0
24dd:2ecf  SHR AL,0x1
24dd:2ed1  SHR AL,0x1
24dd:2ed3  SHR AL,0x1
24dd:2ed5  XOR AL,0x18
24dd:2ed7  ADD AX,0xd826
24dd:2eda  MOV word ptr [SI],AX
24dd:2edc  POP DS
24dd:2edd  POP SI
24dd:2ede  POP AX
24dd:2edf  POP BP
24dd:2ee0  IRET
24dd:2ee1  CMP AL,0x9
24dd:2ee3  JA 0x2000:7cbe
24dd:2ee5  SUB SI,0x2
24dd:2ee8  MOV word ptr [SI],0x9b90
24dd:2eec  JMP 0x2000:7c84
24dd:2eee  JMP 0x2000:7cac
