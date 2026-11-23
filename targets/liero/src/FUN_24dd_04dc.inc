function FUN_24dd_04dc: Longint;
var adjustedAX, highWord: Word; carryOut: Boolean;
begin
  carryOut := LongInt(RegisterAX) + 7 > $ffff;
  adjustedAX := (LongInt(RegisterAX) + 7) and $ffff;
  highWord := adjustedAX shr 4;
  if carryOut then highWord := highWord or $1000;
  RegisterAX := adjustedAX and $8;
  RegisterDX := highWord;
  RegisterCarryFlag := False; RegisterZeroFlag := False;
  FUN_24dd_04dc := (LongInt(RegisterDX) shl 16) + RegisterAX;
end;
