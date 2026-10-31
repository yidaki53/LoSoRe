{ Oracle: input-only original-vs-host Pascal open/reopen composition.
  Host pointer resolves the object; RegisterES:DI must mirror its logical address.
  Output-mode transitions remain unresolved and abort before side effects. }
procedure FUN_24dd_36c4(objectPointer: Pointer);
var
  modePointer, positionPointer: ^Word;
  requestedMode: Word;
begin
  requestedMode := RegisterDX;
  modePointer := PWord(PByte(objectPointer) + 2);
  if (requestedMode <> $D7B1) or (modePointer^ = $D7B2) then
    RunError(211);
  if modePointer^ = $D7B1 then
    FUN_24dd_3711(objectPointer)
  else if modePointer^ <> $D7B0 then
  begin
    GlobalWord6410 := $66;
    Exit;
  end;
  RegisterDX := requestedMode;
  modePointer^ := requestedMode;
  positionPointer := PWord(PByte(objectPointer) + 8);
  positionPointer^ := 0;
  Inc(positionPointer);
  positionPointer^ := 0;
  RegisterBX := $10;
  FUN_24dd_374d;
  if not RegisterZeroFlag then
    modePointer^ := $D7B0;
end;
