{ liero::FUN_249c_0000 — logical BIOS page-zero cursor service projection.
  Oracle: complete original-byte argument/service binding and bounded original
  BIOS cursor-state observations. Original takes two words, uses low bytes.
  BIOSCursorRow/Column are logical device state, not real BIOS/BDA storage.
  Only cursor position and declared far-return SP are modeled here;
  BIOS-specific register/flags effects, native ABI and reachability unresolved.
  Original asm/FUN_249c_0000.s retained as INCLUDE_ASM residue. }
procedure FUN_249c_0000(columnWord, rowWord: Word);
begin
  BIOSCursorRow := rowWord and $FF;
  BIOSCursorColumn := columnWord and $FF;
  RegisterSP := (LongInt(RegisterSP) + 8) and $FFFF;
end;
