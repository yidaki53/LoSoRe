procedure FUN_24dd_4905;
var
  param_1: Byte;
  param_2: Integer;
  param_3: Pointer;
  i: Integer;
  ofs: Word;
begin
  ofs := Word(param_3);
  for i := 0 to param_2 - 1 do begin
    Mem[ofs] := param_1;
    Inc(ofs);
  end;
end;