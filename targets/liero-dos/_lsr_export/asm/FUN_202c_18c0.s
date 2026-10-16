; FUN_202c_18c0  entry=202c:18c0 size=708
202c:18c0  ENTER 0x6,0x0
202c:18c4  XOR AX,AX
202c:18c6  MOV word ptr [BP + -0x2],AX
202c:18c9  IMUL AX,word ptr [BP + -0x2],0x14
202c:18cd  LES DI,[0x6688]
202c:18d1  ADD DI,AX
202c:18d3  CMP byte ptr ES:[DI + 0x10],0x0
202c:18d8  JBE 0x2000:1ba6
202c:18da  CMP word ptr [BP + -0x2],0x258
202c:18df  JGE 0x2000:1ba6
202c:18e1  INC word ptr [BP + -0x2]
202c:18e4  JMP 0x2000:1b89
202c:18e6  MOV AL,byte ptr [BP + 0x1a]
202c:18e9  AND AL,0x7f
202c:18eb  MOV byte ptr [BP + -0x5],AL
202c:18ee  MOV DL,byte ptr [BP + 0x1a]
202c:18f1  IMUL AX,word ptr [BP + -0x2],0x14
202c:18f5  LES DI,[0x6688]
202c:18f9  ADD DI,AX
202c:18fb  MOV byte ptr ES:[DI + 0x10],DL
202c:18ff  MOV CX,word ptr [BP + 0x16]
202c:1902  MOV BX,word ptr [BP + 0x18]
202c:1905  IMUL AX,word ptr [BP + -0x2],0x14
202c:1909  LES DI,[0x6688]
202c:190d  ADD DI,AX
202c:190f  MOV word ptr ES:[DI],CX
202c:1912  MOV word ptr ES:[DI + 0x2],BX
202c:1916  MOV CX,word ptr [BP + 0x12]
202c:1919  MOV BX,word ptr [BP + 0x14]
202c:191c  IMUL AX,word ptr [BP + -0x2],0x14
202c:1920  LES DI,[0x6688]
202c:1924  ADD DI,AX
202c:1926  MOV word ptr ES:[DI + 0x4],CX
202c:192a  MOV word ptr ES:[DI + 0x6],BX
202c:192e  MOV AL,byte ptr [BP + -0x5]
202c:1931  XOR AH,AH
202c:1933  MOV DI,AX
202c:1935  SHL DI,0x1
202c:1937  MOV AX,word ptr [DI + 0xc7c]
202c:193b  SHL AX,0x1
202c:193d  PUSH AX
202c:193e  CALLF 0x2000:9424
202c:1943  XOR DX,DX
202c:1945  PUSH DX
202c:1946  PUSH AX
202c:1947  MOV AL,byte ptr [BP + -0x5]
202c:194a  XOR AH,AH
202c:194c  MOV DI,AX
202c:194e  SHL DI,0x1
202c:1950  MOV AX,word ptr [DI + 0xc7c]
202c:1954  CWD
202c:1955  PUSH DX
202c:1956  PUSH AX
202c:1957  MOV AL,byte ptr [BP + 0x6]
202c:195a  CBW
202c:195b  MOV DI,AX
202c:195d  SHL DI,0x3
202c:1960  MOV CX,word ptr [DI + 0x159e]
202c:1964  MOV BX,word ptr [DI + 0x15a0]
202c:1968  MOV AX,word ptr [BP + 0x10]
202c:196b  CWD
202c:196c  CALLF 0x2000:8b50
202c:1971  MOV CX,0x64
202c:1974  XOR BX,BX
202c:1976  CALLF 0x2000:8b8d
202c:197b  ADD AX,word ptr [BP + 0xc]
202c:197e  ADC DX,word ptr [BP + 0xe]
202c:1981  POP CX
202c:1982  POP BX
202c:1983  SUB AX,CX
202c:1985  SBB DX,BX
202c:1987  POP CX
202c:1988  POP BX
202c:1989  ADD AX,CX
202c:198b  ADC DX,BX
202c:198d  MOV CX,AX
202c:198f  MOV BX,DX
202c:1991  IMUL AX,word ptr [BP + -0x2],0x14
202c:1995  LES DI,[0x6688]
202c:1999  ADD DI,AX
202c:199b  MOV word ptr ES:[DI + 0x8],CX
202c:199f  MOV word ptr ES:[DI + 0xa],BX
202c:19a3  MOV AL,byte ptr [BP + -0x5]
202c:19a6  XOR AH,AH
202c:19a8  MOV DI,AX
202c:19aa  SHL DI,0x1
202c:19ac  MOV AX,word ptr [DI + 0xc7c]
202c:19b0  SHL AX,0x1
202c:19b2  PUSH AX
202c:19b3  CALLF 0x2000:9424
202c:19b8  XOR DX,DX
202c:19ba  PUSH DX
202c:19bb  PUSH AX
202c:19bc  MOV AL,byte ptr [BP + -0x5]
202c:19bf  XOR AH,AH
202c:19c1  MOV DI,AX
202c:19c3  SHL DI,0x1
202c:19c5  MOV AX,word ptr [DI + 0xc7c]
202c:19c9  CWD
202c:19ca  PUSH DX
202c:19cb  PUSH AX
202c:19cc  MOV AL,byte ptr [BP + 0x6]
202c:19cf  CBW
202c:19d0  MOV DI,AX
202c:19d2  SHL DI,0x3
202c:19d5  MOV CX,word ptr [DI + 0x15a2]
202c:19d9  MOV BX,word ptr [DI + 0x15a4]
202c:19dd  MOV AX,word ptr [BP + 0x10]
202c:19e0  CWD
202c:19e1  CALLF 0x2000:8b50
202c:19e6  MOV CX,0x64
202c:19e9  XOR BX,BX
202c:19eb  CALLF 0x2000:8b8d
202c:19f0  ADD AX,word ptr [BP + 0x8]
202c:19f3  ADC DX,word ptr [BP + 0xa]
202c:19f6  POP CX
202c:19f7  POP BX
202c:19f8  SUB AX,CX
202c:19fa  SBB DX,BX
202c:19fc  POP CX
202c:19fd  POP BX
202c:19fe  ADD AX,CX
202c:1a00  ADC DX,BX
202c:1a02  MOV CX,AX
202c:1a04  MOV BX,DX
202c:1a06  IMUL AX,word ptr [BP + -0x2],0x14
202c:1a0a  LES DI,[0x6688]
202c:1a0e  ADD DI,AX
202c:1a10  MOV word ptr ES:[DI + 0xc],CX
202c:1a14  MOV word ptr ES:[DI + 0xe],BX
202c:1a18  MOV AL,byte ptr [BP + -0x5]
202c:1a1b  XOR AH,AH
202c:1a1d  MOV DI,AX
202c:1a1f  SHL DI,0x1
202c:1a21  CMP word ptr [DI + 0x1104],-0x1
202c:1a26  JG 0x2000:1ceb
202c:1a28  JMP 0x2000:1dde
202c:1a2b  MOV AL,byte ptr [BP + -0x5]
202c:1a2e  XOR AH,AH
202c:1a30  MOV DI,AX
202c:1a32  MOV AL,byte ptr [DI + 0x11a5]
202c:1a36  CMP AL,0x0
202c:1a38  JNZ 0x2000:1d66
202c:1a3a  MOV AL,byte ptr [BP + -0x5]
202c:1a3d  XOR AH,AH
202c:1a3f  MOV DI,AX
202c:1a41  CMP byte ptr [DI + 0x117d],0x1
202c:1a46  JNZ 0x2000:1d55
202c:1a48  MOV AL,byte ptr [BP + -0x5]
202c:1a4b  XOR AH,AH
202c:1a4d  MOV DI,AX
202c:1a4f  CMP byte ptr [DI + 0x1155],0x0
202c:1a54  JBE 0x2000:1d3c
202c:1a56  MOV AL,byte ptr [BP + -0x5]
202c:1a59  XOR AH,AH
202c:1a5b  MOV DI,AX
202c:1a5d  MOV AL,byte ptr [DI + 0x1155]
202c:1a61  XOR AH,AH
202c:1a63  INC AX
202c:1a64  PUSH AX
202c:1a65  CALLF 0x2000:9424
202c:1a6a  MOV DL,AL
202c:1a6c  IMUL AX,word ptr [BP + -0x2],0x14
202c:1a70  LES DI,[0x6688]
202c:1a74  ADD DI,AX
202c:1a76  MOV byte ptr ES:[DI + 0x11],DL
202c:1a7a  JMP 0x2000:1d53
202c:1a7c  PUSH 0x2
202c:1a7e  CALLF 0x2000:9424
202c:1a83  MOV DL,AL
202c:1a85  IMUL AX,word ptr [BP + -0x2],0x14
202c:1a89  LES DI,[0x6688]
202c:1a8d  ADD DI,AX
202c:1a8f  MOV byte ptr ES:[DI + 0x11],DL
202c:1a93  JMP 0x2000:1d64
202c:1a95  IMUL AX,word ptr [BP + -0x2],0x14
202c:1a99  LES DI,[0x6688]
202c:1a9d  ADD DI,AX
202c:1a9f  MOV byte ptr ES:[DI + 0x11],0x0
202c:1aa4  JMP 0x2000:1ddc
202c:1aa6  CMP AL,0x1
202c:1aa8  JNZ 0x2000:1db2
202c:1aaa  CMP byte ptr [BP + 0x6],0x40
202c:1aae  JLE 0x2000:1d73
202c:1ab0  DEC byte ptr [BP + 0x6]
202c:1ab3  MOV AL,byte ptr [BP + 0x6]
202c:1ab6  CBW
202c:1ab7  SUB AX,0xc
202c:1aba  MOV word ptr [BP + -0x4],AX
202c:1abd  MOV AX,word ptr [BP + -0x4]
202c:1ac0  CWD
202c:1ac1  MOV CX,0x8
202c:1ac4  IDIV CX
202c:1ac6  MOV word ptr [BP + -0x4],AX
202c:1ac9  CMP word ptr [BP + -0x4],0x0
202c:1acd  JGE 0x2000:1d94
202c:1acf  XOR AX,AX
202c:1ad1  MOV word ptr [BP + -0x4],AX
202c:1ad4  CMP word ptr [BP + -0x4],0xc
202c:1ad8  JLE 0x2000:1d9f
202c:1ada  MOV word ptr [BP + -0x4],0xc
202c:1adf  MOV DL,byte ptr [BP + -0x4]
202c:1ae2  IMUL AX,word ptr [BP + -0x2],0x14
202c:1ae6  LES DI,[0x6688]
202c:1aea  ADD DI,AX
202c:1aec  MOV byte ptr ES:[DI + 0x11],DL
202c:1af0  JMP 0x2000:1ddc
202c:1af2  CMP AL,0x2
202c:1af4  JZ 0x2000:1dba
202c:1af6  CMP AL,0x3
202c:1af8  JNZ 0x2000:1dcd
202c:1afa  MOV DL,byte ptr [BP + 0x6]
202c:1afd  IMUL AX,word ptr [BP + -0x2],0x14
202c:1b01  LES DI,[0x6688]
202c:1b05  ADD DI,AX
202c:1b07  MOV byte ptr ES:[DI + 0x11],DL
202c:1b0b  JMP 0x2000:1ddc
202c:1b0d  IMUL AX,word ptr [BP + -0x2],0x14
202c:1b11  LES DI,[0x6688]
202c:1b15  ADD DI,AX
202c:1b17  MOV byte ptr ES:[DI + 0x11],0x0
202c:1b1c  JMP 0x2000:1e06
202c:1b1e  PUSH 0x2
202c:1b20  CALLF 0x2000:9424
202c:1b25  MOV DX,AX
202c:1b27  MOV AL,byte ptr [BP + -0x5]
202c:1b2a  XOR AH,AH
202c:1b2c  MOV DI,AX
202c:1b2e  MOV AL,byte ptr [DI + 0x11cd]
202c:1b32  XOR AH,AH
202c:1b34  SUB AX,DX
202c:1b36  MOV DL,AL
202c:1b38  IMUL AX,word ptr [BP + -0x2],0x14
202c:1b3c  LES DI,[0x6688]
202c:1b40  ADD DI,AX
202c:1b42  MOV byte ptr ES:[DI + 0x11],DL
202c:1b46  MOV AL,byte ptr [BP + -0x5]
202c:1b49  XOR AH,AH
202c:1b4b  MOV DI,AX
202c:1b4d  SHL DI,0x1
202c:1b4f  PUSH word ptr [DI + 0x1064]
202c:1b53  CALLF 0x2000:9424
202c:1b58  XOR DX,DX
202c:1b5a  MOV CX,AX
202c:1b5c  MOV BX,DX
202c:1b5e  MOV AL,byte ptr [BP + -0x5]
202c:1b61  XOR AH,AH
202c:1b63  MOV DI,AX
202c:1b65  SHL DI,0x1
202c:1b67  MOV AX,word ptr [DI + 0x1014]
202c:1b6b  CWD
202c:1b6c  SUB AX,CX
202c:1b6e  SBB DX,BX
202c:1b70  MOV DX,AX
202c:1b72  IMUL AX,word ptr [BP + -0x2],0x14
202c:1b76  LES DI,[0x6688]
202c:1b7a  ADD DI,AX
202c:1b7c  MOV word ptr ES:[DI + 0x12],DX
202c:1b80  LEAVE
202c:1b81  RETF 0x16
