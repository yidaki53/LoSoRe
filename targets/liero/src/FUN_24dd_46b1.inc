{ liero::FUN_24dd_46b1 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_46b1.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_46b1.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_46b1(void)
// 
// {
//   int iVar1;
//   long lVar2;
//   uint uVar3;
//   char cVar4;
//   int iVar5;
//   undefined2 unaff_DS;
//   
//   iVar1 = *(int *)0x6414;
//   lVar2 = (ulong)*(uint *)0x6412 * (ulong)uRam000246e7;
//   uVar3 = (uint)lVar2;
//   iVar5 = *(uint *)0x6412 << 3;
//   cVar4 = (char)iVar5;
//   iVar5 = (int)((ulong)lVar2 >> 0x10) + CONCAT11((char)((uint)iVar5 >> 8) + cVar4,cVar4) + iVar1 * 5
//   ;
//   *(int *)0x6412 = uVar3 + 1;
//   *(int *)0x6414 =
//        CONCAT11((char)((uint)iVar5 >> 8) + (char)iVar1 * '\x04' + (char)(iVar1 << 7),(char)iVar5) +
//        (uint)(0xfffe < uVar3);
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_46b1;
var
  stateLow: Word;
  stateHigh: Word;
  multiplier: Word;
  product: LongWord;
  foldedState: Word;
  nextLow: Word;
  nextHigh: Word;
begin
  stateLow := Word(DosMemory[$6412]) or (Word(DosMemory[$6413]) shl 8);
  stateHigh := Word(DosMemory[$6414]) or (Word(DosMemory[$6415]) shl 8);
  multiplier := Word(CodeMemory[$46E7]) or (Word(CodeMemory[$46E8]) shl 8);

  product := LongWord(stateLow) * LongWord(multiplier);
  nextHigh := Word(product shr 16);
  foldedState := Word((stateLow shl 3) and $FFFF);
  foldedState := (foldedState and $00FF) or
    (Word(Byte((foldedState shr 8) + (foldedState and $00FF))) shl 8);
  nextHigh := Word(nextHigh + foldedState);
  nextHigh := Word(nextHigh + stateHigh);
  stateHigh := Word(stateHigh shl 2);
  nextHigh := Word(nextHigh + stateHigh);
  nextHigh := (nextHigh and $00FF) or
    (Word(Byte((nextHigh shr 8) + (stateHigh and $00FF))) shl 8);
  stateHigh := Word(stateHigh shl 5);
  nextHigh := (nextHigh and $00FF) or
    (Word(Byte((nextHigh shr 8) + (stateHigh and $00FF))) shl 8);

  nextLow := Word(Word(DosMemory[$6412]) or
    (Word(DosMemory[$6413]) shl 8));
  Inc(nextLow);
  if nextLow = 0 then
    Inc(nextHigh);

  DosMemory[$6412] := Byte(nextLow);
  DosMemory[$6413] := Byte(nextLow shr 8);
  DosMemory[$6414] := Byte(nextHigh);
  DosMemory[$6415] := Byte(nextHigh shr 8);
  RegisterAX := nextLow;
  RegisterDX := nextHigh;
end;
