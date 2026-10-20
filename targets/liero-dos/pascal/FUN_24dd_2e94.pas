procedure FUN_24dd_2e94;
var
  flag: Byte;
  code_byte: Byte;
  ret_offs: Word;
  code_word: Word;
begin
  flag := Mem[$0000];
  if (flag and $02) <> 0 then begin
    code_byte := Mem[$0000];
    if code_byte < $3C then begin
      ret_offs := MemW[$0000];
      ret_offs := ret_offs + $A3CE;
      MemW[$0000] := ret_offs;
    end
    else if code_byte = $3C then begin
      code_word := MemW[$0000];
      if (code_word and $2000) = 0 then begin
        Mem[$0000] := $9B;
        ret_offs := ((code_word and $07C0) shr 3) xor $18;
        ret_offs := ret_offs + $D826;
        MemW[$0000] := ret_offs;
      end;
    end
    else if code_byte = $3D then begin
      MemW[$0000] := $9B90;
    end;
  end;
end;