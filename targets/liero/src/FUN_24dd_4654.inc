{ liero::FUN_24dd_4654 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_4654.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_4654.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// int __stdcall16far FUN_24dd_4654(uint param_1)
// 
// {
//   long lVar1;
//   ulong uVar2;
//   
//   uVar2 = FUN_24dd_46b1();
//   lVar1 = (uVar2 >> 0x10) * (ulong)param_1;
//   return (int)((ulong)lVar1 >> 0x10) +
//          (uint)CARRY2((uint)lVar1,(uint)((uVar2 & 0xffff) * (ulong)param_1 >> 0x10));
// }
// 
// --- end reference ---
function FUN_24dd_4654(param_1: Word): Integer;
var
  lowProduct: LongWord;
  highProduct: LongWord;
begin
  FUN_24dd_46b1;
  lowProduct := LongWord(RegisterAX) * LongWord(param_1);
  highProduct := LongWord(RegisterDX) * LongWord(param_1);
  FUN_24dd_4654 := Integer(
    Word((highProduct + (lowProduct shr 16)) shr 16));
end;
