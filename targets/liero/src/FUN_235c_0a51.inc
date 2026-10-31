{ liero::FUN_235c_0a51 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_235c_0a51.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_235c_0a51.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_235c_0a51(void)
// 
// {
//   int iVar1;
//   uint uVar2;
//   int iVar3;
//   undefined4 uVar4;
//   int iVar5;
//   undefined2 uVar6;
//   undefined2 unaff_DS;
//   undefined1 local_3;
//   
//   local_3 = 0;
//   while( true ) {
//     if (*(char *)(local_3 + 0x67fc) != '\0') {
//       uVar4 = *(undefined4 *)((uint)local_3 * 10 + 0x6804);
//       uVar6 = (undefined2)((ulong)uVar4 >> 0x10);
//       iVar5 = (int)uVar4;
//       iVar1 = *(int *)(iVar5 + 8);
//       uVar2 = *(uint *)((uint)local_3 * 10 + 0x6809);
//       iVar3 = *(int *)((uint)local_3 * 10 + 0x680b);
//       if ((iVar1 < iVar3) || ((iVar1 <= iVar3 && (*(uint *)(iVar5 + 6) <= uVar2)))) {
//         FUN_235c_091d(CONCAT11((char)(uVar2 >> 8),local_3));
//         *(char *)0x67ce = *(char *)0x67ce + -1;
//       }
//     }
//     if (local_3 == 7) break;
//     local_3 = local_3 + 1;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_235c_0a51;
var
  recordIndex: Byte;
  recordOffset: Word;
  objectOffset: Word;
  objectSegment: Word;
  objectAddress: Longint;
  objectLow: Word;
  objectHigh: Word;
  thresholdLow: Word;
  thresholdHigh: Word;
begin
  for recordIndex := 0 to 7 do
  begin
    if DosMemory[$67FC + recordIndex] <> 0 then
    begin
      recordOffset := $6804 + Word(recordIndex) * 10;
      objectOffset := DosMemory[recordOffset] +
        Word(DosMemory[recordOffset + 1]) shl 8;
      objectSegment := DosMemory[recordOffset + 2] +
        Word(DosMemory[recordOffset + 3]) shl 8;
      objectAddress := (Longint(objectSegment) shl 4) + objectOffset;
      objectAddress := objectAddress and $FFFFF;
      objectLow := RealModeMemory[objectAddress + 6] +
        Word(RealModeMemory[objectAddress + 7]) shl 8;
      objectHigh := RealModeMemory[objectAddress + 8] +
        Word(RealModeMemory[objectAddress + 9]) shl 8;
      thresholdLow := DosMemory[recordOffset + 5] +
        Word(DosMemory[recordOffset + 6]) shl 8;
      thresholdHigh := DosMemory[recordOffset + 7] +
        Word(DosMemory[recordOffset + 8]) shl 8;

      if (SmallInt(thresholdHigh) > SmallInt(objectHigh)) or
         ((thresholdHigh = objectHigh) and
          (thresholdLow >= objectLow)) then
      begin
        FUN_235c_091d(recordIndex);
        Dec(DosMemory[$67CE]);
      end;
    end;
  end;
end;
