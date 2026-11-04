{ Oracle: original01f0 CS-relative NUL string through checked0232 output port.
  CodeMemory is explicit original-code binding, not host address/native ABI. }
procedure FUN_24dd_01f0;
var
  value: Byte;
begin
  repeat
    value := CodeMemory[RegisterBX];
    RegisterAX := (RegisterAX and $FF00) or value;
    RegisterZeroFlag := value = 0;
    if value = 0 then Exit;
    FUN_24dd_0232(RegisterAX);
    if RegisterBX = $FFFF then RunError(211);
    Inc(RegisterBX);
  until False;
end;
