; FUN_24dd_17d1  entry=24dd:17d1 size=264
24dd:17d1  PUSH BP
24dd:17d2  PUSH SI
24dd:17d3  PUSH DI
24dd:17d4  MOV BP,word ptr [0xd8]
24dd:17d8  MOV AX,word ptr [BP + 0x0]
24dd:17db  MOV BX,word ptr [BP + 0x2]
24dd:17de  MOV CX,word ptr [BP + 0x4]
24dd:17e1  MOV DX,word ptr [BP + 0x6]
24dd:17e4  SUB DI,DI
24dd:17e6  MOV SI,word ptr [BP + 0x8]
24dd:17e9  CMP SI,0xc001
24dd:17ed  JZ 0x2000:65e0
24dd:17ef  CMP SI,-0x10
24dd:17f2  JG 0x2000:65d1
24dd:17f4  MOV DI,AX
24dd:17f6  MOV AX,BX
24dd:17f8  MOV BX,CX
24dd:17fa  MOV CX,DX
24dd:17fc  SUB DX,DX
24dd:17fe  ADD SI,0x10
24dd:1801  INC SI
24dd:1802  JG 0x2000:65e0
24dd:1804  SHR DX,0x1
24dd:1806  RCR CX,0x1
24dd:1808  RCR BX,0x1
24dd:180a  RCR AX,0x1
24dd:180c  RCR DI,0x1
24dd:180e  JMP 0x2000:65d1
24dd:1810  SHL DI,0x1
24dd:1812  MOV DI,0x0
24dd:1815  ADC AX,DI
24dd:1817  ADC BX,DI
24dd:1819  ADC CX,DI
24dd:181b  ADC DX,DI
24dd:181d  MOV word ptr [BP + 0x0],AX
24dd:1820  MOV word ptr [BP + 0x2],BX
24dd:1823  MOV word ptr [BP + 0x4],CX
24dd:1826  MOV word ptr [BP + 0x6],DX
24dd:1829  MOV BX,DI
24dd:182b  MOV CX,DI
24dd:182d  MOV SI,DI
24dd:182f  TEST byte ptr [BP + 0x3],0x80
24dd:1833  JZ 0x2000:660f
24dd:1835  MOV BX,word ptr [BP + 0x0]
24dd:1838  MOV CX,word ptr [BP + 0x2]
24dd:183b  SHL BX,0x1
24dd:183d  RCL CX,0x1
24dd:183f  MOV AX,word ptr [BP + 0x0]
24dd:1842  MUL word ptr [BP + 0x4]
24dd:1845  ADD BX,AX
24dd:1847  ADC CX,DX
24dd:1849  ADC SI,DI
24dd:184b  ADD BX,AX
24dd:184d  ADC CX,DX
24dd:184f  ADC SI,DI
24dd:1851  MOV BX,CX
24dd:1853  MOV CX,SI
24dd:1855  SUB SI,SI
24dd:1857  MOV AX,word ptr [BP + 0x2]
24dd:185a  MUL word ptr [BP + 0x4]
24dd:185d  ADD BX,AX
24dd:185f  ADC CX,DX
24dd:1861  ADC SI,DI
24dd:1863  ADD BX,AX
24dd:1865  ADC CX,DX
24dd:1867  ADC SI,DI
24dd:1869  MOV AX,word ptr [BP + 0x0]
24dd:186c  MUL word ptr [BP + 0x6]
24dd:186f  ADD BX,AX
24dd:1871  ADC CX,DX
24dd:1873  ADC SI,DI
24dd:1875  ADD BX,AX
24dd:1877  ADC CX,DX
24dd:1879  ADC SI,DI
24dd:187b  SHL BX,0x1
24dd:187d  ADC CX,DI
24dd:187f  ADC SI,DI
24dd:1881  MOV BX,CX
24dd:1883  MOV CX,SI
24dd:1885  SUB SI,SI
24dd:1887  MOV AX,word ptr [BP + 0x4]
24dd:188a  MUL AX
24dd:188c  ADD BX,AX
24dd:188e  ADC CX,DX
24dd:1890  ADC SI,DI
24dd:1892  MOV AX,word ptr [BP + 0x6]
24dd:1895  MUL word ptr [BP + 0x2]
24dd:1898  ADD BX,AX
24dd:189a  ADC CX,DX
24dd:189c  ADC SI,DI
24dd:189e  ADD BX,AX
24dd:18a0  ADC CX,DX
24dd:18a2  ADC SI,DI
24dd:18a4  MOV AX,word ptr [BP + 0x6]
24dd:18a7  MUL word ptr [BP + 0x4]
24dd:18aa  ADD CX,AX
24dd:18ac  ADC SI,DX
24dd:18ae  ADC DI,DI
24dd:18b0  ADD CX,AX
24dd:18b2  ADC SI,DX
24dd:18b4  ADC DI,0x0
24dd:18b7  MOV AX,word ptr [BP + 0x6]
24dd:18ba  MUL AX
24dd:18bc  ADD SI,AX
24dd:18be  ADC DI,DX
24dd:18c0  MOV word ptr [BP + 0x0],BX
24dd:18c3  MOV word ptr [BP + 0x2],CX
24dd:18c6  MOV word ptr [BP + 0x4],SI
24dd:18c9  MOV word ptr [BP + 0x6],DI
24dd:18cc  MOV byte ptr [BP + 0xa],0x0
24dd:18d0  MOV word ptr [BP + 0x8],0x0
24dd:18d5  POP DI
24dd:18d6  POP SI
24dd:18d7  POP BP
24dd:18d8  RET
