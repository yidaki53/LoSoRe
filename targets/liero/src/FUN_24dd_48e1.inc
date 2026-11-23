procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);
var sourceOffset, destinationOffset, count: LongInt; backward: Boolean;
begin
  sourceOffset := RegisterSI; destinationOffset := RegisterDI;
  count := Word(param_1); backward := sourceOffset < destinationOffset;
  Move(param_3^, param_2^, Word(count));
  RegisterBX := RegisterSP; RegisterDX := RegisterDS;
  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;
  if backward then begin
    RegisterCarryFlag := destinationOffset + count > 65535;
    RegisterZeroFlag := ((destinationOffset + count - 1) and 65535) = 0;
    RegisterSI := (sourceOffset - 1) and 65535;
    RegisterDI := (destinationOffset - 1) and 65535;
  end else begin
    RegisterCarryFlag := False; RegisterZeroFlag := sourceOffset = destinationOffset;
    RegisterSI := (sourceOffset + count) and 65535;
    RegisterDI := (destinationOffset + count) and 65535;
  end;
  RegisterSP := (RegisterSP + 14) and 65535;
end;
