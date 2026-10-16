; FUN_24dd_04dc  entry=24dd:04dc size=17
24dd:04dc  ADD AX,0x7
24dd:04df  MOV DX,AX
24dd:04e1  RCR DX,0x1
24dd:04e3  SHR DX,0x1
24dd:04e5  SHR DX,0x1
24dd:04e7  SHR DX,0x1
24dd:04e9  AND AX,0x8
24dd:04ec  RET
