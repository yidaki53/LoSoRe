procedure FUN_24dd_3d68(param_1: Integer; param_2, param_3: Pointer);
var sourceOffset, destinationOffset, count, i: LongInt; src, dst: PByte;
begin
  sourceOffset := RegisterSI; destinationOffset := RegisterDI;
  count := Word(param_1);
  src := PByte(param_3); dst := PByte(param_2);
  for i := 0 to count - 1 do dst[i] := src[i];
  RegisterBX := RegisterSP; RegisterDX := RegisterDS;
  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;
  RegisterSI := (sourceOffset + count) and 65535;
  RegisterDI := (destinationOffset + count) and 65535;
  RegisterSP := (RegisterSP + 14) and 65535;
end;
