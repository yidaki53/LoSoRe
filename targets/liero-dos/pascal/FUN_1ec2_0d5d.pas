procedure FUN_1ec2_0d5d(param_1: Byte; param_2: Integer; param_3: Word; param_4: Pointer);
var
  row: Integer;
  col: Word;
  ofs: Word;
begin
  ofs := Word(param_4);
  for row := 0 to param_2 - 1 do begin
    for col := 0 to param_3 - 1 do begin
      Mem[ofs] := param_1;
      Inc(ofs);
    end;
    Inc(ofs, 320 - param_3);
  end;
end;