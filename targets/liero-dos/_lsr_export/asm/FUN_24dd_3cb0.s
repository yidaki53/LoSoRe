; FUN_24dd_3cb0  entry=24dd:3cb0 size=48
24dd:3cb0  PUSH BP
24dd:3cb1  MOV BP,SP
24dd:3cb3  LES DI,[BP + 0xa]
24dd:3cb6  CALL 0x2000:89d3
24dd:3cb9  JNZ 0x2000:8aac
24dd:3cbb  MOV AX,word ptr [BP + 0x8]
24dd:3cbe  MUL word ptr ES:[DI + 0x4]
24dd:3cc2  MOV CX,AX
24dd:3cc4  MOV AX,word ptr [BP + 0x6]
24dd:3cc7  MUL word ptr ES:[DI + 0x4]
24dd:3ccb  ADD CX,DX
24dd:3ccd  MOV DX,AX
24dd:3ccf  MOV BX,word ptr ES:[DI]
24dd:3cd2  MOV AX,0x4200
24dd:3cd5  INT 0x21
24dd:3cd7  JNC 0x2000:8aac
24dd:3cd9  MOV [0x6410],AX
24dd:3cdc  POP BP
24dd:3cdd  RETF 0x8
