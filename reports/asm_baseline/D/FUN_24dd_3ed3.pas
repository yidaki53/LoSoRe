procedure FUN_24dd_3ed3(param_1, param_2: Word; param_3, param_4: Pointer);
var
  uVar2: Word;
  pbVar3, pbVar4: Pointer;
begin
  pbVar4 := param_4;
  if param_2 < 1 then
    param_2 := 1;
  pbVar3 := Pointer(Integer(param_3) + param_2);
  if Byte(param_3^) < param_2 then
    uVar2 := 0
  else
  begin
    uVar2 := Byte(param_3^) - param_2 + 1;
    if param_1 < 0 then
      param_1 := 0;
    if param_1 < uVar2 then
      uVar2 := param_1;
  end;
  Byte(param_4^) := Byte(uVar2);
  while uVar2 <> 0 do
  begin
    pbVar4 := Pointer(Integer(pbVar4) + 1);
    uVar2 := uVar2 - 1;
    Byte(pbVar4^) := Byte(pbVar3^);
    pbVar3 := Pointer(Integer(pbVar3) + 1);
  end;
end;