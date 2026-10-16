```pascal
procedure FUN_1ec2_00d0(param1, param2: Word; param3: Pointer);
var
  local4, local6: Word;
  localC: array[0..5] of Byte;
  local20C, local10C: array[0..255] of Byte;
begin
  local6 := FUN_24dd_3dbd();
  local4 := param2;
  FUN_24dd_3dbd();
  localC[0] := 0;
  if (local4 < 0) or ((local4 < 1) and (local6 < 10)) then
    FUN_24dd_3eaf(5, @localC, SS, $cc, $24dd);
  FUN_24dd_3e95(@localC, SS);
  FUN_202c_076d(local6, local4);
  FUN_24dd_3f14(@local10C, SS);
  FUN_24dd_3f14($ce, $24dd);
  FUN_24dd_3eaf(5, @localC, SS, @local20C, SS);
  if (param1 < 0) or ((param1 < 1) and ($3c < 10)) then
  begin
    FUN_24dd_3e95(@localC, SS);
    FUN_24dd_3f14($cc, $24dd);
    FUN_24dd_3eaf(5, @localC, SS, @local10C, SS);
  end;
  FUN_24dd_3e95(@localC, SS);
  FUN_202c_076d($3c, param1);
  FUN_24dd_3f14(@local10C, SS);
  FUN_24dd_3eaf(5, @localC, SS, @local20C, SS);
  FUN_24dd_3eaf($ff, param3^, param3^ shr 16, @localC, SS);
end;
```