{ Oracle: input-only original-vs-host Pascal close-wrapper composition.
  Output-mode flush remains unresolved; other non-input modes return status 67.
  Host pointer and RegisterES:DI denote the same resolved object. }
procedure FUN_24dd_3711(objectPointer: Pointer);
var
  modePointer: ^Word;
begin
  modePointer := PWord(PByte(objectPointer) + 2);
  if modePointer^ = $D7B2 then
    RunError(211);
  if modePointer^ <> $D7B1 then
  begin
    GlobalWord6410 := $67;
    Exit;
  end;
  RegisterBX := $1C;
  FUN_24dd_374d;
  modePointer^ := $D7B0;
end;
