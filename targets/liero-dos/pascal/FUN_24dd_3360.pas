procedure FUN_24dd_3360(param_1: Word; param_2: Pointer);
var
  local_2a: array[0..8] of Word;
  ab_stack_17: array[0..6] of Byte;
  local_10: Integer;
  local_e: Word;
  local_c: Word;
  local_a: Word;
  local_8: Word;
  local_6: Word;
  i: Word;
  p: Word;
begin
  p := Word(param_2);
  { software FPU check: INT 0x35 / INT 0x3C }
  { clamp exponent to -0x12..0x12 }
  local_8 := 0;
  if local_8 > $12 then
    local_8 := $12;
  if local_8 < -$12 then
    local_8 := -$12;
  { INT 0x3D - get FPU status }
  local_e := MemW[p];
  local_c := local_e;
  local_a := local_e and $7FFF;
  if local_a = 0 then begin
    local_2a[0] := local_2a[0] and $FF00;
  end
  else if local_a = $7FFF then begin
    { infinity / NaN }
    if local_10 = -$8000 then begin
      if local_e < 0 then begin
        Mem[p] := $2D;
        Inc(p);
      end;
      MemW[p] := $414E;
      Inc(p);
      Inc(p);
      Mem[p] := $4E;
      Inc(p);
    end
    else begin
      MemW[p] := $4E49;
      Inc(p);
      Inc(p);
      Mem[p] := $46;
      Inc(p);
    end;
  end
  else begin
    { normal value: convert digits }
    local_e := local_a;
    i := 8;
    while i > 0 do begin
      local_2a[i] := (local_2a[i] and $0F00) shr 8;
      Dec(i);
    end;
    local_2a[0] := 0;
    { write sign }
    if local_8 < 0 then begin
      Mem[p] := $2D;
      Inc(p);
    end;
    { write digits }
    i := 0;
    while local_2a[i] <> 0 do begin
      Mem[p] := Mem[Word(@local_2a) + i];
      Inc(p);
      Inc(i);
    end;
    { write decimal point and exponent }
    Mem[p] := $2E;
    Inc(p);
    Mem[p] := $45;
    Inc(p);
    if local_8 < 0 then begin
      Mem[p] := $2D;
      Inc(p);
    end
    else begin
      Mem[p] := $2B;
      Inc(p);
    end;
    Mem[p] := (local_8 div 10) + $30;
    Inc(p);
    Mem[p] := (local_8 mod 10) + $30;
    Inc(p);
  end;
end;