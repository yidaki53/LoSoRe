{ liero::FUN_24dd_350e — assembly-derived stack character read
  (oracle: raw assembly review; host segmented-stack tests).
  Original assembly retained in asm/FUN_24dd_350e.s.
}
function FUN_24dd_350e: Char;
var
  stackOffset: Word;
  characterValue: Byte;
begin
  stackOffset := Word(Word(RegisterBP + RegisterSI) - $0028);
  characterValue := ReadStackByte(stackOffset);
  RegisterCarryFlag := False;
  RegisterZeroFlag := characterValue = 0;
  Inc(RegisterSI);
  if characterValue = 0 then
  begin
    characterValue := Ord('0');
    Dec(RegisterSI);
    RegisterZeroFlag := RegisterSI = 0;
  end;
  RegisterAX := (RegisterAX and $FF00) or characterValue;
  FUN_24dd_350e := Chr(characterValue);
end;
