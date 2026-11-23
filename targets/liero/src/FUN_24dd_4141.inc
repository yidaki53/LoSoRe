procedure FUN_24dd_4141(param_1: Word; param_2, param_3: Pointer);
var src, dst: PByte; count, skip, i, sourceOffset: LongInt;
begin
  count := param_1 and $ff; skip := param_1 shr 8;
  src := PByte(param_3); dst := PByte(param_2);
  for i := 0 to count - 1 do dst[i] := src[skip + i];
  sourceOffset := (LongInt(RegisterSI) + skip) and $ffff;
  RegisterBX := param_1; RegisterDX := RegisterDS; RegisterES := RegisterDS;
  RegisterCarryFlag := LongInt(RegisterSI) + skip > $ffff;
  RegisterZeroFlag := sourceOffset = 0;
  RegisterSI := (LongInt(RegisterSI) + skip + count) and $ffff;
  RegisterDI := (LongInt(RegisterDI) + count) and $ffff;
  RegisterCX := 0; RegisterDirectionFlag := False;
  RegisterSP := (LongInt(RegisterSP) + 14) and $ffff;
end;
