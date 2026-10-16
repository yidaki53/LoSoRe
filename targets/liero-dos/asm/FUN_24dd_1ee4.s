; FUN_24dd_1ee4  entry=24dd:1ee4 size=10
24dd:1ee4  PUSH ES
24dd:1ee5  FADD float ptr [BX + SI]
24dd:1ee7  SBB byte ptr [BX + 0x5e],BL
24dd:1eea  MOV SP,BP
24dd:1eec  POP BP
24dd:1eed  RET
