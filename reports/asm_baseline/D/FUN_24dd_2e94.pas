```pascal
procedure FUN_24dd_2e94;
var
  bVar1: Char;
  uVar2: Word;
  iVar4: Integer;
  uVar5: Word;
begin
  uVar5 := Word((PtrRec(@in_stack_00000000)^.Seg shr 16) and $FFFF);
  iVar4 := Integer(in_stack_00000000);
  uVar2 := Word(Ptr(iVar4 - 1, 0)^);
  bVar1 := Chr(uVar2) - Chr($34);
  if bVar1 < Chr(8) then
  begin
    Word(Ptr(iVar4 - 2, 0)^) := Word(Ptr(iVar4 - 2, 0)^) + $A3CE;
  end
  else if bVar1 < Chr(9) then
  begin
    if (uVar2 and $2000) = 0 then
    begin
      Byte(Ptr(iVar4 - 2, 0)^) := $9B;
      uVar2 := (uVar2 and $7C0) shr 3;
      Word(Ptr(iVar4 - 1, 0)^) := ((uVar2 xor $18) + $D826);
    end;
  end
  else if bVar1 < Chr(10) then
  begin
    Word(Ptr(iVar4 - 2, 0)^) := $9B90;
  end;
end;
```