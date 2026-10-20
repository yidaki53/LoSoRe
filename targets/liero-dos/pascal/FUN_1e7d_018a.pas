function FUN_1e7d_018a(param_1, param_2, param_3, param_4: Pointer): Boolean;
var
  local_30c: array[0..255] of Byte;
  local_20c: array[0..255] of Byte;
  local_10c: array[0..7] of Byte;
  local_104: array[0..256] of Byte;
  local_3: Boolean;
begin
  FUN_24dd_3e95(Pointer($0182), Pointer($1E7D));
  FUN_24cb_00a7(@local_10c, nil);
  FUN_1e7d_0082(#0, 0, @local_20c);
  FUN_24dd_3eaf(255, @local_104, @local_30c);
  Integer(param_4^) := FUN_1e7d_0082(#1, 65, @local_104);
  Char(param_3^) := Chr(FUN_1e7d_0082(#0, 73, @local_104));
  Char(param_2^) := Chr(FUN_1e7d_0082(#0, 68, @local_104));
  Byte(param_1^) := Byte(FUN_1e7d_0082(#0, 72, @local_104));
  local_3 := (Integer(param_4^) <> 255) and (local_104[0] <> 0);
  if Char(param_3^) = Chr(255) then local_3 := False;
  if Char(param_2^) = Chr(255) then local_3 := False;
  FUN_1e7d_018a := local_3;
end;