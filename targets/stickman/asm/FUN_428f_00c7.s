; FUN_428f_00c7  entry=428f:00c7 size=23
428f:00c7  PUSH BP
428f:00c8  MOV BP,SP
428f:00ca  MOV CH,byte ptr [BP + 0xc]
428f:00cd  MOV CL,byte ptr [BP + 0xa]
428f:00d0  MOV DH,byte ptr [BP + 0x8]
428f:00d3  MOV DL,byte ptr [BP + 0x6]
428f:00d6  MOV AH,0x2d
428f:00d8  INT 0x21
428f:00da  POP BP
428f:00db  RETF 0x8
