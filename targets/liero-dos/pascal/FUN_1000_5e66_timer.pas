begin
  { condition: (local_12c < 1) && ((local_12c < 0) || (local_12e < 4)) }
  if (cond_lo < 1) and ((cond_lo = $FFFF) or (cond_hi < 4)) then begin
    old_val := MemW[base];
    MemW[base] := MemW[base] + 1000;
    if old_val > $FC17 then
      MemW[base + 2] := MemW[base + 2] + 1;
  end
  else begin
    rnd := FUN_24dd_3dbd();
    MemW[base] := -rnd;
    rnd := FUN_24dd_3dbd();
    MemW[base + 2] := (not MemW[base + 2] + 1) - (Word(rnd <> 0));
  end;
  { propagate to second pair }
  MemW[base - 4] := MemW[base - 4] + MemW[base];
  carry := 0;
  if MemW[base - 4] < MemW[base] then  { unsigned overflow }
    carry := 1;
  MemW[base - 6] := MemW[base - 6] + MemW[base + 2] + carry;
end;