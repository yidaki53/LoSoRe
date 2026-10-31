{ liero::FUN_24dd_04dc — 16-bit AX/DX arithmetic helper.
  Oracle: exhaustive host test against the 16-bit instruction sequence. }
function FUN_24dd_04dc: Longint;
var
  originalAX: Word;
  adjustedAX: Word;
  highWord: Word;
  carryOut: Boolean;
begin
  originalAX := RegisterAX;
  carryOut := originalAX > $FFF8;
  adjustedAX := originalAX + 7;
  highWord := adjustedAX shr 4;
  if carryOut then
    highWord := highWord or $1000;
  RegisterAX := adjustedAX and $0008;
  RegisterDX := highWord;
  RegisterCarryFlag := False;
  RegisterZeroFlag := RegisterAX = 0;
  FUN_24dd_04dc := (Longint(RegisterDX) shl 16) + RegisterAX;
end;
