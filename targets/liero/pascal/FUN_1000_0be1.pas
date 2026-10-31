procedure FUN_1000_0be1(param_1: Word; param_2: Word; param_3: Word; param_4: Word; param_5: Word; param_6: Word);
var
  slot: Word;
  base: Word;
begin
  slot := 0;
  while (slot < $02BC) and (Mem[$6690 + slot * $11] <> 0) do
    Inc(slot);
  if slot < $02BC then begin
    base := Word($6690 + slot * $11);
    Mem[base] := (FUN_2000_9424(2) + $50) and $FF;
    MemW[base + 3] := param_6;
    MemW[base + 7] := param_5;
    MemW[base + 9] := param_4;
    MemW[base + $0B] := param_3;
    MemW[base + $0D] := param_1;
    MemW[base + $0F] := param_2;
  end;
end;