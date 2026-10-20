procedure FUN_24dd_3ed3(param_1, param_2: Word; param_3, param_4: Pointer);
var
  len: Byte;
  max_copy: Word;
  i: Word;
  ofs_src: Word;
  ofs_dst: Word;
begin
  if param_2 < 1 then
    param_2 := 1;
  len := Mem[Word(param_3)];
  ofs_src := Word(param_3) + param_2;
  ofs_dst := Word(param_4) + 1;
  if len < param_2 then
    max_copy := 0
  else begin
    max_copy := len - param_2 + 1;
    if param_1 < max_copy then
      max_copy := param_1;
  end;
  Mem[Word(param_4)] := max_copy;
  for i := 0 to max_copy - 1 do begin
    Mem[ofs_dst] := Mem[ofs_src];
    Inc(ofs_dst);
    Inc(ofs_src);
  end;
end;