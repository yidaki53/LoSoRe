procedure FUN_24dd_455e;
var magnitude: Int64; exponent, originalHigh, flagByte: Word; negative: Boolean;
begin
  originalHigh := RegisterDX;
  magnitude := Int64(RegisterDX) * 65536 + RegisterAX;
  if magnitude = 0 then begin
    RegisterAX := 0; RegisterBX := 0; RegisterDX := 0; flagByte := 0;
  end else begin
    RegisterCX := (originalHigh and $ff00) or (RegisterCX and $ff);
    negative := originalHigh >= $8000;
    if negative then magnitude := Int64(4294967296) - magnitude;
    exponent := 160;
    while magnitude < Int64(2147483648) do begin
      magnitude := magnitude * 2; Dec(exponent);
    end;
    RegisterAX := exponent; RegisterBX := magnitude and $ffff;
    RegisterDX := (magnitude shr 16) and $ffff;
    if negative then flagByte := originalHigh shr 8 else begin
      RegisterDX := RegisterDX and $7fff; flagByte := RegisterDX shr 8;
    end;
  end;
  RegisterCarryFlag := False; RegisterZeroFlag := flagByte = 0;
  RegisterSP := (RegisterSP + 2) and $ffff;
end;
