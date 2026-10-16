procedure FUN_1ec2_0d5d(param_1: Char; param_2: Integer; param_3: Word; param_4: Pointer);
var
  puVar1, puVar3: Pointer;
  uVar2: Word;
begin
  puVar3 := param_4;
  uVar2 := param_3;
  repeat
    uVar2 := uVar2 or param_3;
    while uVar2 <> 0 do
    begin
      puVar1 := puVar3;
      puVar3 := Pointer(Integer(puVar3) + 1);
      puVar1^ := param_1;
      Dec(uVar2);
    end;
    puVar3 := Pointer(Integer(puVar3) + $140 - param_3);
    Dec(param_2);
    uVar2 := 0;
  until param_2 = 0;
end;