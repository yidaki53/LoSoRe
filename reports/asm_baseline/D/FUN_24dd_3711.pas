```pascal
procedure FUN_24dd_3711(param_1: Pointer);
var
  uVar2: Word;
  iVar1: Integer;
begin
  uVar2 := Word(LongInt(param_1) shr 16);
  iVar1 := Integer(param_1);
  if PInteger(LongInt(param_1) + 2)^ <> -0x284F then
  begin
    if PInteger(LongInt(param_1) + 2)^ <> -0x284E then
    begin
      WordPtr($6410)^ := $67;
      Exit;
    end;
    FUN_24dd_374d;
  end;
  FUN_24dd_374d;
  PWord(LongInt(param_1) + 2)^ := $D7B0;
end;
```