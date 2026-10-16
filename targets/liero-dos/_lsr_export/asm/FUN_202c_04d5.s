; FUN_202c_04d5  entry=202c:04d5 size=414
202c:04d5  ENTER 0x8,0x0
202c:04d9  CMP byte ptr [BP + 0x6],0x0
202c:04dd  JNZ 0x2000:07a2
202c:04df  JMP 0x2000:089f
202c:04e2  XOR AX,AX
202c:04e4  MOV word ptr [BP + -0x8],AX
202c:04e7  JMP 0x2000:07ac
202c:04e9  INC word ptr [BP + -0x8]
202c:04ec  MOV AX,word ptr [BP + -0x8]
202c:04ef  ADD AX,word ptr [BP + 0xc]
202c:04f2  MOV word ptr [BP + -0x4],AX
202c:04f5  CMP word ptr [BP + -0x4],0x15d
202c:04fa  JLE 0x2000:07bf
202c:04fc  JMP 0x2000:092f
202c:04ff  CMP word ptr [BP + -0x4],-0x1
202c:0503  JG 0x2000:07c8
202c:0505  JMP 0x2000:0893
202c:0508  XOR AX,AX
202c:050a  MOV word ptr [BP + -0x6],AX
202c:050d  JMP 0x2000:07d2
202c:050f  INC word ptr [BP + -0x6]
202c:0512  MOV AX,word ptr [BP + -0x6]
202c:0515  ADD AX,word ptr [BP + 0xe]
202c:0518  MOV word ptr [BP + -0x2],AX
202c:051b  CMP word ptr [BP + -0x2],-0x1
202c:051f  JG 0x2000:07e4
202c:0521  JMP 0x2000:088a
202c:0524  CMP word ptr [BP + -0x2],0x1f8
202c:0529  JL 0x2000:07ee
202c:052b  JMP 0x2000:088a
202c:052e  MOV DX,word ptr [BP + -0x6]
202c:0531  IMUL AX,word ptr [BP + -0x8],0x7
202c:0535  LES DI,[BP + 0x8]
202c:0538  ADD DI,AX
202c:053a  ADD DI,DX
202c:053c  MOV AL,byte ptr ES:[DI]
202c:053f  OR AL,0x0
202c:0541  OR AL,AL
202c:0543  JA 0x2000:0808
202c:0545  JMP 0x2000:088a
202c:0548  MOV DX,word ptr [BP + -0x2]
202c:054b  MOV AX,word ptr [BP + -0x4]
202c:054e  SHL AX,0x2
202c:0551  LES DI,[0x6674]
202c:0555  ADD DI,AX
202c:0557  LES DI,ES:[DI]
202c:055a  ADD DI,DX
202c:055c  MOV AL,byte ptr ES:[DI]
202c:055f  MOV AH,0x1
202c:0561  MOV DX,0x20
202c:0564  CALLF 0x2000:8f31
202c:0569  MOV DI,DX
202c:056b  TEST byte ptr [DI + 0x6644],AL
202c:056f  JZ 0x2000:085b
202c:0571  MOV DX,word ptr [BP + -0x6]
202c:0574  IMUL AX,word ptr [BP + -0x8],0x7
202c:0578  LES DI,[BP + 0x8]
202c:057b  ADD DI,AX
202c:057d  ADD DI,DX
202c:057f  MOV CL,byte ptr ES:[DI]
202c:0582  MOV DX,word ptr [BP + -0x2]
202c:0585  MOV AX,word ptr [BP + -0x4]
202c:0588  SHL AX,0x2
202c:058b  LES DI,[0x6674]
202c:058f  ADD DI,AX
202c:0591  LES DI,ES:[DI]
202c:0594  ADD DI,DX
202c:0596  MOV byte ptr ES:[DI],CL
202c:0599  JMP 0x2000:088a
202c:059b  MOV DX,word ptr [BP + -0x6]
202c:059e  IMUL AX,word ptr [BP + -0x8],0x7
202c:05a2  LES DI,[BP + 0x8]
202c:05a5  ADD DI,AX
202c:05a7  ADD DI,DX
202c:05a9  MOV AL,byte ptr ES:[DI]
202c:05ac  XOR AH,AH
202c:05ae  ADD AX,0x3
202c:05b1  MOV CL,AL
202c:05b3  MOV DX,word ptr [BP + -0x2]
202c:05b6  MOV AX,word ptr [BP + -0x4]
202c:05b9  SHL AX,0x2
202c:05bc  LES DI,[0x6674]
202c:05c0  ADD DI,AX
202c:05c2  LES DI,ES:[DI]
202c:05c5  ADD DI,DX
202c:05c7  MOV byte ptr ES:[DI],CL
202c:05ca  CMP word ptr [BP + -0x6],0x6
202c:05ce  JZ 0x2000:0893
202c:05d0  JMP 0x2000:07cf
202c:05d3  CMP word ptr [BP + -0x8],0x6
202c:05d7  JZ 0x2000:089c
202c:05d9  JMP 0x2000:07a9
202c:05dc  JMP 0x2000:092f
202c:05df  XOR AX,AX
202c:05e1  MOV word ptr [BP + -0x8],AX
202c:05e4  JMP 0x2000:08a9
202c:05e6  INC word ptr [BP + -0x8]
202c:05e9  MOV AX,word ptr [BP + -0x8]
202c:05ec  ADD AX,word ptr [BP + 0xc]
202c:05ef  MOV word ptr [BP + -0x4],AX
202c:05f2  CMP word ptr [BP + -0x4],0x15d
202c:05f7  JLE 0x2000:08bb
202c:05f9  JMP 0x2000:092f
202c:05fb  CMP word ptr [BP + -0x4],-0x1
202c:05ff  JLE 0x2000:0926
202c:0601  XOR AX,AX
202c:0603  MOV word ptr [BP + -0x6],AX
202c:0606  JMP 0x2000:08cb
202c:0608  INC word ptr [BP + -0x6]
202c:060b  MOV AX,word ptr [BP + -0x6]
202c:060e  ADD AX,word ptr [BP + 0xe]
202c:0611  MOV word ptr [BP + -0x2],AX
202c:0614  CMP word ptr [BP + -0x2],-0x1
202c:0618  JLE 0x2000:0920
202c:061a  CMP word ptr [BP + -0x2],0x1f8
202c:061f  JGE 0x2000:0920
202c:0621  MOV DX,word ptr [BP + -0x6]
202c:0624  IMUL AX,word ptr [BP + -0x8],0x7
202c:0628  LES DI,[BP + 0x8]
202c:062b  ADD DI,AX
202c:062d  ADD DI,DX
202c:062f  MOV AL,byte ptr ES:[DI]
202c:0632  OR AL,0x0
202c:0634  OR AL,AL
202c:0636  JBE 0x2000:0920
202c:0638  MOV DX,word ptr [BP + -0x6]
202c:063b  IMUL AX,word ptr [BP + -0x8],0x7
202c:063f  LES DI,[BP + 0x8]
202c:0642  ADD DI,AX
202c:0644  ADD DI,DX
202c:0646  MOV CL,byte ptr ES:[DI]
202c:0649  MOV DX,word ptr [BP + -0x2]
202c:064c  MOV AX,word ptr [BP + -0x4]
202c:064f  SHL AX,0x2
202c:0652  LES DI,[0x6674]
202c:0656  ADD DI,AX
202c:0658  LES DI,ES:[DI]
202c:065b  ADD DI,DX
202c:065d  MOV byte ptr ES:[DI],CL
202c:0660  CMP word ptr [BP + -0x6],0x6
202c:0664  JNZ 0x2000:08c8
202c:0666  CMP word ptr [BP + -0x8],0x6
202c:066a  JZ 0x2000:092f
202c:066c  JMP 0x2000:08a6
202c:066f  LEAVE
202c:0670  RETF 0xa
