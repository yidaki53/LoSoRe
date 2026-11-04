{ Oracle: original-vs-host close-wrapper composition, checked output flush/close.
  Output flush status never suppresses close; other modes return status 67.
  Host pointer and RegisterES:DI denote the same resolved object. }
procedure FUN_24dd_3711(objectPointer: Pointer);
var
  modePointer: ^Word;
begin
  modePointer := PWord(PByte(objectPointer) + 2);
  if (modePointer^ <> $D7B1) and (modePointer^ <> $D7B2) then
  begin
    GlobalWord6410 := $67;
    Exit;
  end;
  if modePointer^ = $D7B2 then begin
    RegisterBX := $14;
    FUN_24dd_374d;
  end;
  RegisterBX := $1C;
  FUN_24dd_374d;
  modePointer^ := $D7B0;
end;
