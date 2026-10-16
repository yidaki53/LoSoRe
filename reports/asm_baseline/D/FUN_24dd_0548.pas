procedure FUN_24dd_0548;
var
  cVar1: Char;
begin
  cVar1 := FUN_24dd_2fcd;
  if cVar1 = #0 then
    WordPtr($640E)^ := $E6;
  FUN_24dd_3054;
end;