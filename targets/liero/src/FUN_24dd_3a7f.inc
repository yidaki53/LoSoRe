{ liero::FUN_24dd_3a7f — game Pascal draft (oracle: none).
  Drafted from asm/FUN_24dd_3a7f.s via skeleton; UNMATCHED until verify passes.
  Original assembly retained in asm/FUN_24dd_3a7f.s (INCLUDE_ASM residue).
  Reference: Ghidra decompiler C for this function is embedded below as a comment.
}
// --- reference: Ghidra decompiler C (unmatched) ---
// 
// /* WARNING: Instruction at (ram,0x00028886) overlaps instruction at (ram,0x00028885)
//     */
// /* WARNING: Removing unreachable block (ram,0x0002886f) */
// /* WARNING: Removing unreachable block (ram,0x00028876) */
// 
// uint __cdecl16far FUN_24dd_3a7f(void)
// 
// {
//   code *pcVar1;
//   undefined1 uVar2;
//   uint uVar3;
//   undefined2 extraout_DX;
//   undefined2 unaff_DS;
//   
//   FUN_24dd_37ec();
//   pcVar1 = (code *)swi(0x35);
//   uVar2 = (*pcVar1)();
//   out(extraout_DX,uVar2);
//   pcVar1 = (code *)swi(0x3d);
//   (*pcVar1)();
//   *(undefined2 *)0x6410 = 0x6a;
//   pcVar1 = (code *)swi(0x39);
//   uVar3 = (*pcVar1)();
//   return uVar3 ^ 0xcdee;
// }
// 
// --- end reference ---
function FUN_24dd_3a7f: Word;
begin
  { TODO: translate from asm/FUN_24dd_3a7f.s — UNMATCHED until an oracle passes }
end;

