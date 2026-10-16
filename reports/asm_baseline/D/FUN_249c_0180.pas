procedure FUN_249c_0180;
var
  AL, AH, uVar2, uVar3: Byte;
begin
  AH := $B;
  Intr($21, AH);
  AL := AH;  { Assuming AL is set by the interrupt }
  uVar2 := AL;
  if uVar2 = $FF then
  begin
    uVar3 := uVar2 + 1;
  end
  else
  begin
    uVar3 := uVar2;
  end;
  { Return value is in AL, which is the lower byte of uVar3 }
end;