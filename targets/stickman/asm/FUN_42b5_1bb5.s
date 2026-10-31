; FUN_42b5_1bb5  entry=42b5:1bb5 size=15
42b5:1bb5  PUSH DS
42b5:1bb6  LEA DX,[BP + -0x80]
42b5:1bb9  PUSH SS
42b5:1bba  POP DS
42b5:1bbb  INT 0x21
42b5:1bbd  POP DS
42b5:1bbe  JNC 0x4000:4713
42b5:1bc0  MOV [0x39c],AX
42b5:1bc3  RET
