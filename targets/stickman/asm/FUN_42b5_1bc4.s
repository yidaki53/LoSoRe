; FUN_42b5_1bc4  entry=42b5:1bc4 size=19
42b5:1bc4  MOV BX,SP
42b5:1bc6  MOV AL,byte ptr SS:[BX + 0x4]
42b5:1bca  CMP AL,0x61
42b5:1bcc  JC 0x4000:4724
42b5:1bce  CMP AL,0x7a
42b5:1bd0  JA 0x4000:4724
42b5:1bd2  SUB AL,0x20
42b5:1bd4  RETF 0x2
