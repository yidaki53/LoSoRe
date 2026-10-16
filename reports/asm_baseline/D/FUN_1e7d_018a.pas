```pascal
procedure FUN_1e7d_018a(var param1: Byte; var param2: Char; var param3: Char; var param4: Integer);
var
  local30c, local20c, local10c: array[0..255] of Byte;
  local104: array[0..256] of Char;
  local3: Boolean;
begin
  FUN_24dd_3e95($182, $1e7d);
  FUN_24cb_00a7(@local10c, SS);
  func_0x0001e7d0(@local20c);
  FUN_24dd_3eaf($ff, local104, SS, SS, @local30c);
  param4 := FUN_1e7d_0082(1, $41, local104, SS);
  param3 := FUN_1e7d_0082(0, $49, local104, SS);
  param2 := FUN_1e7d_0082(0, $44, local104, SS);
  param1 := FUN_1e7d_0082(0, $48, local104, SS);
  local3 := (param4 <> $ff) and (local104[0] <> #0);
  if param3 = -1 then
    local3 := False;
  if param2 = -1 then
    local3 := False;
end;
```