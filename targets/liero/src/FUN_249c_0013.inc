procedure FUN_249c_0013(param_1: Word; param_2: Pointer);
var p: PByte; value: LongInt;
begin
  p := PByte(param_2);
  value := (LongInt(p[0]) shl 4) + p[1];
  RegisterAX := value; RegisterDX := p[1]; RegisterDI := param_1;
  p[2] := value and 255;
  RegisterCarryFlag := False; RegisterZeroFlag := value = 0;
  RegisterSP := (RegisterSP + 4) and 65535;
end;
