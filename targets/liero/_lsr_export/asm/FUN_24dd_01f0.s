; FUN_24dd_01f0  entry=24dd:01f0 size=14
24dd:01f0  MOV AL,byte ptr CS:[BX]
24dd:01f3  OR AL,AL
24dd:01f5  JZ 0x2000:4fcd
24dd:01f7  CALL 0x2000:5002
24dd:01fa  INC BX
24dd:01fb  JMP 0x2000:4fc0
24dd:01fd  RET
