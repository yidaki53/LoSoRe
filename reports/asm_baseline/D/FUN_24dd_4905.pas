procedure FUN_24dd_4905(param_1: Char; param_2: Integer; param_3: Pointer);
var
  puVar1, puVar2: Pointer;
begin
  puVar2 := param_3;
  while param_2 <> 0 do
  begin
    puVar1 := puVar2;
    puVar2 := Pointer(Integer(puVar2) + 1);
    Move(param_1, puVar1^, 1);
    Dec(param_2);
  end;
end;