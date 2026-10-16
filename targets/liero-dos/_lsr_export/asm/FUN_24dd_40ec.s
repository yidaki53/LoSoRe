; FUN_24dd_40ec  entry=24dd:40ec size=33
24dd:40ec  MOV BX,SP
24dd:40ee  LES DI,SS:[BX + 0x6]
24dd:40f2  MOV AL,byte ptr SS:[BX + 0x4]
24dd:40f6  MOV BL,AL
24dd:40f8  XOR BH,BH
24dd:40fa  MOV CL,0x3
24dd:40fc  SHR BX,CL
24dd:40fe  MOV CL,AL
24dd:4100  AND CL,0x7
24dd:4103  MOV AL,0x1
24dd:4105  SHL AL,CL
24dd:4107  OR byte ptr ES:[BX + DI],AL
24dd:410a  RETF 0x2
