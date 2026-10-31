procedure FUN_2000_c9d0;
var
  x, y: Word;
  w, h: Byte;
  ptr: Pointer;
  ofs: Word;
  row: Integer;
  col: Word;
begin
  ofs := Word(ptr);
  for row := 0 to Integer(h) - 1 do begin
    for col := 0 to Word(w) - 1 do begin
      Mem[ofs] := x;
      Inc(ofs);
    end;
    Inc(ofs, 320 - Word(w));
  end;
end;