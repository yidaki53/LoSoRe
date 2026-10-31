procedure FUN_1000_05a4;
var
  i: Word;
begin
  if Mem[$04B8] <> 0 then begin
    FUN_2000_44DD();
    FUN_2000_38EE();
    for i := 1 to $001E do
      FUN_2000_3EA4(Word($6734 + i * 4));
    FUN_2000_3A62();
  end;
end;