{ liero::FUN_235c_118c — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_118c.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_118c.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_235c_118c(void)
// 
// {
//   int *piVar1;
//   int *piVar2;
//   int iVar3;
//   int *piVar4;
//   int *piVar5;
//   undefined2 unaff_DS;
//   
//   piVar4 = (int *)0x6a58;
//   piVar2 = (int *)*(undefined4 *)0x6e6c;
//   iVar3 = 0x200;
//   piVar5 = (int *)piVar2;
//   do {
//     piVar1 = piVar4;
//     piVar4 = piVar4 + 1;
//     *piVar5 = *piVar1 << 5;
//     iVar3 = iVar3 + -1;
//     piVar5 = piVar5 + 1;
//   } while (iVar3 != 0);
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_118c;
var
  itemIndex: Word;
  sourceOffset: Word;
  destinationOffset: Word;
  destinationSegment: Word;
  sourceValue: Word;
  destinationAddress: Longint;
begin
  destinationOffset := DosMemory[$6E6C] +
    (Word(DosMemory[$6E6D]) shl 8);
  destinationSegment := DosMemory[$6E6E] +
    (Word(DosMemory[$6E6F]) shl 8);
  for itemIndex := 0 to $01FF do
  begin
    sourceOffset := $6A58 + itemIndex * 2;
    sourceValue := DosMemory[sourceOffset] +
      (Word(DosMemory[sourceOffset + 1]) shl 8);
    sourceValue := sourceValue shl 5;
    destinationAddress := (Longint(destinationSegment) shl 4) +
      Word(destinationOffset + itemIndex * 2);
    destinationAddress := destinationAddress and $FFFFF;
    RealModeMemory[destinationAddress] := Byte(sourceValue);
    RealModeMemory[destinationAddress + 1] := Byte(sourceValue shr 8);
  end;
end;
