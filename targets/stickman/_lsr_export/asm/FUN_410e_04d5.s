; FUN_410e_04d5  entry=410e:04d5 size=33
410e:04d5  INC DH
410e:04d7  CMP DH,byte ptr [0xeb0d]
410e:04db  JBE 0x4000:15d5
410e:04dd  DEC DH
410e:04df  PUSH CX
410e:04e0  PUSH DX
410e:04e1  MOV AX,0x601
410e:04e4  MOV BH,byte ptr [0xeb08]
410e:04e8  MOV CX,word ptr [0xeb0a]
410e:04ec  MOV DX,word ptr [0xeb0c]
410e:04f0  CALL 0x4000:16e9
410e:04f3  POP DX
410e:04f4  POP CX
410e:04f5  RET
