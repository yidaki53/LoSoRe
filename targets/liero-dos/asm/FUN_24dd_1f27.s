; FUN_24dd_1f27  entry=24dd:1f27 size=87
24dd:1f27  PUSH BP
24dd:1f28  MOV BP,SP
24dd:1f2a  PUSH SI
24dd:1f2b  PUSH DI
24dd:1f2c  CMP word ptr [SI + 0x8],-0x40
24dd:1f30  JLE 0x2000:6d48
24dd:1f32  SUB word ptr [0xd8],0xc
24dd:1f37  MOV DI,word ptr [0xd8]
24dd:1f3b  CALL 0x2000:5352
24dd:1f3e  INC word ptr [DI + 0x8]
24dd:1f41  PUSH SI
24dd:1f42  PUSH DI
24dd:1f43  PUSH DI
24dd:1f44  CALL 0x2000:5cb2
24dd:1f47  PUSH SI
24dd:1f48  PUSH DI
24dd:1f49  PUSH DI
24dd:1f4a  CALL 0x2000:6047
24dd:1f4d  CALL 0x2000:5443
24dd:1f50  MOV BX,word ptr [0xd8]
24dd:1f54  ADD word ptr [BX + 0x8],0x2
24dd:1f58  CALL 0x2000:65a1
24dd:1f5b  PUSH word ptr CS:[0x1dc9]
24dd:1f60  MOV AX,0x1dcb
24dd:1f63  PUSH AX
24dd:1f64  CALL 0x2000:66a9
24dd:1f67  PUSH word ptr [0xd8]
24dd:1f6b  PUSH DI
24dd:1f6c  PUSH SI
24dd:1f6d  CALL 0x2000:5e77
24dd:1f70  INC word ptr [SI + 0x8]
24dd:1f73  ADD word ptr [0xd8],0x18
24dd:1f78  POP DI
24dd:1f79  POP SI
24dd:1f7a  MOV SP,BP
24dd:1f7c  POP BP
24dd:1f7d  RET
