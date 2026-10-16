{ liero::FUN_24dd_31a6 — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_31a6.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_31a6.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// void __cdecl16near FUN_24dd_31a6(void)
// 
// {
//   uint uVar1;
//   longdouble lVar2;
//   undefined2 unaff_DS;
//   longdouble in_ST0;
//   
//   lVar2 = (longdouble)0;
//   *(uint *)0x7b40 =
//        (uint)NAN(in_ST0) << 8 | (uint)(in_ST0 < lVar2) << 9 | (uint)(in_ST0 != lVar2) << 10 |
//        (uint)(in_ST0 == lVar2) << 0xe;
//   uVar1 = *(uint *)0x7b40;
//   if ((((uVar1 & 0x4500) != 0) && ((uVar1 & 0x4000) != 0)) && ((uVar1 & 0x400) != 0)) {
//     return;
//   }
//   return;
// }
// 
// --- end reference ---
procedure FUN_24dd_31a6;
begin
  { TODO: translate from asm/FUN_24dd_31a6.s — UNMATCHED until an oracle passes }
end;

