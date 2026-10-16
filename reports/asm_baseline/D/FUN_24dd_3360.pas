```pascal
procedure FUN_24dd_3360;
var
  local_28, local_26, local_24, local_22, local_20, local_18, local_16, local_14, local_12: Word;
  local_10, local_8, local_6, local_4, local_2: Word;
  local_0: Byte;
begin
  asm
    PUSH BP
    MOV BP, SP
    SUB SP, 0x28
  end;

  repeat
    asm
      INT 0x35
      JLE 0x2000:8138
      INT 0x3c
      CWD
      POP SI
      XOR CX, BP
      AAA
      JLE 0x2000:8130
    end;
  until False;

  if CX > 0x12 then
    CX := 0x12
  else if CX < -0x12 then
    CX := 0xffee;

  asm
    MOV word ptr [BP + -0x6], CX
    CLD
    INT 0x3d
  end;

  local_10 := word ptr [BP + -0xc];
  local_8 := local_10;
  local_6 := local_10 and $7fff;

  if local_6 = 0 then
  begin
    local_28 := local_28 and $ff00;
    local_4 := 0;
  end
  else if local_6 = $7fff then
  begin
    if local_12 = $8000 then
    begin
      if local_10 < 0 then
      begin
        asm
          MOV AX, word ptr [BP + -0x28]
          INC AX
          MOV word ptr [BP + -0x28], AX
          MOV AL, 0x2d
          STOSB ES:DI
        end;
      end;
      asm
        MOV AX, 0x4e49
        STOSW ES:DI
        MOV AL, 0x46
        STOSB ES:DI
      end;
    end
    else
    begin
      asm
        MOV AX, 0x414e
        STOSW ES:DI
        MOV AL, 0x4e
        STOSB ES:DI
      end;
    end;
    goto LAB_24dd_34fc;
  end
  else
  begin
    asm
      INT 0x37
      OUTSB DX, SI
      IN AL, DX
      SUB AX, 0x3fff
      MOV DX, 0x4d10
      IMUL DX
      MOV word ptr [BP + -0x8], DX
      MOV AX, 0x11
      SUB AX, DX
      CALL 0x2000:83a4
      INT 0x35
      CLD
      INT 0x3c
      WAIT
      DEC DX
      XOR CX, BP
      XOR AL, 0xd9
      INT 0x39
      JLE 0x2000:81be
      INT 0x3d
      TEST word ptr [BP + -0x4], 0x4100
      JZ 0x2000:81d4
      INT 0x3c
      CALLF 0xffff:bd66
      INC SI
      CLC
      INT 0x3b
      JBE 0x2000:81c4
      LEA BX, [BP + -0x28]
      MOV CL, 0x4
      MOV SI, 0x9
      INT 0x3d
      MOV AL, byte ptr [BP + SI + -0x15]
      MOV AH, AL
      SHR AL, CL
      AND AH, 0xf
      ADD AX, 0x3030
      MOV word ptr SS:[BX], AX
      INC BX
      INC BX
      DEC SI
      JNZ 0x2000:81e2
      MOV word ptr SS:[BX], SI
      CMP word ptr [BP + -0x6], 0x0
      JL 0x2000:820b
      CMP word ptr [BP + -0x8], 0x24