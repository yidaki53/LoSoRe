{ liero::FUN_249c_0013 — SS frame attribute-byte arithmetic.
  Oracle: exact original bytes, exhaustive byte-pair runtime checks and
  original caller-prefix differential. Existing Integer interface preserves
  the one-word argument bits; historical pointer/type identity is unknown.
  Runtime uses a sequential 20-bit segmented memory image. Writable cells
  must not alias active original return/argument/saved-BP frames or code.
  Native TP7 ABI, arbitrary stack aliasing and whole caller remain unresolved;
  original asm/FUN_249c_0013.s retained as INCLUDE_ASM residue. }
procedure FUN_249c_0013(param_1: Integer);
var
  frameOffset, firstOffset, secondOffset, resultOffset: Word;
  resultAddress, value: LongInt;
begin
  frameOffset := LongInt(param_1) and $FFFF;
  firstOffset := (LongInt(frameOffset) - 261) and $FFFF;
  secondOffset := (LongInt(frameOffset) - 260) and $FFFF;
  resultOffset := (LongInt(frameOffset) - 259) and $FFFF;
  RegisterDX := ReadStackByte(secondOffset);
  value := LongInt(ReadStackByte(firstOffset)) * 16 + RegisterDX;
  resultAddress := ((LongInt(RegisterSS) shl 4) + resultOffset) and $FFFFF;
  RealModeMemory[resultAddress] := value and $FF;
  RegisterAX := value;
  RegisterDI := frameOffset;
  RegisterCarryFlag := False;
  RegisterZeroFlag := value = 0;
  RegisterSP := (LongInt(RegisterSP) + 4) and $FFFF;
end;
