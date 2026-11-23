procedure FUN_24dd_40d6(param_1: Word; param_2: Pointer);
var destination: ^Word; remaining, entry: Word;
begin
  entry := RegisterSP;
  destination := param_2;
  destination^ := param_1;
  Inc(destination);
  remaining := 15;
  while remaining <> 0 do
  begin
    destination^ := 0;
    Inc(destination);
    Dec(remaining);
  end;
  RegisterAX := 0; RegisterBX := entry; RegisterCX := 0; RegisterDX := $369c;
  RegisterDI := (RegisterDI + 32) and $ffff;
  RegisterSP := (entry + 6) and $ffff;
  RegisterCarryFlag := False; RegisterZeroFlag := True; RegisterDirectionFlag := False;
end;
